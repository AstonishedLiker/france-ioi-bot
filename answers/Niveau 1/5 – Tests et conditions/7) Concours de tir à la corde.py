nbMembres = int(input())

poidsEquipe1 = 0
poidsEquipe2 = 0

for i in range(nbMembres * 2):
    poids = int(input())
    if i % 2 == 0:  # indice pair = équipe 1
        poidsEquipe1 += poids
    else:  # indice impair = équipe 2
        poidsEquipe2 += poids

if poidsEquipe1 > poidsEquipe2:
    print("L'équipe 1 a un avantage")
else:
    print("L'équipe 2 a un avantage")

print("Poids total pour l'équipe 1 :", poidsEquipe1)
print("Poids total pour l'équipe 2 :", poidsEquipe2)