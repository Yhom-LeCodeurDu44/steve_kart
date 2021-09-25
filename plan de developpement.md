# Liste des développements
[x] Réduire la taille du kart
[x] kart va en diagonale
[x] position inchangée si on touche à rien
[x] position inchangée si on touche directions opposées en même temps
[ ] limite des bords
[ ] utilisation joystick
[ ] passage secret dans bords

# Notes #
## Détection des bords
Notes sur les détection de collisions
2 approches
- soit utiliser soit des formes géométriques pour délimiter la piste (rectangles) et détecter que le kart ne touche aucun de ces rectangles
- soit utiliser une détection de masque au pixel près

Dans les 2 cas, des méthodes sont fournies par pygame
Détection au pixel près
1. utiliser une image de piste où la piste est sans couleur (utiliser la couleur invisible tel que définie dans le programme)
2. créer un masque au pixel près de cette piste. La piste, de couleur invisible, sera exclue du masque, on aura donc un masque de "hors piste" (tout sauf la piste).
```python
masque_hors_piste = pygame.mask.from_surface( __lapisteinvisible__ )
```
3pour détecter un hors piste: détecter lorsque le masque du kart touche le masque de hors piste à une position choisie, et là... faire ce qu'on veut que ça fasse
```python
masque_hors_piste.overlap( masque_kart, positiondukart )
# -> Vrai si collision, faux si pas de collision
```
