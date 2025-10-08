nbLivres = int(input())
longueurMax = 0

for i in range(nbLivres):
    titre = input()
    if len(titre) > longueurMax:
        print(titre)
        longueurMax = len(titre)
