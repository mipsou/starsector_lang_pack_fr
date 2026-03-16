import java.io.*;
import java.util.*;
import java.util.jar.*;
import java.security.*;
import java.nio.file.*;

/**
 * Gestionnaire de JAR pour Starsector
 * Compatible Java 7 (1.7.0_79)
 */
public class JarManager {
    private final Path jarPath;
    private final Path outputDir;
    private final Path backupDir;

    public JarManager(String jarPath, String outputDir) {
        this.jarPath = Paths.get(jarPath);
        this.outputDir = Paths.get(outputDir);
        this.backupDir = Paths.get(outputDir, "backups", 
            String.format("%1$tY%1$tm%1$td_%1$tH%1$tM%1$tS", new Date()));
    }

    /**
     * Crée une sauvegarde du JAR original
     */
    public boolean createBackup() throws IOException {
        Files.createDirectories(backupDir);
        Files.copy(jarPath, backupDir.resolve(jarPath.getFileName()), 
                  StandardCopyOption.REPLACE_EXISTING);
        return true;
    }

    /**
     * Calcule le hash SHA-256 d'un fichier
     */
    public String calculateHash(Path file) throws IOException, NoSuchAlgorithmException {
        MessageDigest digest = MessageDigest.getInstance("SHA-256");
        byte[] hash = digest.digest(Files.readAllBytes(file));
        StringBuilder hexString = new StringBuilder();
        for (byte b : hash) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) hexString.append('0');
            hexString.append(hex);
        }
        return hexString.toString();
    }

    /**
     * Extrait les fichiers du JAR
     */
    public void extractFiles(String... patterns) throws IOException {
        try (JarFile jar = new JarFile(jarPath.toFile())) {
            createBackup();

            Enumeration<JarEntry> entries = jar.entries();
            while (entries.hasMoreElements()) {
                JarEntry entry = entries.nextElement();
                String name = entry.getName();

                // Vérifie si le fichier correspond à un des patterns
                if (patterns != null && patterns.length > 0) {
                    boolean matches = false;
                    for (String pattern : patterns) {
                        if (name.contains(pattern)) {
                            matches = true;
                            break;
                        }
                    }
                    if (!matches) continue;
                }

                // Crée le dossier parent si nécessaire
                Path outFile = outputDir.resolve(name);
                Files.createDirectories(outFile.getParent());

                // Copie le fichier
                try (InputStream in = jar.getInputStream(entry);
                     OutputStream out = Files.newOutputStream(outFile)) {
                    byte[] buffer = new byte[4096];
                    int read;
                    while ((read = in.read(buffer)) != -1) {
                        out.write(buffer, 0, read);
                    }
                }

                System.out.println("Extrait: " + name);
            }
        }
    }

    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Usage: java JarManager <jar_path> <output_dir> [pattern1 pattern2 ...]");
            System.exit(1);
        }

        try {
            JarManager manager = new JarManager(args[0], args[1]);
            String[] patterns = Arrays.copyOfRange(args, 2, args.length);
            manager.extractFiles(patterns);
            System.out.println("Extraction terminée avec succès");
        } catch (Exception e) {
            System.err.println("Erreur: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
