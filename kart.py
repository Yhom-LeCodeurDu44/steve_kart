import pygame

from fichier_secteurs import detection_secteur, mise_a_jour_secteurs_traverses


VITESSE_MAX = 4


class Kart:
    images:None
    direction_x:int = 0
    direction_y:int = -1
    image_courante=None
    position:[int]
    vitesse:int = 0
    secteur_courant:int = None
    secteurs:set()

def calcul_commande_direction( liste_touches_appuyees, touche_haut, touche_bas, touche_gauche, touche_droite ):
    direction_x = 0
    direction_y = 0

    if liste_touches_appuyees[touche_haut]:
        direction_y -= 1

    if liste_touches_appuyees[touche_bas]:
        direction_y += 1

    if liste_touches_appuyees[touche_droite]:
        direction_x += 1

    if liste_touches_appuyees[touche_gauche]:
        direction_x -= 1

    return direction_x, direction_y

def change_direction_selon_commande_steve( kart, keys ):
    kart.direction_x, kart.direction_y = calcul_commande_direction (keys, pygame.K_z, pygame.K_s, pygame.K_q, pygame.K_d )


def calcul_commande_direction_bob( kart, keys ):
    kart.direction_x, kart.direction_y = calcul_commande_direction( keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT )

def calcul_nouvelle_position(kart):
    kart.position = [
        int(kart.position[0] + kart.direction_x * kart.vitesse),
        int(kart.position[1] + kart.direction_y * kart.vitesse)
    ]


def detection_hors_piste(sortie_mask, kart_courant, position_courante):
    maskart = pygame.mask.from_surface(kart_courant)
    return sortie_mask.overlap(maskart, position_courante)
    

def mise_a_jour_vitesse( kart, horspiste ):
    if horspiste: 
        if kart.vitesse <= 0:
            kart.vitesse = 0
        else:
            kart.vitesse -= VITESSE_MAX/50
    else :
        kart.vitesse = VITESSE_MAX    
    
def choisir_orientation_sprite(kart):
    kart.image_courante = choisir_orientation_sprite_kart(kart.image_courante, kart.direction_x, kart.direction_y, kart.images)
    

def choisir_orientation_sprite_kart( kart_courant, direction_x, direction_y, sprite_images ):
    # si la direction change, changer l'image
    if direction_y != 0 or direction_x != 0:
        return sprite_images[(direction_x, direction_y)]
    else:
        return kart_courant


def choisir_orientation_sprite_bob_kart( bob, kart_courant, direction_x, direction_y ):     
    return choisir_orientation_sprite_kart( kart_courant, direction_x, direction_y, bob.images)

def mise_a_jour_kart(kart, sortie_mask, zones_secteurs):
        horspiste = detection_hors_piste( sortie_mask, kart.image_courante, kart.position)
        mise_a_jour_vitesse( kart, horspiste )
        calcul_nouvelle_position(kart)
        choisir_orientation_sprite(kart)
        secteur = detection_secteur( zones_secteurs, kart.position)
        mise_a_jour_secteurs_traverses(kart, secteur)
    
    