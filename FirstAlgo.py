import json
class Noeud:
    def __init__(self,valeur):
        self.valeur = valeur
        self.enfants = {}

    def to_dict(self):
        return{
            'valeur': self.valeur,
            'enfants':{key : enfant.to_dict() for key, enfant in self.enfants.items()}
        }
        
        

class ArbreSuffixes:
    def __init__(self, texte):
        
        self.texte = texte + "$"
        self.racine = Noeud('')
        self.construire_arbre()
       
    def inserer_suffixe(self,suffixe):
        noeud_actu = self.racine
        print(suffixe)
        for cc in suffixe :
            if cc not in noeud_actu.enfants :
                noeud_actu.enfants[cc]  = Noeud(cc)
            noeud_actu = noeud_actu.enfants[cc]
            
    
    def construire_arbre(self):

        for i in range(len(self.texte)):
            self.inserer_suffixe(self.texte[i:])



    def to_json(self):  
        return json.dumps(self.racine.to_dict(),indent=2)
        
    
  
    
   


texte = "banane"
arbre = ArbreSuffixes(texte)
print(arbre.to_json())

with open('arbre_suffixes.json', 'w', encoding='utf-8') as f:
    f.write(arbre.to_json())