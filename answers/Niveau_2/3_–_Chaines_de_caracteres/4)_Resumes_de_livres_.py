nbLivres = int(input())
longueurMinimale = int(input())

for i in range(nbLivres):
    titre = input()
    resume = input()
    if len(resume) < longueurMinimale:
        print(titre)
