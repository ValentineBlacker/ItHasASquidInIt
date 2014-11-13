'''
Created on Aug 8, 2014

@author: DemiCow

'''
import pygame

class LifeDot(pygame.sprite.DirtySprite):
    """The icons that show how many lives you have left. Also draws nice border
    to keep them in."""
    def __init__(self, scene, pos): 
        pygame.sprite.DirtySprite.__init__(self)       
        self.scene = scene
        self.screen = scene.screen
        
        self.load_images()    
        
        self.image = self.imagemaster
        self.rect = self.image.get_rect()
        
        hud_top = self.scene.hudrect.top
        hud_left = self.scene.hudrect.left
        
        self.rect.center =(hud_left+20 + self.imgsize[0]*pos,
                            hud_top + 20)
        
        self.position = self.rect.center
        
    
                
    def load_images(self):
        imgmaster = pygame.image.load("images/icon.png")
        imgmaster = imgmaster.convert_alpha()        
        self.imgsize = (32, 32)
        
        self.imagemaster = pygame.Surface(self.imgsize, pygame.SRCALPHA)        
        self.imagemaster.blit(imgmaster, (0, 0), ((0,0), self.imgsize))  
    
    def update(self, time_delta):
        self.scene.screen.blit(self.imagemaster, (self.rect.x, self.rect.y), special_flags= 0)
        
        