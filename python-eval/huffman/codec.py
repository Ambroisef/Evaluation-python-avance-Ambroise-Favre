def coefficients(chaine): 
    """renvoie une liste de tuples avec les caractères et leur poids, dans l'ordre décroissant"""
    dic = {}
    for x in chaine :
        if x not in dic.keys() : 
            dic[x] = 1
        else : 
            dic[x] = dic[x] + 1
    liste = sorted(dic.items(), key = lambda t: t[1]) 
    liste.reverse()
    return (liste)



class noeud:
        def __init__(self, dessous, chaine):
            self.chaine = chaine
            self.noeuds_engendres = dessous
            # Un noeud contient donc sa chaine, et les noeuds qu'il engendre.
            # La liste est vide s'il s'agit d'une feuille.            
        def __repr__(self):
            return(self.chaine) # Il s'agit uniquement d'une aide à la construction du code.



class TreeBuilder:

    def __init__(self, chaine): 
        self.chaine = chaine
        self.coefs = coefficients(chaine)

    def tree(self):
        """construit l'arbre"""
        ensemble_noeuds = []
        liste = self.coefs
        while len(liste) > 1:
            b = liste.pop()
            a = liste.pop()
            x1 = a[0]
            y1 = a[1]
            x2 = b[0]
            y2 = b[1]
            noeud_en_dessous1 = 0
            noeud_en_dessous2 = 0
            
            for x in ensemble_noeuds :
                chaine = x.chaine
                if chaine == x1 :
                    noeud_en_dessous1 = x
                if chaine == x2 :
                    noeud_en_dessous2 = x
            # On enregistre ici les noeuds, déjà créés car
            # on construit l'arbre par le bas
            # qui seront engendrés par celui dont la chaine sera x1 + x2.
            # 
            # Dans les lignes suivantes, on construit les noeuds, en fonction 
            # des possibles noeuds engendrés               
            if noeud_en_dessous1 == 0 and noeud_en_dessous2 != 0: 
                na = noeud([], x1)
                n = noeud([noeud_en_dessous2] + [na], x1 + x2)
                ensemble_noeuds.append(na)
                ensemble_noeuds.append(n)
            elif noeud_en_dessous2 == 0 and noeud_en_dessous1 != 0: 
                nb = noeud([], x2)
                n = noeud([noeud_en_dessous1] + [nb], x1 + x2)
                ensemble_noeuds.append(nb)
                ensemble_noeuds.append(n)
            elif noeud_en_dessous2 == 0 and noeud_en_dessous1 == 0: 
                na = noeud([], x1)
                nb = noeud([], x2)
                n = noeud([na, nb], x1 + x2)
                ensemble_noeuds.append(na)
                ensemble_noeuds.append(nb)
                ensemble_noeuds.append(n)
            else :
                n = noeud ([noeud_en_dessous1, noeud_en_dessous2], x1 + x2)
                ensemble_noeuds.append(n)

            # Ici, on va rajouter le nouvel élément, correspondant au noeud créé,
            # au bon endroit (la liste est triée) dans la liste
            b = True
            i=0
            l=len(liste)
            while b and i < l : 
                c1 = liste[i][1]
                if c1 <= y1 + y2 :
                    liste = liste [:i] + [(x1 + x2, y1 + y2)] + liste [i:]
                    b = False
                i=i+1                  
        self.liste_noeuds = ensemble_noeuds
            

class Codec:
    def __init__(self, tree):
        self.liste_noeuds = tree.liste_noeuds
           
    def encode(self, chaine): 
        """permet de coder chaine en binaire, avec l'arbre avec lequel on a construit self"""
        code = ''
        liste_noeuds = self.liste_noeuds
        for x in chaine:
            b = True 
            noeud_act = liste_noeuds[-1] # On commence toujours par le sommet
            # qui se situe à la fin de la liste des noeuds
            # 
            # L'algorithme se place sur noeud_act, 
            # et parcourt les noeuds engendrés (noeuds_suivants)
            # pour descendre dans l'arbre, en choisissant le bon coté 
            while b:
                noeuds_suivants = noeud_act.noeuds_engendres
                for (i, y) in enumerate(noeuds_suivants):
                    if x in y.chaine:
                        code = code + f'{i}'
                        if x == y.chaine:
                            b = False
                            break
                        else:
                            noeud_act = y
        return (code)

    def decode(self, code):
        """permet de décoder code, avec l'arbre avec lequel on a construit self"""
        code1 = code[:] # On travaille sur une copie
        chainef = ''
        liste_noeuds = self.liste_noeuds
        noeud_act = liste_noeuds[-1] # De même on part toujours du haut du graphe 
        while code1 != '':
            bit = code1[0]
            noeuds_suivants = noeud_act.noeuds_engendres
            if noeuds_suivants == []: # On est sur une feuille 
                chainef = chainef + noeud_act.chaine
                noeud_act = liste_noeuds[-1] # On est arrivé au bout d'une branche, et on revient en haut
            else:
                noeud_act = noeuds_suivants[int(bit)]
                code1 = code1[1:]

        chainef = chainef + noeud_act.chaine # On rajoute le dernier caractère

            
        return (chainef)



chaine_caractere = 'paris est une tres belle ville avec de tres beaux monuments'
tree_builder = TreeBuilder(chaine_caractere)
tree_builder.tree()
codec=Codec(tree_builder)
code = codec.encode(chaine_caractere)
texte = codec.decode(code)
print(texte)