ancienne_taxe = float(input())
nouvelle_taxe = float(input())
prix_actuel = float(input())

prix_hors_taxe = prix_actuel / (1 + ancienne_taxe / 100)
nouveau_prix = prix_hors_taxe * (1 + nouvelle_taxe / 100)
nouveau_prix_arrondi = round(nouveau_prix, 2)

print(nouveau_prix_arrondi)