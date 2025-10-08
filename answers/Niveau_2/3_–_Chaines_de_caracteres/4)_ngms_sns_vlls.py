titre = input()
auteur = input()

voyelles = "AEIOUY "

titre_sans_voyelles = ""
for caractere in titre:
    if caractere not in voyelles:
        titre_sans_voyelles += caractere

auteur_sans_voyelles = ""
for caractere in auteur:
    if caractere not in voyelles:
        auteur_sans_voyelles += caractere

print(titre_sans_voyelles)
print(auteur_sans_voyelles)
