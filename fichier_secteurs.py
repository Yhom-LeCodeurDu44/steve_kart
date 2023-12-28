from collections.abc import Set
from typing import List
import pygame

def generation_cartes_secteur() -> pygame.Surface:
    secteur = pygame.image.load("resources/secteurs.png")
    secteur = pygame.transform.scale(secteur, (768, 768))
    return secteur


def detection_secteur(secteur: pygame.Surface, steve_position: List[int]):
    steve_secteur_couleur = secteur.get_at(steve_position)
    
    COULEUR_SECTEURS_RED = {
        0: 0,
        17: 1,
        34: 2,
        51: 3,
        85:-1,
        68:4
    }

    try:
        return COULEUR_SECTEURS_RED[steve_secteur_couleur.r]
    except KeyError:
        return

def mise_a_jour_secteurs_traverses(kart, secteur):
    kart.secteur_courant = secteur
    if kart.secteur_courant is None:
        return
    else:
        kart.secteurs.add(kart.secteur_courant)  


def init_debogue():
    pygame.font.init()
    return pygame.font.SysFont('Calibri', 20)

def rendu_deboggage(police_debogue, steve, bob):
    message = f'Steve: {steve.tours}/{steve.secteurs}\nBob: {bob.tours}/{bob.secteurs}'
    debogue = police_debogue.render(message, False, (0,0,0))
    return debogue

def detection_tour(kart):
    if kart.secteur == 0 && len(kart.secteurs) == 6:
        kart.tours += 1
        kart.secteurs = set()
    
    