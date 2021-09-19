import pygame

pygame.init()

# mettre à la bonne taille
screen = pygame.display.set_mode((800, 800))

circuit = pygame.image.load("resources/steve_kart_map.png")
circuit = pygame.transform.scale(circuit, (800, 800))

print("image circuit chargée")

MALIBU = (140, 198, 255)
KART_IMAGES = {}
fichiers = {
    -1: {-1: "resources/steve_kart_haut_gauche.png",
         0: "resources/steve_kart_dos.png",
         1: "resources/steve_kart_haut_droite.png"},
    0: {-1: "resources/steve_kart_gauche.png",
        0: "resources/steve_kart_face.png",
        1: "resources/steve_kart_droite.png"},
    1: {-1: "resources/steve_kart_bas_gauche.png",
        0: "resources/steve_kart_face.png",
        1: "resources/steve_kart_bas_droite.png"}
}

for y in [-1, 0, 1]:
    KART_IMAGES[y] = {}
    for x in [-1, 0, 1]:
        image = pygame.image.load(fichiers[y][x])
        image.set_colorkey(MALIBU)
        KART_IMAGES[y][x] = image
        print("image kart %s,%s chargée" % (y, x))

kart_steve = KART_IMAGES[-1][0]

steve_position = [145, 637]

# boucle principale
clock = pygame.time.Clock()
while True:
    time = clock.tick(60)

    liste_evenements = pygame.event

    keys = pygame.key.get_pressed()
    axe_x = 0
    axe_y = 0

    if keys[pygame.K_UP]:
        axe_y -= 1
    if keys[pygame.K_DOWN]:
        axe_y += 1
    if keys[pygame.K_LEFT]:
        axe_x -= 1
    if keys[pygame.K_RIGHT]:
        axe_x += 1

    steve_position[0] += axe_x * 4
    steve_position[1] += axe_y * 4

    if axe_y != 0 or axe_x != 0:
        kart_steve = KART_IMAGES[axe_y][axe_x]

    screen.blit(circuit, (0, 0))
    screen.blit(source=kart_steve, dest=steve_position)
    pygame.display.flip()

    # détection d'evenement
    for nouvel_evenement in liste_evenements.get():
        # check if the event is the X button
        if nouvel_evenement.type == pygame.QUIT:
            # if it is quit the game
            exit(0)
