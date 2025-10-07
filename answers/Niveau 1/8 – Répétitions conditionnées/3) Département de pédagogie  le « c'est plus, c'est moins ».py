nombreSecret = int(input())
nbEssais = 0

while True:
    proposition = int(input())
    nbEssais += 1
    
    if proposition < nombreSecret:
        print("c'est plus")
    elif proposition > nombreSecret:
        print("c'est moins")
    else:
        break

print("Nombre d'essais nécessaires :")
print(nbEssais)