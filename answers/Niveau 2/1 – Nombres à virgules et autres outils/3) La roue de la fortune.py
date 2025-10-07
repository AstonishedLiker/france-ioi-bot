nbZones = int(input())

zoneFinale = nbZones % 24

if zoneFinale < 0:
    zoneFinale += 24

print(zoneFinale)