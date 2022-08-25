import pygame

def load_image(file_path, size=None, scale=None):
    """ 
    size: tuple (width, height)
    scale: integer value to scale the image
    """
    surface = pygame.image.load(file_path)
    if size:
        surface = pygame.transform.scale(surface, size)
    if scale:
        rect = surface.get_rect()
        surface = pygame.transform.scale(surface, (scale*rect.width, scale*rect.height))
    return surface


""" Authored by Allie Lahnala (alahnala@gmail.com) for the Hessian IT Summer School 2022 at University of Marburg"""