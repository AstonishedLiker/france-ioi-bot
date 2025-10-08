population = int(input())

jour = 1
malades = 1

while malades < population:
    jour += 1
    nouveauxMalades = malades * 2
    malades += nouveauxMalades

print(jour)