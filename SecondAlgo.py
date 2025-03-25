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
        if not suffixe: #verif suffixe vide
            return
            
        noeud_actu = self.racine
        i = 0
        
       
        while i < len(suffixe):
            premier_caractere = suffixe[i]
            
           #ajout nouveau neoud si existe pas prem cara
            if premier_caractere not in noeud_actu.enfants:
                noeud_actu.enfants[premier_caractere] = Noeud(suffixe[i:])
                return
            
           
            enfant = noeud_actu.enfants[premier_caractere]
            valeur_enfant = enfant.valeur
            
            #trouver long prefixe commun
            j = 0
            while i + j < len(suffixe) and j < len(valeur_enfant) and suffixe[i + j] == valeur_enfant[j]:
                j += 1
            
            
            if j < len(valeur_enfant):
                #partie pas commun
                nouveau_noeud = Noeud(valeur_enfant[j:])
                nouveau_noeud.enfants = enfant.enfants
                
                #modif existant pour contenir que partie correspond
                enfant.valeur = valeur_enfant[:j]
                enfant.enfants = {nouveau_noeud.valeur[0]: nouveau_noeud}
                
                #transfert reste
                if i + j < len(suffixe):
                    enfant.enfants[suffixe[i + j]] = Noeud(suffixe[i + j:])
                
                return
            
            
            i += len(valeur_enfant)
            noeud_actu = enfant
    
    def construire_arbre(self):
        for i in range(len(self.texte)):
            self.inserer_suffixe(self.texte[i:])

    def contient_suffixe(self,suffixe):
        noeud_c= self.racine
        for cc in suffixe:
            print(f"Recherche du caractère: {cc}")
            if cc not in noeud_c.enfants:
                print(f"Suffixe non trouvé à {cc}")
                return False
            noeud_c=noeud_c.enfants[cc]
        return True

    
    def to_json(self):
        return json.dumps(self.racine.to_dict(), indent=2)

if __name__ == "__main__":
    with open("miserables_very_short.txt", "r", encoding="utf-8") as fichier:
        texte_brut = fichier.read()
    
    texte_nettoye = nettoyer_texte(texte_brut)
    arbre = ArbreSuffixes(texte_nettoye)
    
    
    with open('arbre_suffixes2.json', 'w', encoding='utf-8') as f:
        f.write(arbre.to_json())
    
    print("L'arbre des suffixes compressé a été généré et sauvegardé dans 'arbre_suffixes.json'.")



    with open('arbre_suffixes2.json', 'r', encoding='utf-8') as f:
        arbre_json = json.load(f)

   
    print(arbre.contient_suffixe("theprojectgutenbergliterary$"))

    


