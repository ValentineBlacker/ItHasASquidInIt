'''
Created on Aug 8, 2014

@author: DemiCow
'''


import pygame

try:
    import android
except ImportError:
    android = None

class Bullet(pygame.sprite.DirtySprite):
    """class for ink bullets fired by squid"""
    def __init__(self, scene):
        pygame.sprite.DirtySprite.__init__(self)
        self.scene = scene
        self.screen = scene.screen
        #default sprite attributes
        
        self.dx = 0
        self.dy = 0
        self.speed = scene.speed* 2
               
        self.dirty = 2  
        self.pause = 0
        self.frame = 0        
        self.load_images()

        self.image = self.imagebullet

        self.rect = self.image.get_rect()     
                
        self.mask = pygame.mask.from_surface(self.image)
        
        self.position = self.rect.center
        self.reset()
        
        
    def load_images(self):
        imagemaster = pygame.image.load("images/bullet.png")
        imagemaster = imagemaster.convert_alpha()        
        self.imgsize = (7, 7)
        
        self.imagebullet = pygame.Surface(self.imgsize, pygame.SRCALPHA)
        self.imagebullet.blit(imagemaster, (0, 0), ((0,0), self.imgsize))        
        
  
        
    def update(self):
        
        self.rect.x += self.dx
        #self.rect.y += self.dy
        self.check_bounds()
        
        if self.check_bounds() == True: 
            self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)  
                
    
            
    def is_fired(self, posx, posy):
        """fires bullets"""        
        self.rect.x = posx
        self.rect.y = posy
        if self.scene.scroll_to_left == True:
            self.dx = self.speed       
        else: self.dx = -self.speed 
        self._set_visible(True)
 
   
    def check_bounds(self):
        if self.rect.x > self.screen.get_width() or self.rect.x < 0:
            self.reset()
            return False
        else: return True
             
    def reset(self):
        """resets fired bullets"""
        self.rect.x= -100
        self.rect.y = -100      
        self.dx = 0
        self.dy = 0
        