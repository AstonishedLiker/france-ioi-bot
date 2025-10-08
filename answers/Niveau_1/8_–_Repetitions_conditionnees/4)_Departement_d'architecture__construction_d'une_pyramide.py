nbPierresMax = int(input())

hauteur = 0
pierresUtilisees = 0

while True:
    hauteur += 1
    pierresNiveau = hauteur * hauteur
    if pierresUtilisees + pierresNiveau <= nbPierresMax:
        pierresUtilisees += pierresNiveau
    else:
        hauteur -= 1
        break

print(hauteur)
print(pierresUtilisees)