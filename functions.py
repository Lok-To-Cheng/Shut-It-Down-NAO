import pygame

def clip(surf, x, y, w, h):
    handle_surf = surf.copy()
    clip_rect = pygame.Rect(x, y, w, h)
    handle_surf.set_clip(clip_rect)
    img = surf.subsurface(handle_surf.get_clip())
    return img.copy()

def apply_colour(surf, colour):
    colour_mask = pygame.Surface(surf.get_size())
    colour_mask.fill(colour)
    coloured_surf = surf.copy()
    coloured_surf.blit(colour_mask, (0, 0), special_flags=pygame.BLEND_MULT)
    return coloured_surf