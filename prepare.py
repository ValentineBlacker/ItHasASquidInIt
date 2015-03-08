'''
Created on Dec 4, 2014

@author: DemiCow
'''

import pygame
import os
import pycurve

def load_all_sounds(directory, accept=(".wav", ".mp3", ".ogg", ".mdi")):
    """Create a dictionary of paths to music files in given directory
    if their extensions are in accept."""
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def load_all_baddies(directory,colorkey=(255,0,255),accept=(".png")):
    """Load all graphics with extensions in the accept argument. If alpha
    transparency is found in the image the image will be converted using
    convert_alpha(). If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey."""
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory, pic))    
            img = img.convert_alpha() 
        graphics[name]=img   
    return graphics

def load_all_bosses(directory,colorkey=(255,0,255),accept=(".png")):
    """Load all graphics with extensions in the accept argument. If alpha
    transparency is found in the image the image will be converted using
    convert_alpha(). If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey."""
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory, pic))    
            img = img.convert_alpha() 
        graphics[name]=img   
    return graphics

def load_all_images(directory,colorkey=(255,0,255),accept=(".png")):
    """Load all graphics with extensions in the accept argument. If alpha
    transparency is found in the image the image will be converted using
    convert_alpha(). If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey."""
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory, pic))    
            img = img.convert_alpha() 
        graphics[name]=img   
    return graphics

def load_all_maps(directory,colorkey=(255,0,255),accept=(".png")):
    """Load all graphics with extensions in the accept argument. If alpha
    transparency is found in the image the image will be converted using
    convert_alpha(). If no alpha transparency is detected image will be
    converted using convert() and colorkey will be set to colorkey."""
    graphics = {}
    for pic in os.listdir(directory):
        name,ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory, pic))    
            img = img.convert_alpha() 
        graphics[name]=img   
    return graphics


RESOLUTION = (1280, 768)
CAPTION = "it has a squid in it"
#Initialization
pygame.init()
pygame.mixer.init()

pygame.display.set_caption(CAPTION)
SCREEN = pygame.display.set_mode(RESOLUTION)
SCREEN_RECT = SCREEN.get_rect()
MASTER_SPEED = 36
FPS = 60
MUSIC_ON = False
#Resource loading

SOUNDS = load_all_sounds(os.path.join('data/sounds'))
IMAGES = load_all_images(os.path.join("data/images/misc"))
BADDIES = load_all_baddies(os.path.join("data/images/baddies"))
BOSSES = load_all_bosses(os.path.join("data/images/bosses"))
MAPS = load_all_maps(os.path.join("data/images/maps"))
FONT = "data/images/misc/Nobile-Regular.ttf"
PATHS = [pycurve.make_b_spline(RESOLUTION,pycurve.PATHS[pycurve.PATHS.index(x)]) for x in pycurve.PATHS]

img_icon = IMAGES['icon']
pygame.display.set_icon(img_icon)
pygame.display.set_caption(CAPTION)
