import json
import time
  

class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.enfants = {}

    def to_dict(self): return [self.valeur, {k: e.to_dict() for k, e in self.enfants.items()}] if self.enfants else self.valeur

class ArbreSuffixes:
    def __init__(self, texte):
        self.texte = texte + "$"
        self.racine = Noeud('')
        self.temps_construction = self.construire_arbre()

    def inserer_suffixe(self, suffixe):
        noeud_actu = self.racine
        for cc in suffixe:
            if cc not in noeud_actu.enfants:
                noeud_actu.enfants[cc] = Noeud(cc)
            noeud_actu = noeud_actu.enfants[cc]

    def construire_arbre(self):
        debut = time.time()
        for i in range(len(self.texte)):
            self.inserer_suffixe(self.texte[i:])
        fin = time.time()
        return fin - debut

    def contient_suffixe(self,suffixe):
        noeud_c= self.racine
        for cc in suffixe:
            
            if cc not in noeud_c.enfants:
                
                return False
            noeud_c=noeud_c.enfants[cc]
        return True

    def to_json(self):
        return json.dumps(self.racine.to_dict(), indent=1)

if __name__ == "__main__":
    with open("miserables_short.txt", "r", encoding="utf-8") as fichier:
        texte_brut = fichier.read()

  
    arbre = ArbreSuffixes(texte_brut)
    print("Temps de construction de l'arbre: ",arbre.temps_construction, "secondes")

    with open('arbre_suffixes.json', 'w', encoding='utf-8') as f:
        f.write(arbre.to_json())

    print("L'arbre des suffixes a été généré et sauvegardé dans 'arbre_suffixes.json'.")

    with open('arbre_suffixes.json', 'r', encoding='utf-8') as f:
        arbre_json = json.load(f)

   
    print(arbre.contient_suffixe("theprojectgutenbergliterary$"))
