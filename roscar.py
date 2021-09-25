import pygame
from pygame.sprite import Sprite, Rect

pygame.init()

# mettre à la bonne taille
TAILLE_ECRAN = (768, 768)
screen = pygame.display.set_mode(TAILLE_ECRAN)
MALIBU = (140, 198, 255)
DEMARRAGE_KART = (145, 637)
TAILLE_KART = 20
VITESSE = 4
kart_images = {
    (0, -1): "resources/steve_kart_dos.png",
    (1, -1): "resources/steve_kart_haut_droite.png",
    (1, 0): "resources/steve_kart_droite.png",
    (1, 1): "resources/steve_kart_bas_droite.png",
    (0, 0): "resources/steve_kart_dos.png",
    (0, 1): "resources/steve_kart_face.png",
    (-1, 1): "resources/steve_kart_bas_gauche.png",
    (-1, 0): "resources/steve_kart_gauche.png",
    (-1, -1): "resources/steve_kart_haut_gauche.png",
}

for x in [-1, 0, 1]:
    for y in [-1, 0, 1]:
        nom_fichier = kart_images[(x, y)]
        print(nom_fichier)
        image = pygame.image.load(nom_fichier)
        image.set_colorkey(MALIBU)  # color du fond a ne pas i,primer
        kart_images[(x, y)] = pygame.transform.scale(image, (TAILLE_KART, TAILLE_KART))

circuit = Sprite()
circuit.image = pygame.image.load("resources/steve_kart_map.png")
circuit.image = pygame.transform.scale(circuit.image, TAILLE_ECRAN)
circuit.rect = pygame.Rect((0,0), TAILLE_ECRAN)

steve = Sprite()
steve.image = kart_images[tuple(direction)]
steve.rect = pygame.Rect(DEMARRAGE_KART, (TAILLE_KART, TAILLE_KART))
decors = pygame.sprite.Group(circuit)
karts = pygame.sprite.Group(steve)
# steve taille

direction = [0,1]
direction[0] = 0
direction[1] = -1


# boucle principale
clock = pygame.time.Clock()
while True:
    time = clock.tick(60)

    # détection clavier et direction + position
    keys = pygame.key.get_pressed()

    direction[0] = 0
    direction[1] = 0

    if keys[pygame.K_UP]:
        direction[1] -= 1

    if keys[pygame.K_DOWN]:
        direction[1] += 1

    if keys[pygame.K_RIGHT]:
        direction[0] += 1

    if keys[pygame.K_LEFT]:
        direction[0] -= 1

    steve.rect.x += direction[0] * VITESSE
    steve.rect.y += direction[1] * VITESSE

    # si la direction change, changer l'image
    if direction[0] != 0 or direction[1] != 0:
        steve.image = kart_images[tuple(direction)]

    # dessin
    decors.draw(screen)
    karts.draw(screen)
    pygame.display.flip()

    # détection d'evenement
    liste_evenements = pygame.event
    for nouvel_evenement in liste_evenements.get():
        # check if the event is the X button
        if nouvel_evenement.type == pygame.QUIT:
            # if it is quit the game
            exit(0)
