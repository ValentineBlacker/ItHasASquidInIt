'''
Created on Aug 11, 2014

@author: DemiCow
'''
import pygame
import baddie
import prepare
import math

class Boss(baddie.Baddie):

    def __init__(self, scene):
        """ intialize sprite class """
        pygame.sprite.DirtySprite.__init__(self)
        self.scene = scene
        self.screen = scene.screen   
        #default sprite attributes
        self.pause = 0
        self.frame = 0   
        self.sine_variables()
        self.delay = 500 
        self.reset()
        
    def load_images(self):
        #self.imgmaster= pygame.image.load("images/bosses/boss{0}.png".format (self.scene.wave_number))        
        #self.imgmaster = self.imgmaster.convert_alpha()
        self.imgmaster = prepare.BOSSES['boss{0}'.format(self.scene.wave_number)]
       
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
        
    def reset(self):
        self.speed = 0        
        self.dx = 0
        self.hit = False
        self.pause = 0
        self.frame = 0
        self.hp = (self.scene.wave_number*5)+ 20
        self.image_size = (500,500)
        self.number_of_frames = 8        
        self.load_images()        
        self.image = self.imgstand
       
        self.currentimage = self.imgmoving
        self.rect = self.image.get_rect()     
        self.mask = pygame.mask.from_surface(self.image)
        self.shootable = False
        self.size = self.image.get_size()
        if self.scene.scroll_to_left :
            self.rect.left =  self.scene.field_length - 20
        else: 
            self.rect.right = -20
        self.rect.bottom = self.scene.field_height - 100
        
        self.movement_length = 200
        self.movement_count = self.movement_length  
        
    
    def movement(self):
        "moves boss back and forth"
        if self.movement_count <= self.movement_length  and self.movement_count >= 100:  
            return -4#self.scene.speed
        elif self.movement_count <= 0 and self.movement_count >= -self.movement_length +100 :
            return 4#self.scene.speed
        else: return 0
    
    def sine_variables(self):
        self.sinpause = 0     
        self.sinframe = 0    
        
    def sine_wave(self, delay = 50, modifier = 6):        
        #frame is x. yposition = sin(x)
        self.sinpause += 1
        if self.sinpause >= delay:
            self.sinpause = 0
            self.sinframe += 1
            if self.sinframe >= 50:
                self.sinframe = 0           
        dy = int(-(modifier*(math.sin)(self.sinframe))) 
        return dy #*20 (* time_delta)
       
    def die(self):
        """if curent image is dead, moves self offscreen after animation plays."""
        if self.frame >= self.number_of_frames-1:
            self.rect.x = -1000
                
    def update(self, time_delta):
        
        if self.currentimage == self.imgdead:
            self.die()
        if self.scene.foreground_map.at_end == True:
            
            if self.scene.scroll_to_left == True and self.rect.right > self.scene.field_length:
                self.dx = -self.scene.speed
            elif self.scene.scroll_to_left == False and self.rect.left < 0:
                self.dx = self.scene.speed
            elif self.currentimage is not self.imgdead: 
                self.dx = self.movement()
                self.shootable = True
                if self.movement_count< -self.movement_length :
                    self.movement_count = self.movement_length
                self.movement_count -=1 #* time_delta                          
            self.rect.x += self.dx#* time_delta
            self.rect.y += self.sine_wave(self.scene.wave_number*10 + 10)#bottom = self.sine_wave() + (self.scene.field_height - 100)
            #the order here is important or the collidemask won't work for the flipped sprite
            self.animation(time_delta)
            if self.scene.scroll_to_left :
                self.flip()
            self.mask = pygame.mask.from_surface(self.image)
            if self.hit == True and self.shootable == True:
                self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)
                self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 2) 
                self.hit = False
            else: self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)
        else: pass
        