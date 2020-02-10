import sys
from ruler import Ruler


DATASET = sys.argv[1]
# L'argument envoyé par le sytème est [bundle.py, fichier.txt]

with open(DATASET, "r") as dataset:
    lignes = dataset.readlines()
    l = len(lignes)//2 # On enlève éventuellement la dernière ligne
    for i in range (l):
        bringauche = str(lignes[2*i])
        brindroit = str(lignes[2*i + 1])
        if bringauche[-1] == '\n': # on enlève les newlignes
            bringauche = bringauche[: -1]
        if brindroit[-1] == '\n' :
            brindroit = brindroit[: -1]
        ruler = Ruler(bringauche, brindroit)
        ruler.compute()
        print(f'===== example {i} - distance = {ruler.distance}')
        (a, b) = ruler.report()
        print(a)
        print(b)