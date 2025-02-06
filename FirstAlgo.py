class Noeud:
    def __init__(self):
       
        self.enfants = {}
        self.est_fin = False
        self.mot = ""

class ArbreSuffixes:
    def __init__(self, texte):
        self.racine = Noeud()
        self.feuilles = {self.racine}
        self.suffixes = []
        
        
        for caractere in texte + "$":
            self.ajouter_caractere(caractere)
            if caractere == "$":
                
                self.suffixes = [feuille.mot for feuille in self.feuilles]
    
    def ajouter_caractere(self, caractere):
        nouvelles_feuilles = []
        
       
        nouveau_noeud = Noeud()
        
        nouveau_noeud.mot = caractere
        self.racine.enfants[caractere] = nouveau_noeud
        nouvelles_feuilles.append(nouveau_noeud)
        
      
        for feuille in self.feuilles:
            if feuille != self.racine:
                nouveau_noeud = Noeud()
                
                nouveau_noeud.mot = feuille.mot + caractere
              
                nouvelles_feuilles.append(nouveau_noeud)
        
        self.feuilles = nouvelles_feuilles
    
    def afficher_suffixes(self):
      
        for suffixe in self.suffixes:
            print(suffixe)


texte = "banana"
arbre = ArbreSuffixes(texte)
arbre.afficher_suffixes()