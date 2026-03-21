# Outils Java pour Starsector

## Environnement Java
- Version : Java 7 (1.7.0_79-b15)
- Type : JRE (Java Runtime Environment)
- Localisation : `d:\Fractal Softworks\Starsector\jre`

## Gestion des JAR

### Approche Recommandée
1. Utiliser le système de mods natif via `mod_info.json`
2. Pour les fichiers dans les JAR :
   ```
   starsector-core/
   └── data/
       └── strings/
           └── jar_content/  # Contenu extrait des JAR
   ```

### Outils Disponibles
1. Classes Java 7 utiles :
   - `java.util.jar.JarFile` : Lecture des JAR
   - `java.util.zip.ZipEntry` : Manipulation des entrées
   - `java.nio.file.Files` : Opérations fichiers
   - `java.nio.file.Paths` : Gestion chemins

2. Commandes JRE :
   ```bash
   # Lister le contenu d'un JAR
   java -jar starsector.jar -list

   # Extraire des fichiers
   java -jar starsector.jar -extract fichier.txt
   ```

### Sécurité
1. Ne jamais modifier les JAR originaux
2. Toujours créer des backups
3. Utiliser le système de mods pour les remplacements
4. Valider l'intégrité des fichiers extraits

### Workflow Recommandé
1. Extraire les fichiers nécessaires
2. Créer les traductions
3. Utiliser `mod_info.json` pour le remplacement
4. Tester in-game
5. Valider et distribuer
