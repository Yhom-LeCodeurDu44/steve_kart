import pygame

pygame.init()

# mettre à la bonne taille
screen = pygame.display.set_mode((768, 768))
MALIBU = (140, 198, 255)

kart_images = {
    1: "resources/steve_kart_dos.png",
    2: "resources/steve_kart_haut_droite.png",
    3: "resources/steve_kart_droite.png",
    4: "resources/steve_kart_bas_droite.png",
    5: "resources/steve_kart_face.png",
    6: "resources/steve_kart_bas_gauche.png",
    7: "resources/steve_kart_gauche.png",
    8: "resources/steve_kart_haut_gauche.png",

}
for i in range(1, 9):
    print(kart_images[i])
    image = pygame.image.load(kart_images[i])
    image.set_colorkey(MALIBU)  # color du fond a ne pas i,primer
    kart_images[i] = pygame.transform.scale(image, (20, 20))

circuit = pygame.image.load("resources/steve_kart_map.png")
circuit = pygame.transform.scale(circuit, (768, 768))
kart_steve = kart_images[1]

# steve taille
steve_position = [145, 637]

# boucle principale
clock = pygame.time.Clock()
while True:
    time = clock.tick(60)

    # détection clavier et direction + position
    keys = pygame.key.get_pressed()
    direction = 1
    if keys[pygame.K_UP]:
        direction = 1
        steve_position[1] -= 4

    if keys[pygame.K_RIGHT]:
        direction = 3
        steve_position[0] += 4

    if keys[pygame.K_DOWN]:
        direction = 5
        steve_position[1] += 4

    if keys[pygame.K_LEFT]:
        direction = 7
        steve_position[0] -= 4

    if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
        direction = 2

    if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
        direction = 4

    if keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
        direction = 6

    if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
        direction = 8

    kart_steve = kart_images[direction]

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
