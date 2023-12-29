from collections.abc import Set
from typing import List
import pygame

def generation_cartes_secteur() -> pygame.Surface:
    secteur = pygame.image.load("resources/secteurs.png")
    secteur = pygame.transform.scale(secteur, (768, 768))
    return secteur


def detection_secteur(secteur: pygame.Surface, position: List[int]):
    try:
        couleur_position = secteur.get_at(position)
    except IndexError:
        # hors de la carte
        return

    COULEUR_ROUGE_DE_SECTEUR = {
        0: 0,
        17: 1,
        34: 2,
        51: 3,
        85:-1,
        68:4
    }

    try:
        return COULEUR_ROUGE_DE_SECTEUR[couleur_position.r]
    except KeyError:
        print(f'couleur de secteur inconnu {couleur_position}')
        return

def mise_a_jour_secteurs_traverses(kart, secteur):
    if secteur is None:
        return
    kart.secteur_courant = secteur
    kart.secteurs.add(kart.secteur_courant)  


def init_debogue():
    pygame.font.init()
    return pygame.font.SysFont('Calibri', 20)

def rendu_log_kart(kart):
    return f'Tours {kart.tours} | Sec {kart.secteurs}'

def rendu_deboggage(police_debogue, steve, bob):
    message = "\n".join(rendu_log_kart(k) for k in [steve, bob])
    debogue = police_debogue.render(message, False, (0,0,0))
    return debogue

def detection_tour(kart):
    if kart.secteur_courant == 0 and len(kart.secteurs) == 6:
        kart.tours += 1
        kart.secteurs = set()
    
    