<#
  Injecte les traductions de tools/translations/*.json dans les fichiers du mod.

  Chaque JSON a la forme :
    { "file": "hullmods/hull_mods.csv", "key": ["id"],
      "entries": { "<cle>": { "<colonne>": "<texte FR>" } } }
  JSON copies en entier : "format": "json", "files": { "<chemin>": { "<champ>": "<texte FR>" } }.
  JSON fusionnes par le jeu (.faction, planets.json...) : "format": "partial", "files": { "<chemin>": { <objet a ecrire tel quel> } }.

  Base utilisee : le fichier du mod s'il existe, sinon le fichier vanilla.
  Seuls les champs listes sont reecrits ; tout le reste (stats, scripts) reste octet pour octet.

  Usage : .\tools\Apply-Translations.ps1 -Vanilla "<Starsector>\starsector-core\data"
#>
param(
  [Parameter(Mandatory)] [string]$Vanilla,
  [string]$ModData = (Join-Path $PSScriptRoot '..\data'),
  [string]$Translations = (Join-Path $PSScriptRoot 'translations')
)
$ErrorActionPreference = 'Stop'

Add-Type -Language CSharp -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Text;

public static class CsvPatcher {
    class Rec { public List<string> Fields = new List<string>(); public List<bool> Quoted = new List<bool>(); public string Raw; public string Eol; }

    static List<Rec> Parse(string s) {
        var recs = new List<Rec>();
        int i = 0, n = s.Length;
        while (i < n) {
            var r = new Rec(); int start = i;
            var f = new StringBuilder(); bool q = false, wasQuoted = false;
            while (true) {
                if (i >= n) { r.Fields.Add(f.ToString()); r.Quoted.Add(wasQuoted); r.Eol = ""; break; }
                char c = s[i];
                if (q) {
                    if (c == '"') { if (i + 1 < n && s[i + 1] == '"') { f.Append('"'); i += 2; continue; } q = false; i++; continue; }
                    f.Append(c); i++; continue;
                }
                if (c == '"') { q = true; wasQuoted = true; i++; continue; }
                if (c == ',') { r.Fields.Add(f.ToString()); r.Quoted.Add(wasQuoted); f.Clear(); wasQuoted = false; i++; continue; }
                if (c == '\r' || c == '\n') {
                    r.Fields.Add(f.ToString()); r.Quoted.Add(wasQuoted);
                    int e = i; if (c == '\r' && i + 1 < n && s[i + 1] == '\n') i += 2; else i++;
                    r.Eol = s.Substring(e, i - e); r.Raw = s.Substring(start, e - start); break;
                }
                f.Append(c); i++;
            }
            if (r.Raw == null) r.Raw = s.Substring(start, i - start);
            recs.Add(r);
        }
        return recs;
    }

    static string Enc(string v) {
        if (v.IndexOfAny(new[] { ',', '"', '\r', '\n' }) >= 0 || v.StartsWith(" ") || v.EndsWith(" "))
            return "\"" + v.Replace("\"", "\"\"") + "\"";
        return v;
    }

    // patches : cle -> (colonne -> valeur). Renvoie le texte patche ; 'applied' = nb de champs modifies, 'unknown' = cles absentes.
    public static string Patch(string text, string[] keyCols, Dictionary<string, Dictionary<string, string>> patches, out int applied, out List<string> unknown) {
        var recs = Parse(text);
        var header = recs[0].Fields;
        var idx = new Dictionary<string, int>();
        for (int k = 0; k < header.Count; k++) if (!idx.ContainsKey(header[k])) idx[header[k]] = k;
        var keyIdx = new int[keyCols.Length];
        for (int k = 0; k < keyCols.Length; k++) keyIdx[k] = idx[keyCols[k]];
        var seen = new HashSet<string>(); applied = 0;
        var sb = new StringBuilder(text.Length + 4096);
        for (int r = 0; r < recs.Count; r++) {
            var rec = recs[r];
            if (r > 0) {
                var parts = new string[keyIdx.Length];
                for (int k = 0; k < keyIdx.Length; k++) parts[k] = keyIdx[k] < rec.Fields.Count ? rec.Fields[keyIdx[k]] : "";
                string key = string.Join("|", parts);
                Dictionary<string, string> p;
                if (patches.TryGetValue(key, out p) && !seen.Contains(key)) {
                    seen.Add(key);
                    var outFields = new List<string>();
                    // re-tokenise les champs bruts pour conserver la forme des champs non modifies
                    for (int k = 0; k < rec.Fields.Count; k++) {
                        string col = k < header.Count ? header[k] : null;
                        string v;
                        if (col != null && p.TryGetValue(col, out v)) { outFields.Add(Enc(v)); applied++; }
                        else outFields.Add(rec.Quoted[k] ? "\"" + rec.Fields[k].Replace("\"", "\"\"") + "\"" : rec.Fields[k]);
                    }
                    sb.Append(string.Join(",", outFields)).Append(rec.Eol);
                    continue;
                }
            }
            sb.Append(rec.Raw).Append(rec.Eol);
        }
        unknown = new List<string>();
        foreach (var k in patches.Keys) if (!seen.Contains(k)) unknown.Add(k);
        return sb.ToString();
    }
}
'@

$utf8 = New-Object System.Text.UTF8Encoding($false)
$total = 0
foreach ($tf in Get-ChildItem $Translations -Filter *.json | Sort-Object Name) {
  $t = Get-Content $tf.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($t.format -eq 'partial') {
    # fichiers fusionnes par le jeu (.faction) : on n'ecrit que les champs traduits,
    # une copie complete dupliquerait les tableaux (knownShips, portraits...) a la fusion
    # les valeurs peuvent etre imbriquees ("ranks":{"posts":{"x":{"name":...}}})
    foreach ($f in $t.files.PSObject.Properties) {
      $out = Join-Path $ModData $f.Name
      New-Item -ItemType Directory -Force (Split-Path $out) | Out-Null
      [IO.File]::WriteAllText($out, ($f.Value | ConvertTo-Json -Depth 10), $utf8)
      $total += ([regex]::Matches(($f.Value | ConvertTo-Json -Depth 10 -Compress), '":"')).Count
    }
    "{0,-38} -> {1} fichiers partiels" -f $tf.Name, @($t.files.PSObject.Properties).Count
    continue
  }

  if ($t.format -eq 'json') {
    # remplacement champ par champ ("champ":"valeur") dans des JSON Starsector (qui tolerent les commentaires #),
    # copies en entier : pour les fichiers que le jeu remplace au lieu de les fusionner (descriptor.json...)
    foreach ($f in $t.files.PSObject.Properties) {
      $dst = Join-Path $ModData $f.Name
      $src = if (Test-Path $dst) { $dst } else { Join-Path $Vanilla $f.Name }
      $text = [IO.File]::ReadAllText($src, $utf8)
      $n = 0
      foreach ($p in $f.Value.PSObject.Properties) {
        $val = ($p.Value -replace '\\', '\\' -replace '"', '\"')
        $re = '("' + [regex]::Escape($p.Name) + '"\s*:\s*)"(?:[^"\\]|\\.)*"'
        if ([regex]::IsMatch($text, $re)) { $text = [regex]::Replace($text, $re, { param($m) $m.Groups[1].Value + '"' + $val + '"' }, 1); $n++ }
        else { Write-Warning "$($tf.Name): champ '$($p.Name)' introuvable dans $($f.Name)" }
      }
      New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
      [IO.File]::WriteAllText($dst, $text, $utf8)
      $total += $n
    }
    "{0,-38} -> {1} fichiers JSON" -f $tf.Name, @($t.files.PSObject.Properties).Count
    continue
  }

  $dst = Join-Path $ModData $t.file
  $src = if (Test-Path $dst) { $dst } else { Join-Path $Vanilla $t.file }
  $text = [IO.File]::ReadAllText($src, $utf8)

  $patches = New-Object 'System.Collections.Generic.Dictionary[string,System.Collections.Generic.Dictionary[string,string]]'
  foreach ($e in $t.entries.PSObject.Properties) {
    $d = New-Object 'System.Collections.Generic.Dictionary[string,string]'
    foreach ($c in $e.Value.PSObject.Properties) { $d[$c.Name] = [string]$c.Value }
    $patches[$e.Name] = $d
  }
  $n = 0; $unknown = $null
  $text = [CsvPatcher]::Patch($text, [string[]]$t.key, $patches, [ref]$n, [ref]$unknown)
  foreach ($u in $unknown) { Write-Warning "$($tf.Name): cle '$u' introuvable dans $($t.file)" }

  New-Item -ItemType Directory -Force (Split-Path $dst) | Out-Null
  [IO.File]::WriteAllText($dst, $text, $utf8)
  "{0,-38} -> {1} ({2} champs)" -f $tf.Name, $t.file, $n
  $total += $n
}
"Total : $total champs traduits"
