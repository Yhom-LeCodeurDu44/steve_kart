import pygame

pygame.init()

# mettre à la bonne taille
screen = pygame.display.set_mode((800, 800))
MALIBU = (140, 198, 255)
WHITE = (255, 255, 255)

circuit = pygame.image.load("resources/circuit.png").convert()
circuit.set_colorkey(MALIBU)
fond_piste = pygame.image.load("resources/fond_piste_sable.jpg").convert()
fond_piste.set_colorkey(MALIBU)
# piste = pygame.image.load("resources/piste.png").convert()
# piste.set_colorkey(MALIBU)
# piste = pygame.transform.scale(piste, (800, 800))
# masque_piste.invert()

# circuit.blit(source=circuit, dest=(0,0))
circuit = pygame.transform.scale(circuit, (800, 800))
masque_piste = pygame.mask.from_surface(circuit)

print("image circuit chargée")

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
        image = pygame.transform.scale(image, (30, 30))
        KART_IMAGES[y][x] = image
        print("image kart %s,%s chargée" % (y, x))

kart_steve: pygame.Surface = KART_IMAGES[-1][0]
steve_masque = pygame.mask.from_surface(kart_steve)

steve_position = [145, 630]
screen.blit(fond_piste, (0, 0))
screen.blit(circuit, (0, 0))
screen.blit(source=kart_steve, dest=steve_position)
pygame.display.flip()

# boucle principale
clock = pygame.time.Clock()
pygame.joystick.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
else:
    joystick = None

while True:
    # on attend le framerate
    time = clock.tick(60)

    # détection de la direction, direction X et Y étant -1, 0, 1

    # par défaut, on bouge pas
    direction_axe_x = 0
    direction_axe_y = 0

    # detection des touches
    keys = pygame.key.get_pressed()

    # direction verticale
    if keys[pygame.K_UP]:
        direction_axe_y -= 1
    if keys[pygame.K_DOWN]:
        direction_axe_y += 1

    # direction horizontale
    if keys[pygame.K_LEFT]:
        direction_axe_x -= 1
    if keys[pygame.K_RIGHT]:
        direction_axe_x += 1

    # si joystick, même chose
    if joystick is not None:
        joy_x = joystick.get_axis(0)
        joy_y = joystick.get_axis(1)

        if joy_y < -0.4:
            direction_axe_y -= 1
        if joy_y > 0.4:
            direction_axe_y += 1
        if joy_x < -0.4:
            direction_axe_x -= 1
        if joy_x > 0.4:
            direction_axe_x += 1

    # calcule nouvelle position éventuelle
    x = steve_position[0]
    x += direction_axe_x * 4
    y = steve_position[1]
    y += direction_axe_y * 4

    # détection du conflit avant application de la direction

    if not steve_masque.overlap(masque_piste, (-x, -y)):  # si ça reste sur la piste on met à jour la position
        # print("sortie de piste!")
        steve_position[0] = x
        steve_position[1] = y

    if direction_axe_y != 0 or direction_axe_x != 0:  # si pas de mouvement, on garde l'image
        kart_steve = KART_IMAGES[direction_axe_y][direction_axe_x]
        steve_masque = pygame.mask.from_surface(kart_steve)

    screen.blit(fond_piste, (0, 0))
    screen.blit(circuit, (0, 0))
    screen.blit(source=kart_steve, dest=steve_position)
    pygame.display.flip()

    liste_evenements = pygame.event

    # détection d'evenement
    for nouvel_evenement in liste_evenements.get():
        # check if the event is the X button
        if nouvel_evenement.type == pygame.QUIT:
            # if it is quit the game
            exit(0)
