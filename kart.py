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
    touche_commandes: dict = None
    bouton_manette_reload: int = None
    position_depart: List[int] = (0, 0)


def calcul_commande_direction(
    liste_touches_appuyees,
    touches_commande,
    axes_joystick
):
    direction_x = 0
    direction_y = 0

    if liste_touches_appuyees[touches_commande["haut"]] | axes_joystick["haut"]:
        direction_y -= 1

    if liste_touches_appuyees[touches_commande["bas"] | axes_joystick["bas"]:
        direction_y += 1

    if liste_touches_appuyees[touches_commande["droite"]] | axes_joystick["droite"]:
        direction_x += 1

    if liste_touches_appuyees[touches_commande["gauche"]] | axes_joystick["gauche"]:
        direction_x -= 1

    return direction_x, direction_y


def change_direction_selon_commande(kart, keys, axes_joystick):
    kart.direction_x, kart.direction_y = calcul_commande_direction(
        keys,
        kart.touches_commande
        axes_joystick
    )

def remise_kart_au_depart(kart):
    kart.position = kart.position_depart

def detection_reload(kart, keys, axes_joystick):
    if keys[kart.touches_commande["reload"]] | axes_joystick["reload"]:
        remise_kart_au_depart(kart)
        return

        


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
    # center of kart.image_ciourante sprite
    center_kart = kart.image_courante.get_rect().center
    secteur = detection_secteur(zones_secteurs, center_kart)
    mise_a_jour_secteurs_traverses(kart, secteur)
