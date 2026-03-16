# Script PowerShell pour l'extraction des JAR
# Utilise la configuration locale pour plus de sécurité

# Lecture de la configuration
$config = Get-Content ".\extract_jar.local.conf" | Where-Object { $_ -notmatch '^\s*#' } | ConvertFrom-StringData

# Vérification des arguments
if ($args.Count -eq 0) {
    Write-Host "Usage: .\extract_jar.ps1 <chemin_du_jar>"
    Write-Host "Exemple: .\extract_jar.ps1 'd:\Fractal Softworks\Starsector\starsector-core\starfarer.api.jar'"
    exit 1
}

$jarPath = $args[0]

# Création des répertoires
if (-not (Test-Path $config.OUTPUT_DIR)) {
    New-Item -ItemType Directory -Path $config.OUTPUT_DIR
}
if (-not (Test-Path $config.BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $config.BACKUP_DIR
}

# Timestamp pour le backup
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$jarName = [System.IO.Path]::GetFileNameWithoutExtension($jarPath)
$jarExt = [System.IO.Path]::GetExtension($jarPath)
$backupPath = Join-Path $config.BACKUP_DIR "${jarName}_${timestamp}${jarExt}"

# Backup du JAR
Write-Host "Création du backup..."
Copy-Item $jarPath $backupPath

# Extraction du JAR
Write-Host "Liste du contenu du JAR..."
& $config.JAVA_PATH -jar $jarPath -list

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erreur lors de l'extraction"
    exit 1
}

Write-Host "Opération terminée"
