n = int(input())

for _ in range(n):
    taille = int(input())
    age = int(input())
    poids = int(input())
    a_cheval = int(input())
    cheveux_bruns = int(input())
    
    criteres_verifies = 0
    
    if 178 <= taille <= 182:
        criteres_verifies += 1
    
    if age >= 34:
        criteres_verifies += 1
    
    if poids < 70:
        criteres_verifies += 1
    
    if a_cheval == 0:
        criteres_verifies += 1
    
    if cheveux_bruns == 1:
        criteres_verifies += 1
    
    if criteres_verifies == 5:
        print("Très probable")
    elif criteres_verifies >= 3:
        print("Probable")
    elif criteres_verifies == 0:
        print("Impossible")
    else:
        print("Peu probable")