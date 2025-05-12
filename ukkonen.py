import json
import time

class Noeud:
    def __init__(self, start, end):
        self.children = {}
        self.start = start
        self.end = end
        self.suffix_link = None
        self.index = -1
    
    def to_dict(self, text):
      
        edge_label = text[self.start:self.end+1] if self.start != -1 else ""
        result = {
            "edge": edge_label,
            "suffix_index": self.index
        }
        
        if self.children:
            result["children"] = {
                c: child.to_dict(text) for c, child in self.children.items()
            }
        
        return result

class ArbreSuffixes:
    def __init__(self, text):
        self.text = text + '$'
        self.root = Noeud(-1, -1)
        self.root.suffix_link = self.root
        self.size = len(self.text)

        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0

        self.remaining = 0
        self.position = -1
        self.leaf_end = -1
        
        self.temps_construction = self.build()  # Construire l'arbre automatiquement

    def long_arrete(self, node):
        return (self.leaf_end if node.end == -1 else node.end) - node.start + 1

    def build(self):
        start_time = time.time()
        
        for i in range(self.size):
            self.position = i
            self.leaf_end = i
            self.remaining += 1

            last_new_node = None

            while self.remaining > 0:
                if self.active_length == 0:
                    self.active_edge = i

                edge_char = self.text[self.active_edge]
                if edge_char not in self.active_node.children:
                    # Règle 2 
                    self.active_node.children[edge_char] = Noeud(i, -1)

                    if last_new_node:
                        last_new_node.suffix_link = self.active_node
                        last_new_node = None
                else:
                    next_node = self.active_node.children[edge_char]
                    if self.active_length >= self.long_arrete(next_node):
                        self.active_edge += self.long_arrete(next_node)
                        self.active_length -= self.long_arrete(next_node)
                        self.active_node = next_node
                        continue

                    if self.text[next_node.start + self.active_length] == self.text[i]:
                        # Règle 1 
                        self.active_length += 1
                        if last_new_node:
                            last_new_node.suffix_link = self.active_node
                            last_new_node = None
                        break

                    # Règle 3 
                    split_end = next_node.start + self.active_length - 1
                    split_node = Noeud(next_node.start, split_end)
                    self.active_node.children[edge_char] = split_node
                    split_node.children[self.text[i]] = Noeud(i, -1)

                    next_node.start += self.active_length
                    split_node.children[self.text[next_node.start]] = next_node

                    if last_new_node:
                        last_new_node.suffix_link = split_node
                    last_new_node = split_node

                self.remaining -= 1

                if self.active_node == self.root and self.active_length > 0:
                    self.active_length -= 1
                    self.active_edge = i - self.remaining + 1
                elif self.active_node != self.root:
                    self.active_node = self.active_node.suffix_link

        self.indice_suffixe(self.root, 0)
        
        end_time = time.time()
        return end_time - start_time

    def indice_suffixe(self, node, height):
        is_leaf = True
        for child in node.children.values():
            is_leaf = False
            self.indice_suffixe(child, height + self.long_arrete(child))
        if is_leaf:
            node.index = self.size - height

    def trouve(self, pattern):
        current_node = self.root
        i = 0
        while i < len(pattern):
            c = pattern[i]
            if c not in current_node.children:
                return False
            next_node = current_node.children[c]
            j = 0
            while j < self.long_arrete(next_node) and i < len(pattern):
                if self.text[next_node.start + j] != pattern[i]:
                    return False
                i += 1
                j += 1
            current_node = next_node
        return True
    


def main():
    with open("miserables.txt", "r", encoding="utf-8") as fichier:
        texte_brut = fichier.read()
        arbre = ArbreSuffixes(texte_brut)
        print("Temps de construction de l'arbre:", arbre.temps_construction, "secondes")
        with open('arbre_suffixes_ukkonen.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(arbre.root.to_dict(arbre.text), indent=1))
        
       
        
    
      

if __name__ == "__main__":
    main()