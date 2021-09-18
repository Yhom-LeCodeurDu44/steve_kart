import pygame

pygame.init()

# mettre à la bonne taille
screen = pygame.display.set_mode((800, 800))
MALIBU = (140, 198, 255)

kart_face = pygame.image.load("resources/steve_kart_face.png")
kart_face.set_colorkey(MALIBU)
kart_droite = pygame.image.load("resources/steve_kart_droite.png")
kart_droite.set_colorkey(MALIBU)
kart_dos = pygame.image.load("resources/steve_kart_dos.png")
kart_dos.set_colorkey(MALIBU)
kart_gauche = pygame.image.load("resources/steve_kart_gauche.png")
kart_gauche.set_colorkey(MALIBU)

KART_IMAGES = []
for f in ["resources/steve_kart_haut_gauche.png",
          "resources/steve_kart_dos.png",
          "resources/steve_kart_haut_droite.png",
          "resources/steve_kart_gauche.png",
          "resources/steve_kart_face.png",
          "resources/steve_kart_droite.png",
          "resources/steve_kart_bas_gauche.png",
          "resources/steve_kart_face.png",
          "resources/steve_kart_bas_droite.png"]:
    image = pygame.image.load(f)
    image.set_colorkey(MALIBU)
    KART_IMAGES.append(image)

circuit = pygame.image.load("resources/steve_kart_map.png")
circuit = pygame.transform.scale(circuit, (800, 800))
kart_steve = kart_dos

steve_position = [145, 637]

# boucle principale
clock = pygame.time.Clock()
while True:
    time = clock.tick(60)

    screen.blit(circuit, (0, 0))
    screen.blit(source=kart_steve, dest=steve_position)
    pygame.display.flip()

    liste_evenements = pygame.event

    keys = pygame.key.get_pressed()
    direction = 4
    if keys[pygame.K_UP]:
        direction -= 3
        steve_position[1] -= 4
    if keys[pygame.K_DOWN]:
        direction += 3
        steve_position[1] += 4
    if keys[pygame.K_RIGHT]:
        direction += 1
        steve_position[0] += 4
    if keys[pygame.K_LEFT]:
        direction -= 1
        steve_position[0] -= 4

    if direction != 4:
        kart_steve = KART_IMAGES[direction]

    # détection d'evenement
    for nouvel_evenement in liste_evenements.get():
        # check if the event is the X button
        if nouvel_evenement.type == pygame.QUIT:
            # if it is quit the game
            exit(0)
