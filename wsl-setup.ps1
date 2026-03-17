# Script de configuration WSL2 avec systemd
# À exécuter en tant qu'administrateur

# Activer WSL2
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Définir WSL2 comme version par défaut
wsl --set-default-version 2

# Créer le fichier wsl.conf pour activer systemd
$wslconf = @"
[boot]
systemd=true

[automount]
enabled = true
options = "metadata,umask=22,fmask=11"
mountFsTab = true
"@

# Installer Ubuntu avec systemd
wsl --install Ubuntu

# Attendre que l'installation soit terminée
Start-Sleep -Seconds 10

# Copier le fichier wsl.conf dans Ubuntu
wsl -d Ubuntu -u root bash -c "echo '$wslconf' > /etc/wsl.conf"

# Redémarrer WSL
wsl --shutdown
Start-Sleep -Seconds 5
wsl -d Ubuntu
