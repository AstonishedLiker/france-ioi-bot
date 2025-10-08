lettre = input()
nbLignes = int(input())

compteur = 0

for i in range(nbLignes):
    ligne = input()
    for caractere in ligne:
        if caractere == lettre:
            compteur += 1

print(compteur)
