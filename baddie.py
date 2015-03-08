'''
Created on Aug 8, 2014

@author: DemiCow
'''
import pygame 
import math 
import random 
import squid
import prepare


#imgsize = (75,75)
number_of_frames = 4

type_1 = (75,75)
type_2 = (100,100)
type_3 = (150,50)



class Baddie(squid.Squid):

    def __init__(self, scene):
        """ intialize sprite class """
        pygame.sprite.DirtySprite.__init__(self)
        self.scene = scene
        self.screen = prepare.SCREEN
       
        self.wave_dict = {0 : ['l_fish','b_fish','q_fish'], 
                          1: ['mothfish', 'ecto', 'strix'],
                          2: ['spidy', 'waxy', 'qbee'],
                          3: ['dollface', 'lucy', 'sylvie'],
                          4: ['l_fish']
                          }
        #default sprite attributes            
        self.pause = 0
        self.delay = 400
        self.movement_counter = None
        self.list_id = 0
        self.list_index = 0
        self.magic_index = 1
        self.reset()
                
    def load_images(self):       
        self.imgmaster = prepare.BADDIES[self.name]
        if self.list_index == self.magic_index:
            self.imgmaster = self.shaded_image(self.imgmaster, (255,0,255))
        else: pass
    
        #intial placeholder image
        self.imgstand = pygame.Surface(self.image_size, pygame.SRCALPHA)        
        self.imgstand.blit(self.imgmaster, (0, 0), ((0,0), self.image_size))       
        
        #populates list of frames, using imgsize that matches frame size
        self.imgmoving= []
        offsetmoving = tuple((self.image_size[0]*i,0) 
                             for i in range(self.number_of_frames))
        
        for i in range(0,self.number_of_frames):
            tmpimg = pygame.Surface(self.image_size, pygame.SRCALPHA)
            tmpimg.blit(self.imgmaster, (0, 0), (offsetmoving[i], self.image_size))            
            self.imgmoving.append(tmpimg)
            
        self.imgdead= []
        offsetdead = tuple((self.image_size[0]*i,self.image_size[1]) 
                             for i in range(self.number_of_frames))
        
        for i in range(0,self.number_of_frames):
            tmpimg = pygame.Surface(self.image_size, pygame.SRCALPHA)
            tmpimg.blit(self.imgmaster, (0, 0), (offsetdead[i], self.image_size))          
            self.imgdead.append(tmpimg)
               
    def check_bounds(self):  
        """returns TRUE if sprite is visible"""
        if self.rect.x > self.screen.get_width() or self.rect.x < 0:   
            return False
        else:
            return True
    
    def ghost_image(self, image, color):
        shaded = image.copy()
        shaded.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return shaded

    def shaded_image(self,image, color):
        copied = image.copy()
        ghost = self.ghost_image(image, color)
        copied.blit(ghost, (0,0))
        return copied
    
                  
    def update(self, time_delta):     
        #SAVE PNGS AT 8 BIT  
        self.animation(time_delta)
        if self.currentimage == self.imgdead:
            self.die()        
        if self.check_bounds() == True:                             
            if self.scene.scroll_to_left == True:
                self.flip()
            
            if self.hit == True :
                self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)
                self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 2) 
                self.hit = False
            else: self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)
            
            
               
    def die(self):
        """if curent image is dead, moves self offscreen after animation plays."""
        if self.frame >= self.number_of_frames-1:
            self.dead = True
            self.reset()
                
   
    def reset(self):
        """"calls when object created and at start of each wave.
        object can change appearance and properties."""   
        self.frame = random.randrange(0,3)        
        self.name = random.choice(self.wave_dict[self.scene.wave_number])
        self.image_size = type_1
        self.number_of_frames = number_of_frames
        self.hp = 1
        self.load_images()        
        self.image = self.imgstand
        self.currentimage = self.imgmoving
        self.rect = self.image.get_rect()     
        self.rect.inflate_ip(-5, -5)    
        self.size = self.image.get_size()
        self.hit = False
        self.rect.centerx, self.rect.centery = (9000,9000)            
        #