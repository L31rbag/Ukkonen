import os
import time
import matplotlib.pyplot as plt
from FirstAlgo import ArbreSuffixes as ArbreSuffixesSimple
from SecondAlgo import ArbreSuffixes as ArbreSuffixesCompresse


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
taille_simple = []
taille_compresse = []


for i in range(nb_echantillons):
   
    taille = int(taille_max * (i + 1) / nb_echantillons)
    tailles_echantillons.append(taille)
    
 
    texte = texte_complet[:taille]
    
    print(f"Test {i+1}/{nb_echantillons} - Taille: {taille} caractères")
    
    
    arbre_simple = ArbreSuffixesSimple(texte)
    temps_simple.append(arbre_simple.temps_construction)
    
    
    nom_fichier_simple = os.path.join(dossier_benchmark, f"simple_{i+1}.json")
    fichier = open(nom_fichier_simple, 'w', encoding='utf-8')
    fichier.write(arbre_simple.to_json())
    fichier.close()
    taille_simple.append(os.path.getsize(nom_fichier_simple))
    
   
    arbre_compresse = ArbreSuffixesCompresse(texte)
    temps_compresse.append(arbre_compresse.temps_construction)
    
    
    nom_fichier_compresse = os.path.join(dossier_benchmark, f"compresse_{i+1}.json")
    fichier = open(nom_fichier_compresse, 'w', encoding='utf-8')
    fichier.write(arbre_compresse.to_json())
    fichier.close()
    taille_compresse.append(os.path.getsize(nom_fichier_compresse))


print("\nRésultats du benchmark:")
print("Taille texte | Temps simple | Temps compressé | Taille simple | Taille compressé")
print("-" * 80)

for i in range(nb_echantillons):
    print(f"{tailles_echantillons[i]} | {temps_simple[i]:.6f}s | {temps_compresse[i]:.6f}s | {taille_simple[i]} | {taille_compresse[i]}")


print("\nComparaison performance:")
for i in range(nb_echantillons):
    if temps_simple[i] > 0:
        diff_temps = ((temps_simple[i] / temps_compresse[i]) - 1) * 100
    else:
        diff_temps = float('inf')
    
    if taille_simple[i] > 0:
        diff_taille = ((taille_simple[i] / taille_compresse[i]) - 1) * 100
    else:
        diff_taille = float('inf')
    
    print(f"{tailles_echantillons[i]} | Temps: {diff_temps:+.2f}% | Taille: {diff_taille:+.2f}%")


plt.figure(figsize=(12, 15))



# graphe temps log
plt.subplot(3, 1, 2)
plt.plot(tailles_echantillons, temps_simple, 'o-', label='Arbre simple (FirstAlgo)')
plt.plot(tailles_echantillons, temps_compresse, 's-', label='Arbre compressé (SecondAlgo)')
plt.xlabel('Taille du texte (caractères)')
plt.ylabel('Temps (secondes)')
plt.title('Temps de construction - Échelle logarithmique')
plt.yscale('log') 
plt.legend()
plt.grid(True)

# graph taille log
plt.subplot(3, 1, 3)
plt.plot(tailles_echantillons, taille_simple, 'o-', label='Arbre simple (FirstAlgo)')
plt.plot(tailles_echantillons, taille_compresse, 's-', label='Arbre compressé (SecondAlgo)')
plt.xlabel('Taille du texte (caractères)')
plt.ylabel('Taille fichier (octets)')
plt.title('Taille des fichiers JSON - Échelle logarithmique')
plt.yscale('log')  
plt.legend()
plt.grid(True)

plt.tight_layout()
chemin_graphique = os.path.join(dossier_benchmark, 'resultats.png')
plt.savefig(chemin_graphique)
print(f"\nGraphiques sauvegardés dans '{chemin_graphique}'")