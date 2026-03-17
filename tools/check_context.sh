#!/bin/bash

# Fonction pour afficher le contexte Windows
check_windows_context() {
    echo "=== Contexte Windows ==="
    cmd.exe /c ver
    echo "Utilisateur : $USERNAME"
    echo "Répertoire : $(pwd)"
    echo "===================="
}

# Fonction pour afficher le contexte WSL
check_wsl_context() {
    echo "=== Contexte WSL ==="
    uname -a
    echo "Utilisateur : $(whoami)"
    echo "Groupes : $(id)"
    echo "Répertoire : $(pwd)"
    echo "Distribution : $(cat /etc/*release 2>/dev/null | grep PRETTY_NAME)"
    echo "===================="
}

# Fonction pour afficher le contexte Podman
check_podman_context() {
    echo "=== Contexte Podman ==="
    if command -v podman &> /dev/null; then
        echo "Version Podman : $(podman version --format '{{.Client.Version}}')"
        echo "Machine active : $(podman machine list 2>/dev/null | grep -w "Currently running")"
        echo "État de connexion au registre :"
        podman login --get-login registry.redhat.io 2>/dev/null || echo "Non connecté"
    else
        echo "Podman n'est pas installé"
    fi
    echo "===================="
}

# Exécution principale
echo "### VÉRIFICATION DU CONTEXTE ###"
echo "Date : $(date)"
echo

# Vérification du contexte actuel
if [ -f /proc/version ] && grep -qi microsoft /proc/version; then
    check_wsl_context
    check_podman_context
else
    check_windows_context
fi
