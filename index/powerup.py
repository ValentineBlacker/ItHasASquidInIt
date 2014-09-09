'''
Created on Aug 8, 2014

@author: DemiCow
'''
import pygame, random, baddie

class Powerup(baddie.Baddie):    
    def __init__(self, scene):     
        pygame.sprite.DirtySprite.__init__(self)
        self.scene = scene
        self.screen = scene.screen    
        self.image_size = (25, 25)
        self.reset() 
        
    def load_images(self):
        """ Loads powerup image based on color"""
        imagemaster = pygame.image.load("images/prawn.png")
        imagemaster = imagemaster.convert_alpha()
        offset_dict = {'blue': 0, 'red': 1, 'yellow': 2}
        self.img_drop = pygame.Surface(self.image_size, pygame.SRCALPHA)        
        self.img_drop.blit(imagemaster, (0, 0), ((0,0), self.image_size))
        
        image_drop = pygame.Surface(self.image_size, pygame.SRCALPHA)
        image_drop.blit(imagemaster, (0, 0), ((offset_dict[self.color]*self.image_size[0],0), self.image_size)) 
        self.image = image_drop
                    
    def movement(self):
        pass
    
    def animation(self):
        pass
         
    def update(self):
        self.startmovement -=1
        if self.startmovement <0:
            if self.scene.foreground_map.at_end == True:
                self.rect.x += (self.dx/2)
            else: self.rect.x += self.dx
            if self.check_bounds() == True:
                self.scene.screen.blit(self.image, (self.rect.x, self.rect.y), 
                                       special_flags= 0)
            
            
    
                
    def reset(self):
        self.startmovement = random.randrange(0,
                            (self.scene.foreground_map.tile_size_x*
                            self.scene.foreground_map.map_width)/4)
        if self.scene.scroll_to_left == True:
            self.dx = - (self.scene.speed + (self.scene.speed_increase * 
                                             self.scene.wave_number+1)) 
        else: self.dx = self.scene.speed + (self.scene.speed_increase * 
                                            self.scene.wave_number+1)
                        
        self.power_dict = {0: 'blue',
                           1: 'red',
                           2: 'yellow'
                           }   
        self.power_type = random.randrange(0,3)  
        self.color = self.power_dict[self.power_type] 
        self.load_images()        
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.inflate_ip(-5, -5)    
        if self.scene.scroll_to_left :
            self.rect.x =  self.scene.field_length +1
        else: 
            self.rect.x = -1    
        self.rect.y = random.randrange(50,(self.screen.get_height()-50))
         
        