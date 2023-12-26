import pygame

pygame.init()

# mettre à la bonne taille
screen = pygame.display.set_mode((768, 768))
MALIBU = (140, 198, 255)
TAILLE_KART = 20
VITESSE_MAX = 4
VITESSE_HORS_PISTE = 0.5
POSITION_DEPART = [145, 637]
POSITION_DEPART_2 = [165, 637]

def convertir_couleur(img, vert_clair, rouge_clair):
    original_color_key = img.get_colorkey()
    img.set_colorkey(vert_clair)
    surf = img.copy()
    surf.fill(rouge_clair)
    surf.blit(img, (0, 0))
    img.set_colorkey(original_color_key)
    surf.set_colorkey(original_color_key)
    return surf

def transform_vert_to_rouge(img):
    vert_clair = [24, 235, 0]
    rouge_clair = [236, 10, 10]
    vert_foncé = [0, 162, 0]
    rouge_foncé = [155, 33, 33]
    surf = convertir_couleur(img, vert_clair, rouge_clair)
    surf = convertir_couleur(surf, vert_foncé, rouge_foncé)
    return surf

def initialiser_images_kart(fichiers_karts):
    images = {}
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            nom_fichier = fichiers_karts[(x, y)]
            print(nom_fichier)
            image = pygame.image.load(nom_fichier)
            image.set_colorkey(MALIBU)  # color du fond a ne pas i,primer
            images[(x, y)] = pygame.transform.scale(image, (TAILLE_KART, TAILLE_KART))
    return images


def convertir_images_kart_en_rouge(sprites_verts):
    images_rouges = {}
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            img = sprites_verts[(x, y)]
            images_rouges[(x, y)] = transform_vert_to_rouge(img)
    return images_rouges

def generation_sprites_kart_verts(nom_kart='steve'):
    sprites_verts = {
        (0, -1): "resources/kart_vert_dos.png",
        (1, -1): "resources/kart_vert_haut_droite.png",
        (1, 0): "resources/kart_vert_droite.png",
        (1, 1): "resources/kart_vert_bas_droite.png",
        (0, 0): "resources/kart_vert_dos.png",
        (0, 1): "resources/kart_vert_face.png",
        (-1, 1): "resources/kart_vert_bas_gauche.png",
        (-1, 0): "resources/kart_vert_gauche.png",
        (-1, -1): "resources/kart_vert_haut_gauche.png",
    }

    return initialiser_images_kart(sprites_verts)

def generation_sprites_kart_steve():
    return generation_sprites_kart_verts("steve")
    
def generation_sprites_kart_bob(sprites_verts):
    return convertir_images_kart_en_rouge(sprites_verts)

def preparation_masque_hors_piste():
    sortie = pygame.image.load("resources/circuit.png")
    sortie = pygame.transform.scale(sortie, (768, 768))
    sortie.set_colorkey(MALIBU)
    mask = pygame.mask.from_surface(sortie)
    return mask, sortie

def generation_sprite_circuit():
    circuit = pygame.image.load("resources/oskart_map.png")
    circuit.set_colorkey(MALIBU)
    return pygame.transform.scale(circuit, (768, 768))

def calcul_commande_direction( liste_touches_appuyees, touche_haut, touche_bas, touche_gauche, touche_droite ):
    direction_x = 0
    direction_y = 0

    if liste_touches_appuyees[pygame.K_z]:
        direction_y -= 1

    if liste_touches_appuyees[pygame.K_s]:
        direction_y += 1

    if liste_touches_appuyees[pygame.K_d]:
        direction_x += 1

    if liste_touches_appuyees[pygame.K_q]:
        direction_x -= 1

    return direction_x, direction_y

def calcul_commande_direction_steve( keys ):
    return calcul_commande_direction (keys, pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d )

def calcul_commande_direction_bob( keys ):
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

    return direction_x, direction_y

def calcul_nouvelle_position(position, direction_x, direction_y, vitesse):
    nouvelle_position = [
        position[0] + direction_x * vitesse,
        position[1] + direction_y * vitesse
    ]
    return nouvelle_position


def detection_hors_piste(sortie_mask, kart_courant, position_courante):
    maskart = pygame.mask.from_surface(kart_courant)
    return sortie_mask.overlap(maskart, position_courante)
    

