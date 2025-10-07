nbMesures = int(input())
tempMin = int(input())
tempMax = int(input())

for i in range(nbMesures):
    temperature = int(input())
    if temperature < tempMin or temperature > tempMax:
        print("Alerte !!")
        break
    else:
        print("Rien à signaler")