import pygame
from fichier_secteurs import generation_cartes_secteur, init_debogue, rendu_deboggage
from gestion_interface import detection_signal_interruption, lecture_direction_joysticks, lecture_touches_pressées

from initialisation_images import (
    generation_sprite_circuit,
    generation_sprites_kart_bob,
    generation_sprites_kart_steve,
    preparation_masque_hors_piste,
)
from kart import Kart, change_direction_selon_commande, detection_reload, mise_a_jour_kart, remise_kart_au_depart

pygame.init()
pygame.joystick.init()

# mettre à la bonne taille
screen = pygame.display.set_mode((768, 768))
VITESSE_HORS_PISTE = 0.5
POSITION_DEPART = [145, 637]
POSITION_DEPART_2 = [165, 637]


COMMANDES_STEVE = {
    "haut": pygame.K_z,
    "bas": pygame.K_s,
    "gauche": pygame.K_q,
    "droite": pygame.K_d,
    "reload": pygame.K_f,
}

COMMANDES_BOB = {
    "haut": pygame.K_UP,
    "bas": pygame.K_DOWN,
    "gauche": pygame.K_LEFT,
    "droite": pygame.K_RIGHT,
    "reload": pygame.K_RSHIFT,
}


def afficher_tout(
    screen, circuit, sortie, karts, debogue
):
    screen.blit(circuit, (0, 0))
    screen.blit(sortie, (0, 0))
    for kart in karts:
        screen.blit(source=kart.image_courante, dest=kart.position)
    screen.blit(source=debogue, dest=(10, 10))
    pygame.display.flip()


# mise en route joysticks
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for joystick in joysticks:
    print(joystick)

# chargement images et graphismes
police_debogue = init_debogue()
circuit = generation_sprite_circuit()
sortie_mask, sortie = preparation_masque_hors_piste()
zones_secteurs: pygame.Surface = generation_cartes_secteur()

# initialisation Steve
steve = Kart()
steve.images = generation_sprites_kart_steve()
steve.position_depart = POSITION_DEPART
steve.direction_x = 0
steve.direction_y = -1
steve.vitesse = 0
steve.secteurs = set()
steve.secteur_courant = -1
steve.image_courante = steve.images[(steve.direction_x, steve.direction_y)]
steve.touches_commande = COMMANDES_STEVE
remise_kart_au_depart(steve)

# initialisation bob
bob = Kart()
bob.images = generation_sprites_kart_bob(steve.images)
bob.position_depart = POSITION_DEPART_2
bob.direction_x = 0
bob.direction_y = -1
bob.vitesse = 0
bob.secteur_courant = None
bob.secteurs = set()
bob.image_courante = bob.images[(bob.direction_x, bob.direction_y)]
bob.touches_commande = COMMANDES_BOB
remise_kart_au_depart(bob)

axes_joystick_steve = {
    "haut": False,
    "bas": False,
    "gauche": False,
    "droite": False,
}
axes_joystick_bob = {
    "haut": False,
    "bas": False,
    "gauche": False,
    "droite": False,
}


def mise_a_jour_karts(steve, bob, sortie_mask, zones_secteurs):
    mise_a_jour_kart(steve, sortie_mask, zones_secteurs)
    mise_a_jour_kart(bob, sortie_mask, zones_secteurs)


# boucle principale
clock = pygame.time.Clock()


while True:
    time = clock.tick(60)

    # détection clavier et direction + position Steve
    etat_touches = lecture_touches_pressées()
    evenements = pygame.event.get()
    axes_joystick_steve, axes_joystick_bob = lecture_direction_joysticks(joysticks)

    # détection d'evenement
    detection_signal_interruption(evenements, etat_touches)

    change_direction_selon_commande(steve, etat_touches, axes_joystick_steve)
    change_direction_selon_commande(bob, etat_touches, axes_joystick_bob)

    detection_reload(steve, etat_touches, axes_joystick_steve)
    detection_reload(bob, etat_touches, axes_joystick_bob)

    mise_a_jour_karts(steve, bob, sortie_mask, zones_secteurs)

    debogue = rendu_deboggage(police_debogue, steve, bob)

    afficher_tout(
        screen,
        circuit,
        sortie,
        (steve,bob),
        debogue
    )
