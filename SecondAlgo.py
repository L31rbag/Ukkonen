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
        debut = time.time()
        for i in range(len(self.texte)):
            self.inserer_suffixe(self.texte[i:])
        fin = time.time()
        return fin - debut

    def contient_suffixe(self, suffixe):
        noeud_actu = self.racine
        i = 0
        
        while i < len(suffixe):
            trouve = False
            
            for caractere, enfant in noeud_actu.enfants.items():
                valeur_enfant = enfant.valeur
                
            
                if suffixe[i] == valeur_enfant[0]:
                    
                    j = 0
                    while (i + j < len(suffixe) and 
                        j < len(valeur_enfant) and 
                        suffixe[i + j] == valeur_enfant[j]):
                        j += 1
                    
                
                    if j < len(valeur_enfant):
                        return False
                    
                    
                    i += j
                    noeud_actu = enfant
                    trouve = True
                    break
            
            
            if not trouve:
                return False
        
        return True

    
    def to_json(self):
        return json.dumps(self.racine.to_dict(), indent=1)

if __name__ == "__main__":
    with open("miserables_very_short.txt", "r", encoding="utf-8") as fichier:
        texte_brut = fichier.read()
    
 
    arbre = ArbreSuffixes(texte_brut)
    
    print("Temps de construction de l'arbre: ",arbre.temps_construction, "secondes")
    with open('arbre_suffixes2.json', 'w', encoding='utf-8') as f:
        f.write(arbre.to_json())
    
    print("L'arbre des suffixes compressé a été généré et sauvegardé dans 'arbre_suffixes.json'.")



    with open('arbre_suffixes2.json', 'r', encoding='utf-8') as f:
        arbre_json = json.load(f)

   
    print(arbre.contient_suffixe("theprojectgutenbergliterary$"))

    


