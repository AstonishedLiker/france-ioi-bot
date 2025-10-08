ligne = input()

resultat = ""
for caractere in ligne:
    if caractere == " ":
        resultat += "_"
    else:
        resultat += caractere

print(resultat)
