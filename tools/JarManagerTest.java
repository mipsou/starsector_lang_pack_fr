import org.junit.*;
import static org.junit.Assert.*;
import java.nio.file.*;
import java.io.*;

/**
 * Tests unitaires pour JarManager
 */
public class JarManagerTest {
    private Path tempDir;
    private Path testJar;
    private Path outputDir;
    private JarManager manager;

    @Before
    public void setUp() throws IOException {
        // Crée un dossier temporaire pour les tests
        tempDir = Files.createTempDirectory("jar_test");
        testJar = tempDir.resolve("test.jar");
        outputDir = tempDir.resolve("output");
        
        // Crée un JAR de test
        createTestJar();
        
        manager = new JarManager(testJar.toString(), outputDir.toString());
    }

    @After
    public void tearDown() throws IOException {
        // Nettoie les fichiers temporaires
        deleteRecursively(tempDir);
    }

    private void createTestJar() throws IOException {
        // Crée un JAR minimal pour les tests
        try (FileOutputStream fos = new FileOutputStream(testJar.toFile());
             JarOutputStream jos = new JarOutputStream(fos)) {
            
            // Ajoute une entrée de test
            jos.putNextEntry(new java.util.jar.JarEntry("test.txt"));
            jos.write("Test content".getBytes());
            jos.closeEntry();
        }
    }

    private void deleteRecursively(Path path) throws IOException {
        if (Files.isDirectory(path)) {
            try (DirectoryStream<Path> entries = Files.newDirectoryStream(path)) {
                for (Path entry : entries) {
                    deleteRecursively(entry);
                }
            }
        }
        Files.delete(path);
    }

    @Test
    public void testCreateBackup() throws IOException {
        assertTrue("La création du backup devrait réussir", manager.createBackup());
        
        // Vérifie que le backup existe
        Path backupDir = outputDir.resolve("backups");
        assertTrue("Le dossier backup devrait exister", Files.exists(backupDir));
        
        try (DirectoryStream<Path> backups = Files.newDirectoryStream(backupDir)) {
            boolean found = false;
            for (Path backup : backups) {
                if (backup.toString().contains(testJar.getFileName().toString())) {
                    found = true;
                    break;
                }
            }
            assertTrue("Le fichier backup devrait exister", found);
        }
    }

    @Test
    public void testCalculateHash() throws Exception {
        // Crée un fichier test avec un contenu connu
        Path testFile = tempDir.resolve("hash_test.txt");
        String content = "Test content for hash";
        Files.write(testFile, content.getBytes());
        
        String hash1 = manager.calculateHash(testFile);
        assertNotNull("Le hash ne devrait pas être null", hash1);
        
        // Vérifie que le même contenu donne le même hash
        String hash2 = manager.calculateHash(testFile);
        assertEquals("Le même contenu devrait donner le même hash", hash1, hash2);
        
        // Vérifie qu'un contenu différent donne un hash différent
        Files.write(testFile, "Different content".getBytes());
        String hash3 = manager.calculateHash(testFile);
        assertNotEquals("Un contenu différent devrait donner un hash différent", hash1, hash3);
    }
}
