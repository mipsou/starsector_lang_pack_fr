import re

def convert_guillemets(text):
    # Remplace les guillemets anglais par des guillemets français en respectant l'imbrication
    count = 0
    def replacer(match):
        nonlocal count
        count += 1
        return "«\u00A0" if count % 2 == 1 else "\u00A0»"
    
    text = re.sub(r'"', replacer, text)
    
    # Remplace les guillemets imbriqués (2ème niveau) par ‹ ›
    count = 0
    def replacer_nested(match):
        nonlocal count
        count += 1
        return "‹\u00A0" if count % 2 == 1 else "\u00A0›"
    
    text = re.sub(r'«\u00A0([^«»]*?)"([^«»]*?)"', lambda m: f'«\u00A0{m.group(1)}‹\u00A0{m.group(2)}\u00A0›', text)
    
    return text

if __name__ == "__main__":
    # Tests
    tests = [
        'Il a dit : "Ce texte est un exemple avec "guillemets" imbriqués."',
        'Test avec "plusieurs" "guillemets"',
        'Test avec "citation et "sous-citation" imbriquée"'
    ]
    
    for test in tests:
        print(f"Input:  {test}")
        print(f"Output: {convert_guillemets(test)}\n")
