paquet1 = input()
paquet2 = input()

nbEgalites = 0
i = 0

while i < len(paquet1) and i < len(paquet2):
    if paquet1[i] == paquet2[i]:
        nbEgalites += 1
        i += 1
    else:
        if paquet1[i] < paquet2[i]:
            print(1)
        else:
            print(2)
        print(nbEgalites)
        exit()

if len(paquet1) == len(paquet2):
    print("=")
elif len(paquet1) > len(paquet2):
    print(1)
else:
    print(2)

print(nbEgalites)
