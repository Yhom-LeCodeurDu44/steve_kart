import pygame

pygame.init()

# mettre à la bonne taille
screen = pygame.display.set_mode((768, 768))
MALIBU = (140, 198, 255)
TAILLE_KART = 20
VITESSE_MAX = 4
vitesse = VITESSE_MAX
VITESSE_HORS_PISTE = 0.5
POSITION_DEPART = [145, 637]



def generation_sprites_kart():
    sprites = {
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
            nom_fichier = sprites[(x, y)]
            print(nom_fichier)
            image = pygame.image.load(nom_fichier)
            image.set_colorkey(MALIBU)  # color du fond a ne pas imprimer
            sprites[(x, y)] = pygame.transform.scale(image, (TAILLE_KART, TAILLE_KART))
    
    return sprites

def preparation_masque_hors_piste():
    sortie = pygame.image.load("resources/circuit.png")
    sortie = pygame.transform.scale(sortie, (768, 768))
    sortie.set_colorkey(MALIBU)
    mask = pygame.mask.from_surface(sortie)
    return mask, sortie

def generation_sprite_circuit():
    circuit = pygame.image.load("resources/steve_kart_map.png")
    circuit.set_colorkey(MALIBU)
    return pygame.transform.scale(circuit, (768, 768))

def calcul_commande_direction( keys ):
    direction_x = 0
    direction_y = 0

    if keys[pygame.K_z]:
        direction_y -= 1

    if keys[pygame.K_s]:
        direction_y += 1

    if keys[pygame.K_d]:
        direction_x += 1

    if keys[pygame.K_q]:
        direction_x -= 1

    return direction_x, direction_y

def commande_reload_position( steve_position, keys ):
    if keys[pygame.K_f]:
        print('replacement demandé2')
        #jai essayé des trucs mais jsp...
        steve_position = POSITION_DEPART


def mise_a_jour_nouvelle_position(steve_position, direction_x, direction_y, vitesse):
    steve_position[0] += direction_x * vitesse
    steve_position[1] += direction_y * vitesse
    return steve_position
    #le contenu de steve_position est directement modifié

def detection_hors_piste(sortie_mask, kart_steve):
    maskart = pygame.mask.from_surface(kart_steve)
    return sortie_mask.overlap(maskart, steve_position)
    
def mise_a_jour_vitesse_horspiste( vitesse_courante, horspiste ):
    if horspiste: 
        if vitesse_courante <= 0:
            return 0
        else:
            return vitesse_courante - VITESSE_MAX/35
    else :
        return VITESSE_MAX    
    
def choisir_orientation_sprite_steve_kart( kart_courant, direction_x, direction_y ):     
    # si la direction change, changer l'image
    if direction_y != 0 or direction_x != 0:
        return kart_images[(direction_x, direction_y)]
    else:
        return kart_courant

def detection_signal_interruption():
    liste_evenements = pygame.event
    for nouvel_evenement in liste_evenements.get():
        # vérifier si signal se sortie
        if nouvel_evenement.type == pygame.QUIT:
            # cassos
            exit(0)

def afficher_tout(screen, circuit, sortie, kart_steve, steve_position):
    screen.blit(circuit, (0, 0))
    screen.blit(sortie, (0, 0))
    screen.blit(source=kart_steve, dest=steve_position)
    pygame.display.flip()

kart_images = generation_sprites_kart()
circuit = generation_sprite_circuit()
sortie_mask, sortie = preparation_masque_hors_piste()
    
#initialisation Steve
direction_x = 0
direction_y = -1
kart_steve = kart_images[(direction_x, direction_y)]
steve_position = POSITION_DEPART

# boucle principale
clock = pygame.time.Clock()
while True:
    time = clock.tick(60)

    # détection clavier et direction + position
    keys = pygame.key.get_pressed()

    direction_x, direction_y = calcul_commande_direction( keys )

    commande_reload_position( steve_position, keys )

    mise_a_jour_nouvelle_position(steve_position, direction_x, direction_y, vitesse)
    
    # arreter le kart si hors piste   
    horspiste = detection_hors_piste( sortie_mask, kart_steve)
    vitesse = mise_a_jour_vitesse_horspiste( vitesse, horspiste )

    kart_steve = choisir_orientation_sprite_steve_kart(kart_steve, direction_x, direction_y)

    afficher_tout( screen, circuit, sortie, kart_steve, steve_position )

    # détection d'evenement
    detection_signal_interruption()