def mise_a_jour_vitesse( vitesse_courante, horspiste ):
    if horspiste: 
        if vitesse_courante <= 0:
            return 0
        else:
            return vitesse_courante - VITESSE_MAX/50
    else :
        return VITESSE_MAX    
    
def choisir_orientation_sprite_kart( kart_courant, direction_x, direction_y, sprite_images ):
    # si la direction change, changer l'image
    if direction_y != 0 or direction_x != 0:
        return sprite_images[(direction_x, direction_y)]
    else:
        return kart_courant
    
def choisir_orientation_sprite_steve_kart( kart_courant, direction_x, direction_y ):     
    return choisir_orientation_sprite_kart( kart_courant, direction_x, direction_y, steve_images)

def choisir_orientation_sprite_bob_kart( kart_courant, direction_x, direction_y ):     
    return choisir_orientation_sprite_kart( kart_courant, direction_x, direction_y, bob_images)

def detection_signal_interruption(keys):
    liste_evenements = pygame.event
    for nouvel_evenement in liste_evenements.get():
        # vérifier si signal se sortie
        if nouvel_evenement.type == pygame.QUIT:
            # cassos
            exit(0)
        if keys[pygame.K_ESCAPE]:
            exit(0)

def afficher_tout(screen, circuit, sortie, kart_a, position_a, kart_b, position_b):
    screen.blit(circuit, (0, 0))
    screen.blit(sortie, (0, 0))
    screen.blit(source=kart_a, dest=position_a)
    screen.blit(source=kart_b, dest=position_b)
    pygame.display.flip()


steve_images = generation_sprites_kart_steve()
bob_images = generation_sprites_kart_bob(steve_images)
circuit = generation_sprite_circuit()
sortie_mask, sortie = preparation_masque_hors_piste()
    
#initialisation Steve
steve_direction_x = 0
steve_direction_y = -1
steve_kart = steve_images[(steve_direction_x, steve_direction_y)]
steve_position = POSITION_DEPART
steve_vitesse = 0

#initialisation bob
bob_direction_x = 0
bob_direction_y = -1
bob_kart = bob_images[(bob_direction_x, bob_direction_y)]
bob_position = POSITION_DEPART_2
bob_vitesse = 0

def calcul_touche_reload_position( touche_reload_position, steve_position, bob_position, keys ):

    return
def commande_reload_position_steve( steve_position, keys ):
    if keys[pygame.K_f]:
        return POSITION_DEPART
    else:
        return steve_position 
    
def commande_reload_position_bob( bob_position, keys ):
    if keys[pygame.K_RSHIFT]:
        return POSITION_DEPART
    else:
        return bob_position 

# boucle principale
clock = pygame.time.Clock()
while True:
    time = clock.tick(60)

    # détection clavier et direction + position Steve
    keys = pygame.key.get_pressed()

    steve_direction_x, steve_direction_y = calcul_commande_direction_steve( keys )
    steve_position = commande_reload_position_steve( steve_position, keys )
    horspiste = detection_hors_piste( sortie_mask, steve_kart, steve_position)
    # arreter le kart si hors piste 
    steve_vitesse = mise_a_jour_vitesse( steve_vitesse, horspiste )
    steve_position = calcul_nouvelle_position(steve_position, steve_direction_x, steve_direction_y, steve_vitesse)
    steve_kart = choisir_orientation_sprite_steve_kart(steve_kart, steve_direction_x, steve_direction_y)
    
    # détection clavier et direction + position Bob
    bob_direction_x, bob_direction_y = calcul_commande_direction_bob( keys )
    bob_position = commande_reload_position_bob( bob_position, keys )
  
    horspiste = detection_hors_piste( sortie_mask, bob_kart, bob_position)
    bob_vitesse = mise_a_jour_vitesse( bob_vitesse, horspiste )
    bob_position = calcul_nouvelle_position(bob_position, bob_direction_x, bob_direction_y, bob_vitesse)
    bob_kart = choisir_orientation_sprite_bob_kart(bob_kart, bob_direction_x, bob_direction_y)

    afficher_tout( screen, circuit, sortie, steve_kart, steve_position, bob_kart, bob_position )

    # détection d'evenement
    detection_signal_interruption(keys)
