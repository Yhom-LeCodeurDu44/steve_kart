from typing import List
from pygame import Mask, Surface
import pygame

from fichier_secteurs import detection_secteur, mise_a_jour_secteurs_traverses


VITESSE_MAX = 4


class Kart:
    images: None
    direction_x: int = 0
    direction_y: int = -1
    image_courante = None
    position: List[int]
    vitesse: int = 0
    secteur_courant: int = None
    secteurs: set()
    touches_commande: dict = None


def calcul_commande_direction(
    liste_touches_appuyees, touche_haut, touche_bas, touche_gauche, touche_droite
):
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


def calcul_commande_direction_2(
    liste_touches_appuyees,
    touche_haut,
    touche_bas,
    touche_gauche,
    touche_droite,
    axes_joystick
):
    direction_x = 0
    direction_y = 0

    if liste_touches_appuyees[touche_haut] | axes_joystick["haut"]:
        direction_y -= 1

    if liste_touches_appuyees[touche_bas] | axes_joystick["bas"]:
        direction_y += 1

    if liste_touches_appuyees[touche_droite] | axes_joystick["droite"]:
        direction_x += 1

    if liste_touches_appuyees[touche_gauche] | axes_joystick["gauche"]:
        direction_x -= 1

    return direction_x, direction_y


def change_direction_selon_commande(kart, keys, axes_joystick):
    kart.direction_x, kart.direction_y = calcul_commande_direction_2(
        keys,
        kart.touches_commande["haut"],
        kart.touches_commande["bas"],
        kart.touches_commande["gauche"],
        kart.touches_commande["droite"],
        axes_joystick
    )

def detection_reload(kart, keys):
    if keys[kart.touches_commande["reload"]]:
        kart.position = kart.position_depart
        


def calcul_nouvelle_position(kart):
    kart.position = [
        int(kart.position[0] + kart.direction_x * kart.vitesse),
        int(kart.position[1] + kart.direction_y * kart.vitesse),
    ]


def detection_hors_piste(
    sortie_mask: Mask, image_kart: Surface, position_courante: List[int]
):
    maskart = pygame.mask.from_surface(image_kart)
    return sortie_mask.overlap(maskart, position_courante)


def mise_a_jour_vitesse(kart: Kart, horspiste: bool):
    if horspiste:
        calcul_vitesse_horspiste(kart)
    else:
        kart.vitesse = VITESSE_MAX


def calcul_vitesse_horspiste(kart: Kart):
    # on diminue la vitesse de 1/50 de la vitesse max
    kart.vitesse -= VITESSE_MAX / 50
    if kart.vitesse <= 0:
        # on évite les vitesses négatives
        kart.vitesse = 0


def choisir_orientation_sprite(kart: Kart):
    # si la direction change, changer l'image
    if kart.direction_y != 0 or kart.direction_x != 0:
        oriente_image_kart(kart)
    # sinon garder la même image


def oriente_image_kart(kart: Kart):
    kart.image_courante = kart.images[(kart.direction_x, kart.direction_y)]


def mise_a_jour_kart(kart: Kart, sortie_mask: Mask, zones_secteurs: Surface):

    horspiste = detection_hors_piste(sortie_mask, kart.image_courante, kart.position)
    mise_a_jour_vitesse(kart, horspiste)
    calcul_nouvelle_position(kart)
    choisir_orientation_sprite(kart)
    secteur = detection_secteur(zones_secteurs, kart.position)
    mise_a_jour_secteurs_traverses(kart, secteur)
