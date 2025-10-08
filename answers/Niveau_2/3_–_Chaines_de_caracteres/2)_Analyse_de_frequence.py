nbLignes, nbMots = map(int, input().split())

compteur = {}

for i in range(nbLignes):
    mots = input().split()
    for mot in mots:
        longueur = len(mot)
        if longueur in compteur:
            compteur[longueur] += 1
        else:
            compteur[longueur] = 1

for longueur in sorted(compteur.keys()):
    print(longueur, ":", compteur[longueur])
