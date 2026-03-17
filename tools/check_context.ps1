# Script de vérification du contexte système
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

Write-Host "=== Vérification du Contexte Système ==="
Write-Host "Date : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Host

# Version Windows
Write-Host "=== Windows ==="
$osInfo = [System.Environment]::OSVersion.Version
Write-Host "Version : $($osInfo.Major).$($osInfo.Minor) (Build $($osInfo.Build))"
Write-Host "Utilisateur : $env:USERNAME"
Write-Host "Répertoire : $(Get-Location)"
Write-Host

# WSL
Write-Host "=== WSL ==="
$wslStatus = wsl --status 2>&1
Write-Host $wslStatus
Write-Host

# Podman
Write-Host "=== Podman ==="
try {
    $podmanVersion = wsl -d podman-machine-default podman version --format '{{.Client.Version}}' 2>&1
    Write-Host "Version : $podmanVersion"
    
    $podmanMachine = wsl -d podman-machine-default podman machine list 2>&1
    Write-Host "Machine : $podmanMachine"
} catch {
    Write-Host "Erreur Podman : $_"
}
Write-Host

# Environnement
Write-Host "=== Variables d'Environnement ==="
Write-Host "PATH : $env:PATH"
Write-Host "TEMP : $env:TEMP"
Write-Host "SystemRoot : $env:SystemRoot"
