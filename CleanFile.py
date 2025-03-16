import re

def nettoyer_texte(texte):
    
    return re.sub(r'[^a-z]', '', texte.lower())

