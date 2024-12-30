import requests
from bs4 import BeautifulSoup
import os
import markdown
import time
import re

class ForumScraper:
    def __init__(self, base_url="https://fractalsoftworks.com/forum/"):
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        self.doc_dir = "../docs/forum"
        os.makedirs(self.doc_dir, exist_ok=True)

    def get_page(self, url):
        response = requests.get(url, headers=self.headers)
        return BeautifulSoup(response.text, 'html.parser')

    def clean_text(self, text):
        # Nettoyer le HTML et convertir en markdown
        text = re.sub(r'<br\s*/?>', '\n', text)
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()

    def parse_topic(self, url, title):
        print(f"Scraping: {title}")
        soup = self.get_page(url)
        
        # Trouver le contenu principal
        posts = soup.find_all('div', class_='post')
        
        content = []
        for post in posts:
            # Extraire le contenu du post
            post_content = post.find('div', class_='inner')
            if post_content:
                content.append(self.clean_text(str(post_content)))
        
        # Créer le fichier markdown
        filename = re.sub(r'[^\w\s-]', '', title).strip().lower()
        filename = re.sub(r'[-\s]+', '-', filename)
        
        with open(f"{self.doc_dir}/{filename}.md", 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write("\n\n".join(content))
        
        time.sleep(1)  # Respecter le serveur

    def scrape_documentation(self):
        # Liste des URLs de documentation à scraper
        docs = [
            ("https://fractalsoftworks.com/forum/index.php?topic=4760.0", "Mod Descriptor (mod_info.json)"),
            ("https://fractalsoftworks.com/forum/index.php?topic=8355.0", "Rule Scripting"),
            ("https://fractalsoftworks.com/forum/index.php?topic=7164.0", "Style Guide"),
            ("https://fractalsoftworks.com/forum/index.php?topic=15244.0", "Publishing Guide"),
            ("https://fractalsoftworks.com/forum/index.php?topic=6926.0", "Eclipse Guide"),
            ("https://fractalsoftworks.com/forum/index.php?topic=5016.0", "Modding Guide Part 2")
        ]
        
        for url, title in docs:
            self.parse_topic(url, title)

    def download_s3_docs(self):
        print("Téléchargement des documents S3...")
        s3_docs = [
            ("https://s3.amazonaws.com/fractalsoftworks/doc/StarsectorRuleScripting.pdf", "StarsectorRuleScripting.pdf"),
            ("https://s3.amazonaws.com/fractalsoftworks/doc/StarsectorRuleScripting.rtf", "StarsectorRuleScripting.rtf")
        ]
        
        docs_dir = "../docs/s3"
        os.makedirs(docs_dir, exist_ok=True)
        
        for url, filename in s3_docs:
            print(f"Téléchargement de {filename}")
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                with open(f"{docs_dir}/{filename}", 'wb') as f:
                    f.write(response.content)
                print(f"Sauvegardé dans {docs_dir}/{filename}")
            else:
                print(f"Erreur lors du téléchargement de {filename}: {response.status_code}")
            time.sleep(1)

if __name__ == "__main__":
    scraper = ForumScraper()
    scraper.scrape_documentation()
    scraper.download_s3_docs()
