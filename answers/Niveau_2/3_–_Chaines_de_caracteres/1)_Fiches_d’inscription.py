nbPersonnes = int(input())

for i in range(nbPersonnes):
    ligne = input().split()
    prenom = ligne[0]
    nom = ligne[1]
    print(nom, prenom)
