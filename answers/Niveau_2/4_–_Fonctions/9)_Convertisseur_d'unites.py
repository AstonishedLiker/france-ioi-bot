nbConversions = int(input())

METRES_PAR_PIED = 0.3048
GRAMMES_PAR_LIVRE = 0.002205

for i in range(nbConversions):
    ligne = input().split()
    valeur = float(ligne[0])
    unite = ligne[1]
    
    if unite == 'm':
        resultat = valeur / METRES_PAR_PIED
        print(resultat, 'p')
    elif unite == 'g':
        resultat = valeur * GRAMMES_PAR_LIVRE
        print(resultat, 'l')
    elif unite == 'c':
        resultat = 32 + 1.8 * valeur
        print(resultat, 'f')