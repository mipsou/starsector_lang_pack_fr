<#
  Verifie que les fichiers du mod restent compatibles avec le jeu :
  - memes lignes et memes valeurs que la reference pour toutes les colonnes non traduites ;
  - memes nombres de %s / {{...}} et memes variables $... dans les colonnes traduites ;
  - JSON des .faction partiels valides.
  Reference : -Baseline (copie precedente du mod) si le fichier y existe, sinon vanilla.

  Usage : .\tools\Test-Translations.ps1 -Vanilla "<Starsector>\starsector-core\data" [-Baseline "<ancien mod>\data"]
#>
param(
  [Parameter(Mandatory)] [string]$Vanilla,
  [string]$Baseline,
  [string]$ModData = (Join-Path $PSScriptRoot '..\data'),
  [string]$Translations = (Join-Path $PSScriptRoot 'translations')
)
$errors = 0
function Fail($msg) { $script:errors++; Write-Host "ECHEC  $msg" -ForegroundColor Red }
function Tokens($s) {
  if (-not $s) { return '' }
  $pct = ([regex]::Matches($s, '%s')).Count
  $hl = ([regex]::Matches($s, '\{\{')).Count
  # les possessifs/complements anglais ($hisOrHer...) n'ont pas d'equivalent direct : le FR peut s'en passer
  $vars = ([regex]::Matches($s, '\$[A-Za-z_][\w.]*') | % Value | ? { $_ -notmatch '^\$(his|him)Or(Her|Herself)$' } | Sort-Object -Unique) -join ' '
  "%s=$pct {{=$hl vars=[$vars]"
}

foreach ($tf in Get-ChildItem $Translations -Filter *.json | Sort-Object Name) {
  $t = Get-Content $tf.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
  if ($t.format -eq 'partial') {
    foreach ($f in $t.files.PSObject.Properties) {
      try { Get-Content (Join-Path $ModData $f.Name) -Raw -Encoding UTF8 | ConvertFrom-Json | Out-Null }
      catch { Fail "$($f.Name) : JSON invalide" }
    }
    "OK     {0} ({1} fichiers)" -f $tf.Name, @($t.files.PSObject.Properties).Count
    continue
  }
  if ($t.format -eq 'json') { continue }

  $ref = if ($Baseline -and (Test-Path (Join-Path $Baseline $t.file))) { Join-Path $Baseline $t.file } else { Join-Path $Vanilla $t.file }
  $a = @(Import-Csv $ref -Encoding UTF8 3>$null)
  $b = @(Import-Csv (Join-Path $ModData $t.file) -Encoding UTF8 3>$null)
  $en = @{}; foreach ($r in (Import-Csv (Join-Path $Vanilla $t.file) -Encoding UTF8 3>$null)) { $en[($t.key | % { $r.$_ }) -join '|'] = $r }
  if ($a.Count -ne $b.Count) { Fail "$($t.file) : $($a.Count) lignes attendues, $($b.Count) obtenues"; continue }
  $translated = @{}
  foreach ($e in $t.entries.PSObject.Properties) { $translated[$e.Name] = @($e.Value.PSObject.Properties.Name) }
  $cols = $a[0].PSObject.Properties.Name
  for ($i = 0; $i -lt $a.Count; $i++) {
    $k = ($t.key | % { $a[$i].$_ }) -join '|'
    foreach ($c in $cols) {
      $isTr = $translated.ContainsKey($k) -and ($translated[$k] -contains $c)
      if (-not $isTr) {
        if ($a[$i].$c -cne $b[$i].$c) { Fail "$($t.file) [$k].$c modifie hors traduction" }
      } elseif ($en.ContainsKey($k)) {
        $te = Tokens $en[$k].$c; $tfr = Tokens $b[$i].$c
        if ($te -ne $tfr) { Fail "$($t.file) [$k].$c : EN $te / FR $tfr" }
        # options de rules.csv : le jeu decoupe "ordre:id:texte" sur les ':' ; un ':' de plus dans le texte fait planter le chargement
        if ($c -eq 'options' -and ($en[$k].$c.Split(':').Count -ne $b[$i].$c.Split(':').Count)) { Fail "$($t.file) [$k].options : deux-points en trop dans le texte" }
      }
    }
  }
  "OK     {0} ({1} lignes)" -f $tf.Name, $b.Count
}
if ($errors) { Write-Host "$errors erreur(s)" -ForegroundColor Red; exit 1 } else { Write-Host 'Tout est valide.' -ForegroundColor Green }
