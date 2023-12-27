import pygame


def lecture_touches_pressées():
    return pygame.key.get_pressed()

def lecture_direction_joysticks(joysticks):
    nb_joysticks = pygame.joystick.get_count()

    if nb_joysticks > 0:
        axes_joystick_1 = {
            "gauche": joysticks[0].get_axis(0) < -0.2,
            "droite": joysticks[0].get_axis(0) > 0.2,
            "haut": joysticks[0].get_axis(1) < -0.2,
            "bas": joysticks[0].get_axis(1) > 0.2,
        }

    if nb_joysticks > 1:
        axes_joystick_2 = {
            "gauche": joysticks[1].get_axis(0) < -0.2,
            "droite": joysticks[1].get_axis(0) > 0.2,
            "haut": joysticks[1].get_axis(1) < -0.2,
            "bas": joysticks[1].get_axis(1) > 0.2,
        }

    return axes_joystick_1, axes_joystick_2


def detection_signal_interruption(liste_evenements, etat_touches):
    for nouvel_evenement in liste_evenements:
        # vérifier si signal se sortie
        if nouvel_evenement.type == pygame.QUIT:
            # cassos
            exit(0)
        if etat_touches[pygame.K_ESCAPE]:
            exit(0)
        # print(f"evenement non traité {nouvel_evenement}")