# Script de vérification d'encodage pour les fichiers JSON
# Usage : .\check_encoding.ps1
# Vérifie l'encodage de tous les fichiers JSON dans le dossier data/strings

# Fonction pour vérifier l'encodage d'un fichier
function Test-FileEncoding {
    param (
        [Parameter(Mandatory=$true)]
        [string]$FilePath
    )
    
    $bytes = Get-Content -Path $FilePath -Encoding Byte -ReadCount 4 -TotalCount 4
    
    # Vérifier le BOM UTF-8
    if ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        return "UTF-8 with BOM"
    }
    
    # Vérifier le contenu pour UTF-8 sans BOM
    try {
        $content = Get-Content -Path $FilePath -Raw
        $utf8 = [System.Text.Encoding]::UTF8.GetBytes($content)
        $utf8Content = [System.Text.Encoding]::UTF8.GetString($utf8)
        if ($content -eq $utf8Content) {
            return "UTF-8 without BOM"
        }
    }
    catch {
        return "Unknown"
    }
    
    return "Other"
}

# Dossier à scanner
$stringsDir = "D:\Fractal Softworks\Starsector\mods\starsector_lang_pack_fr_private\data\strings"

# Récupérer tous les fichiers JSON
$jsonFiles = Get-ChildItem -Path $stringsDir -Filter "*.json"

# Tableau pour stocker les résultats
$results = @()

# Vérifier chaque fichier
foreach ($file in $jsonFiles) {
    $encoding = Test-FileEncoding -FilePath $file.FullName
    $results += [PSCustomObject]@{
        File = $file.Name
        Encoding = $encoding
        Status = if ($encoding -eq "UTF-8 without BOM") { "✅" } else { "❌" }
    }
}

# Afficher les résultats
Write-Host "`nRésultats de la vérification d'encodage :`n"
$results | Format-Table -AutoSize

# Afficher un résumé
$validCount = ($results | Where-Object { $_.Status -eq "✅" }).Count
$totalCount = $results.Count

Write-Host "`nRésumé :"
Write-Host "- Fichiers valides (UTF-8 sans BOM) : $validCount / $totalCount"
Write-Host "- Fichiers à corriger : $($totalCount - $validCount)"

if ($validCount -ne $totalCount) {
    Write-Host "`nFichiers à corriger :"
    $results | Where-Object { $_.Status -eq "❌" } | ForEach-Object {
        Write-Host "- $($_.File) ($($_.Encoding))"
    }
}
