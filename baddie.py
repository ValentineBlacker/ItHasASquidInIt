'''
Created on Aug 8, 2014

@author: DemiCow
'''
import pygame 
import math 
import random 
import squid



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
        self.screen = scene.screen   
       
        self.wave_dict = {0 : ['l_fish','b_fish','q_fish'], 
                          1: ['mothfish', 'ecto', 'strix'],
                          2: ['spidy'],
                          3: ['spidy']
                          }
        #default sprite attributes
        self.sinpause = 0     
        self.sinframe = 0    
        self.pause = 0
        self.delay = 7      
        self.id = id
        self.reset()
        
        
    def load_images(self):
                    
        self.imgmaster= pygame.image.load("images/baddies/{0}.png".format
                                           (self.name))        
        self.imgmaster = self.imgmaster.convert_alpha()
    
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
    
                  
    def update(self):   
        self.animation()
        if self.currentimage == self.imgdead:
            self.die()
        if self.dead == False:
            self.startmovement -= 1
        self.movement()
        if self.startmovement <0:
            if self.scene.foreground_map.at_end == True:
                self.rect.x += (self.dx/2)
            else: self.rect.x += self.dx
            self.rect.y += self.dy  
            if self.scene.scroll_to_left == True:
                self.flip()
            if self.check_bounds() == True:
                if self.hit == True :
                    self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)
                    self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 2) 
                    self.hit = False
                else: self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)
            
               
    def die(self):
        """if curent image is dead, moves self offscreen after animation plays."""
        if self.frame >= self.number_of_frames-1:
            if self.scene.boss_dead == False:
                self.reset()
            else: self.rect.x = -1000
          
            
    def determine_movement(self):
        """randomly modifies curvy path"""
        self.move_delay = (random.randrange(5,15))
        self.sin_modifier = (random.randrange(0,self.scene.wave_number+4)) 
        self.sin_counter = (random.randrange(50,60)) 
 
    def movement(self):
        """creates sine wave path in y axis"""
        #frame is x. yposition = sin(x)
        if self.startmovement < 0:
            delay = self.move_delay     
            self.sinpause += 1
            if self.sinpause >= delay:
                self.sinpause = 0    
                self.sinframe += 1
                if self.sinframe >= 50:
                    self.sinframe = 0           
            self.dy = (-(self.sin_modifier*(math.sin)(self.sinframe))) 
            
    
   
    def reset(self):
        """"calls when object created and at start of each wave.
        object can change appearance and properties."""

        if self.scene.scroll_to_left == True:
                self.dx = - (self.scene.speed + self.scene.wave_number+5) 
        else: self.dx = (self.scene.speed + self.scene.wave_number+5)
        self.dy = 0
        self.determine_movement() 
        self.frame = random.randrange(0,3)
        self.dead = False
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
        if self.scene.scroll_to_left :
            self.rect.x =  self.scene.field_length  +1
        else: 
            self.rect.centerx = -1
        self.rect.centery = random.randrange(self.size[0],
                                             (self.screen.get_height()-self.size[1]))
        self.startmovement = random.randrange\
                            (0,(self.scene.field_length)- (self.scene.wave_number* 60))\
                            
       