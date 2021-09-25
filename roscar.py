import pygame

pygame.init()

# mettre à la bonne taille
screen = pygame.display.set_mode((768, 768))
MALIBU = (140, 198, 255)
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

circuit = pygame.image.load("resources/steve_kart_map.png")
circuit = pygame.transform.scale(circuit, (768, 768))
direction_x = 0
direction_y = -1
kart_steve = kart_images[(direction_x, direction_y)]

# steve taille
steve_position = [145, 637]

# boucle principale
clock = pygame.time.Clock()
while True:
    time = clock.tick(60)

    # détection clavier et direction + position
    keys = pygame.key.get_pressed()

    direction_x = 0
    direction_y = 0

    if keys[pygame.K_UP]:
        direction_y -= 1

    if keys[pygame.K_DOWN]:
        direction_y += 1

    if keys[pygame.K_RIGHT]:
        direction_x += 1

    if keys[pygame.K_LEFT]:
        direction_x -= 1

    steve_position[0] += direction_x * VITESSE
    steve_position[1] += direction_y * VITESSE

    # si la direction change, changer l'image
    if direction_y != 0 or direction_x != 0:
        kart_steve = kart_images[(direction_x, direction_y)]

    # dessin
    screen.blit(circuit, (0, 0))
    screen.blit(source=kart_steve, dest=steve_position)
    pygame.display.flip()

    # détection d'evenement
    liste_evenements = pygame.event
    for nouvel_evenement in liste_evenements.get():
        # check if the event is the X button
        if nouvel_evenement.type == pygame.QUIT:
            # if it is quit the game
            exit(0)
