import pygame



MALIBU = (140, 198, 255)
TAILLE_KART = 20

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

def generation_sprites_kart_verts():
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
    return generation_sprites_kart_verts()
    
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

