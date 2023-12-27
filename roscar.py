import pygame
from fichier_secteurs import generation_cartes_secteur, init_debogue, rendu_deboggage

from initialisation_images import generation_sprite_circuit, generation_sprites_kart_bob, generation_sprites_kart_steve, preparation_masque_hors_piste
from kart import Kart, change_direction_selon_commande, commande_reload, mise_a_jour_kart

pygame.init()

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

def detection_signal_interruption(keys):
    liste_evenements = pygame.event
    for nouvel_evenement in liste_evenements.get():
        # vérifier si signal se sortie
        if nouvel_evenement.type == pygame.QUIT:
            # cassos
            exit(0)
        if keys[pygame.K_ESCAPE]:
            exit(0)

def afficher_tout(screen, circuit, sortie, kart_image_a, position_a, kart_image_b, position_b, debogue):
    screen.blit(circuit, (0, 0))
    screen.blit(sortie, (0, 0))
    screen.blit(source=kart_image_a, dest=position_a)
    screen.blit(source=kart_image_b, dest=position_b)
    screen.blit(source=debogue, dest=(10,10) )
    pygame.display.flip()
    



#chargement images et graphismes
police_debogue = init_debogue()
circuit = generation_sprite_circuit()
sortie_mask, sortie = preparation_masque_hors_piste()
zones_secteurs: pygame.Surface = generation_cartes_secteur()    
 
#initialisation Steve
steve = Kart()
steve.images=generation_sprites_kart_steve()
steve.direction_x = 0
steve.direction_y = -1
steve.position = POSITION_DEPART
steve.vitesse = 0
steve.secteurs = set()
steve.secteur_courant = -1
steve.image_courante = steve.images[(steve.direction_x, steve.direction_y)]
steve.touches_commande = COMMANDES_STEVE

#initialisation bob
bob = Kart()
bob.images = generation_sprites_kart_bob(steve.images)
bob.direction_x = 0
bob.direction_y = -1
bob.position = POSITION_DEPART_2
bob.vitesse = 0
bob.secteur_courant = None
bob.secteurs = set()
bob.image_courante = bob.images[(bob.direction_x, bob.direction_y)]
bob.touches_commande = COMMANDES_BOB


# boucle principale
clock = pygame.time.Clock()
while True:
    time = clock.tick(60)

    # détection clavier et direction + position Steve
    keys = pygame.key.get_pressed()

    
    change_direction_selon_commande(steve, keys)
    change_direction_selon_commande( bob, keys )
    commande_reload( steve, keys, POSITION_DEPART )
    commande_reload( bob, keys, POSITION_DEPART_2 )

    mise_a_jour_kart(steve, sortie_mask, zones_secteurs)
    mise_a_jour_kart(bob, sortie_mask, zones_secteurs)

    debogue = rendu_deboggage(police_debogue, steve, bob)
    afficher_tout( screen, circuit, sortie, steve.image_courante, steve.position, bob.image_courante, bob.position, debogue)

    # détection d'evenement
    detection_signal_interruption(keys)
