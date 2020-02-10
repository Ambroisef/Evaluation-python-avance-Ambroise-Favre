import numpy as np
from colorama import Fore, Style

def representation_intermediaire(chainef1, chainef2):
    """fonction qui servira à la représentation des brins, de façon récursive"""
    if chainef1 == '':
        return (('', ''))
    c1 = ''
    c2 = ''
    a = chainef1[0]
    b = chainef2[0]
    if a == '-':
        c1 = f'{red_text(a)}'
        c2 = b
    elif b == '-':
        c1 = a
        c2 = f'{red_text(b)}'
    else:
        if a == b:
            c1 = a
            c2 = b
        else:
            c1 = a
            c2 = f'{red_text(b)}'
    (d1, d2) = representation_intermediaire(chainef1[1:], chainef2[1:])
    c1 = c1 + d1
    c2 = c2 + d2
    return (c1, c2)

def red_text(text):
    """fonction permettant d'écrire en rouge"""
    return f"{Fore.RED}{text}{Style.RESET_ALL}"


class Ruler:

    def  __init__(self, chaine1, chaine2): 
        self.chaines_initiales = (chaine1, chaine2)
    
    def compute(self, cout_substitution = 1, cout_ins_sup = 1):
        """fonction qui définie la distance, et qui créer la matrice et les chaines modifiées.
        On se donne la possibilité de modifier les différents coûts.
        On pourrait imaginer, en amélioration, 
        un cout de substitution, d'insertion, ou de suppression qui dépendrait des caractères"""
        (chaine1, chaine2) = self.chaines_initiales
        l1 = len(chaine1)
        l2 = len(chaine2)
        # création de la matrice
        d = np.zeros((l1+1, l2+1))
        for i in range (1, l1+1):
            d[i, 0] = i
        for j in range (1, l2+1):
            d[0, j] = j
        for i in range (0, l1):
            for j in range (0, l2):
                if chaine1[i] == chaine2[j] :
                    cout_sub = 0
                else :
                    cout_sub = cout_substitution
                d[i+1, j+1] = min(d[i, j+1] + cout_ins_sup, d[i+1, j] + cout_ins_sup, d[i, j] + cout_sub)
                # On construit la matrice de proche en proche, en prenant à 
                # chaque fois le minimum des couts des trois possibilités : substitution, suppression ou insertion.

                # On remarquera qu'une supression dans un brin est exactement la même chose, en terme de distance,
                # qu'une insertion dans l'autre brin : on privilégiera l'insertion
                # dans la construction des chaines finales.
        self.matrice = d 
        self.distance = d[l1, l2]

        # construction des chaines finales
        chainef1 = ''
        chainef2 = ''
        (i, j) = d.shape
        i = i-1
        j = j-1
        while (i > 0 and j > 0):
            score = d[i, j]
            score_diag = d[i-1, j-1]
            score_up = d[i, j-1]
            score_left = d[i-1, j]
            x1 = chaine1[i-1]
            x2 = chaine2[j-1]
            # On va déterminer le chemin minimisant la distance.
            if x1==x2:
                cout_sub = 0
            else: 
                cout_sub = cout_substitution
            if score == score_diag + cout_sub:
                chainef1 = x1 + chainef1
                chainef2 = x2 + chainef2
                j = j-1
                i = i-1
            elif score == score_left + cout_ins_sup:
                chainef1 = x1 + chainef1
                chainef2 = '-' + chainef2
                i = i-1
            else:
                chainef1 = '-' + chainef1
                chainef2 = x2 + chainef2
                j = j-1
        # On a parcouru entièrement un des brins, on va finir le travail avec des insertions 
        # pour avoir des chaines finales de même longueur.     
        while i >= 0 and j > 0:
            chainef1 = chaine1[i] + chainef1
            chainef2 = '-' + chainef2
            i = i - 1
        while j >= 0 and i > 0:
            chainef2 = chaine2[j] + chainef2
            chainef1 = '-' + chainef1
            j = j - 1
        self.chaines_finales = (chainef1, chainef2)

    def report(self):
        """renvoie les deux chaines finales, avec l'écriture en rouge"""
        (chainef1, chainef2) = self.chaines_finales
        (c1, c2) = representation_intermediaire(chainef1, chainef2)
        return (c1, c2)





    










