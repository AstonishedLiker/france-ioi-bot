quantite = float(input())

nombre_sacs = int(quantite / 60)
if quantite % 60 != 0:
    nombre_sacs += 1

cout_total = nombre_sacs * 45

print(cout_total)