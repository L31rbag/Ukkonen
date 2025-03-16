import json
from CleanFile import nettoyer_texte  

class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.enfants = {}

    def to_dict(self):
        return {
            'valeur': self.valeur,
            'enfants': {key: enfant.to_dict() for key, enfant in self.enfants.items()}
        }

class ArbreSuffixes:
    def __init__(self, texte):
        self.texte = texte + "$"
        self.racine = Noeud('')
        self.construire_arbre()

    def inserer_suffixe(self, suffixe):
        noeud_actu = self.racine
        for cc in suffixe:
            if cc not in noeud_actu.enfants:
                noeud_actu.enfants[cc] = Noeud(cc)
            noeud_actu = noeud_actu.enfants[cc]

    def construire_arbre(self):
        for i in range(len(self.texte)):
            self.inserer_suffixe(self.texte[i:])

    def to_json(self):
        return json.dumps(self.racine.to_dict(), indent=2)

if __name__ == "__main__":
    with open("miserables_very_short.txt", "r", encoding="utf-8") as fichier:
        texte_brut = fichier.read()

    texte_nettoye = nettoyer_texte(texte_brut)
    arbre = ArbreSuffixes(texte_nettoye)

    with open('arbre_suffixes.json', 'w', encoding='utf-8') as f:
        f.write(arbre.to_json())

    print("L'arbre des suffixes a été généré et sauvegardé dans 'arbre_suffixes.json'.")
