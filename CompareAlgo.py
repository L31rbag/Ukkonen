import os
import time
import gzip
import matplotlib.pyplot as plt
from FirstAlgo import ArbreSuffixes as ArbreSuffixesSimple
from SecondAlgo import ArbreSuffixes as ArbreSuffixesCompresse
from ukkonen import ArbreSuffixes as ArbreSuffixesUkkonen

dossier_benchmark = "benchmark"
if not os.path.exists(dossier_benchmark):
    os.mkdir(dossier_benchmark)

fichier_texte = "miserables_short.txt"
fichier = open(fichier_texte, "r", encoding="utf-8")
texte_complet = fichier.read()
fichier.close()

nb_echantillons = 5
taille_max = len(texte_complet)

tailles_echantillons = []
temps_simple = []
temps_compresse = []
temps_ukkonen = []
taille_simple = []
taille_compresse = []
taille_ukkonen = []

def compresser_fichier(chemin_fichier):
  
    with open(chemin_fichier, 'rb') as f_in:
        contenu = f_in.read()
        
 
    contenu_compresse = gzip.compress(contenu)
    
 
    return len(contenu_compresse) / (1024 * 1024)

for i in range(nb_echantillons):
    taille = int(taille_max * (i + 1) / nb_echantillons)
    tailles_echantillons.append(taille)
    
    texte = texte_complet[:taille]
    
    print(f"Test {i+1}/{nb_echantillons} - Taille: {taille} caractères")
    
    # Benchmark de FirstAlgo (Simple)
    arbre_simple = ArbreSuffixesSimple(texte)
 
    temps_simple.append(arbre_simple.temps_construction * 1000)
    
    nom_fichier_simple = os.path.join(dossier_benchmark, f"simple_{i+1}.json")
    fichier = open(nom_fichier_simple, 'w', encoding='utf-8')
    fichier.write(arbre_simple.to_json())
    fichier.close()
    taille_simple.append(compresser_fichier(nom_fichier_simple))
    
    # Benchmark de SecondAlgo (Compressé)
    arbre_compresse = ArbreSuffixesCompresse(texte)
  
    temps_compresse.append(arbre_compresse.temps_construction * 1000)
    
    nom_fichier_compresse = os.path.join(dossier_benchmark, f"compresse_{i+1}.json")
    fichier = open(nom_fichier_compresse, 'w', encoding='utf-8')
    fichier.write(arbre_compresse.to_json())
    fichier.close()
    taille_compresse.append(compresser_fichier(nom_fichier_compresse))
    
    # Benchmark de Ukkonen
    arbre_ukkonen = ArbreSuffixesUkkonen(texte)
 
    temps_ukkonen.append(arbre_ukkonen.temps_construction * 1000)
    
    nom_fichier_ukkonen = os.path.join(dossier_benchmark, f"ukkonen_{i+1}.json")
    fichier = open(nom_fichier_ukkonen, 'w', encoding='utf-8')
    fichier.write(arbre_ukkonen.to_json())
    fichier.close()
    taille_ukkonen.append(compresser_fichier(nom_fichier_ukkonen))

plt.figure(figsize=(10, 6))
plt.plot(tailles_echantillons, temps_simple, 'o-', color='blue', linewidth=2)
plt.xlabel('Taille du texte (caractères)')
plt.ylabel('Temps (millisecondes)')
plt.title('Temps de construction - Arbre simple (FirstAlgo)')
plt.grid(True)
plt.tight_layout()
chemin_graphique_temps_simple = os.path.join(dossier_benchmark, 'temps_simple.png')
plt.savefig(chemin_graphique_temps_simple)

plt.figure(figsize=(10, 6))
plt.plot(tailles_echantillons, temps_compresse, 's-', color='green', linewidth=2)
plt.xlabel('Taille du texte (caractères)')
plt.ylabel('Temps (millisecondes)')
plt.title('Temps de construction - Arbre compressé (SecondAlgo)')
plt.grid(True)
plt.tight_layout()
chemin_graphique_temps_compresse = os.path.join(dossier_benchmark, 'temps_compresse.png')
plt.savefig(chemin_graphique_temps_compresse)

plt.figure(figsize=(10, 6))
plt.plot(tailles_echantillons, temps_ukkonen, '^-', color='red', linewidth=2)
plt.xlabel('Taille du texte (caractères)')
plt.ylabel('Temps (millisecondes)')
plt.title('Temps de construction - Algorithme de Ukkonen')
plt.grid(True)
plt.tight_layout()
chemin_graphique_temps_ukkonen = os.path.join(dossier_benchmark, 'temps_ukkonen.png')
plt.savefig(chemin_graphique_temps_ukkonen)


plt.figure(figsize=(10, 6))
plt.plot(tailles_echantillons, taille_simple, 'o-', color='blue', linewidth=2)
plt.xlabel('Taille du texte (caractères)')
plt.ylabel('Taille fichier compressé (Mo)')
plt.title('Taille des fichiers JSON compressés - Arbre simple (FirstAlgo)')
plt.grid(True)
plt.tight_layout()
chemin_graphique_taille_simple = os.path.join(dossier_benchmark, 'taille_simple.png')
plt.savefig(chemin_graphique_taille_simple)

plt.figure(figsize=(10, 6))
plt.plot(tailles_echantillons, taille_compresse, 's-', color='green', linewidth=2)
plt.xlabel('Taille du texte (caractères)')
plt.ylabel('Taille fichier compressé (Mo)')
plt.title('Taille des fichiers JSON compressés - Arbre compressé (SecondAlgo)')
plt.grid(True)
plt.tight_layout()
chemin_graphique_taille_compresse = os.path.join(dossier_benchmark, 'taille_compresse.png')
plt.savefig(chemin_graphique_taille_compresse)

plt.figure(figsize=(10, 6))
plt.plot(tailles_echantillons, taille_ukkonen, '^-', color='red', linewidth=2)
plt.xlabel('Taille du texte (caractères)')
plt.ylabel('Taille fichier compressé (Mo)')
plt.title('Taille des fichiers JSON compressés - Algorithme de Ukkonen')
plt.grid(True)
plt.tight_layout()
chemin_graphique_taille_ukkonen = os.path.join(dossier_benchmark, 'taille_ukkonen.png')
plt.savefig(chemin_graphique_taille_ukkonen)





