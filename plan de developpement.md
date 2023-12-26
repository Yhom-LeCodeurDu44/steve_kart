# Liste des développements
[x] Réduire la taille du kart
[x] kart va en diagonale
[x] position inchangée si on touche à rien
[x] position inchangée si on touche directions opposées en même temps
[x] limite des bords
[x] passage secret dans bords
[x] ajout d'un second kart
[x] touche de reload
[ ] faire un beau circuit
[ ] lignes infranchissables
[ ] utilisation joystick
[ ] compteur de tour + chrono (4 tours)
[ ] si reload apparaitre sur checkpoint
[ ] Checkpoint
[ ] Choisir Player1/2
*
# Notes #
## Détection des bords
Notes sur les détection de collisions
2 approches
- utiliser des formes géométriques pour délimiter la piste et le kart
- ou utiliser une détection de masque au pixel près

Dans les 2 cas, des méthodes sont fournies par pygame
 
### Détection par forme géométrique 
- utiliser soit des formes géométriques pour délimiter la piste, comme des rectangles, triangles, etc, et détecter que le kart ne touche aucun de ces rectangles


### Détection au pixel près
1. utiliser une image de piste où la piste est sans couleur (utiliser la couleur invisible tel que définie dans le programme)
2. créer un masque au pixel près de cette piste. La piste, sans couleur, sera exclue du masque, on aura donc un masque du reste, le "hors piste" (tout sauf la piste).
```python
masque_hors_piste = pygame.mask.from_surface( __lapisteinvisible__ )
```
3pour détecter un hors piste: détecter lorsque le masque du kart touche le masque de hors piste à une position choisie, et là... faire ce qu'on veut que ça fasse
```python
masque_hors_piste.overlap( masque_kart, positiondukart )
# -> Vrai si collision, faux si pas de collision
```

## Détection de la progression sur la piste

Méthode retenue: 
1. Délimiter des secteurs de piste
2. Détecter les changements de secteur par masque ou utiliser une carte des secteurs (image colorée mais non affichée)
3. Le passage de tour est lorsqu’on passe du dernier secteur au premier secteur
4. Détection des retours arrière: lorsqu’on revient du premier au dernier secteur on « annule » la progression
5. Option: quand on sort de piste on est ramené à un point de référence du précédent secteur 