'''
Created on Aug 8, 2014

@author: DemiCow
'''
import pygame
import prepare

try:
    import android
except ImportError:
    android = None


class Squid(pygame.sprite.DirtySprite):

    def __init__(self, scene):
        """ intialize sprite class """
        pygame.sprite.DirtySprite.__init__(self)
        self.scene = scene
        self.screen = scene.screen     
        
        #default sprite attributes
        
        self.pause = 0
        self.frame = 0   
        self.delay = 800       
        self.imgsize = (75, 75)
        self.reset()        
        if android:
            android.accelerometer_enable(True)
            
    def reset(self):
        self.dx = 0
        self.dy = 0
        
        self.speed = 0        
        self.dirty = 2  
           
        self.number_of_frames = 4  
        self.load_images()

        self.image = self.imgstand
        self.mask = pygame.mask.from_surface(self.image)
        self.currentimage = self.imgmoving
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.inflate_ip(-10,-10)
        if self.scene.scroll_to_left:
            self.rect.center = (self.size[0],self.screen.get_height()/4)
        else:
            self.rect.center = (self.screen.get_width()- self.size[0],self.screen.get_height()/2)
             
        self.dead = False
        self.position = self.rect.center
      
        
        
    def load_images(self):        
        imagemaster = prepare.IMAGES['vampy']
        
        #standing still frame
        self.imgstand = pygame.Surface(self.imgsize, pygame.SRCALPHA)
        
        self.imgstand.blit(imagemaster, (0, 0), ((0,0), self.imgsize))
        
        
        
        #moving animation
        self.imgmoving= []
        offsetmoving = tuple((self.imgsize[0]*i,0) 
                             for i in xrange (4))
        for i in xrange(len(offsetmoving)):
            tmpimg = pygame.Surface(self.imgsize, pygame.SRCALPHA)
            tmpimg.blit(imagemaster, (0, 0), (offsetmoving[i], self.imgsize))            
            self.imgmoving.append(tmpimg)
            
        #dead image    
        self.imgdead = pygame.Surface(self.imgsize, pygame.SRCALPHA) 
        self.imgdead.blit(imagemaster, (0, 0), ((self.imgsize[0]*4,0), self.imgsize))
        
        #damage image    
        self.imgdamage = pygame.Surface(self.imgsize, pygame.SRCALPHA) 
        self.imgdamage.blit(imagemaster, (0, 0), ((self.imgsize[0]*4,self.imgsize[1]), self.imgsize))
        
        #moving animation w/ shield
        self.imgshield= []
        offsetshield = tuple((self.imgsize[0]*i,self.imgsize[1]) 
                             for i in xrange(4))
        for i in xrange(len(offsetshield)):
            tmpimg = pygame.Surface(self.imgsize, pygame.SRCALPHA)
            tmpimg.blit(imagemaster, (0, 0), (offsetshield[i], self.imgsize))            
            self.imgshield.append(tmpimg)
            
        #animation for titlescreen
        temptitle= []
        offsettitle = tuple((self.imgsize[0]*i,self.imgsize[1]*2) 
                            for i in xrange(5))
        for i in xrange(len(offsettitle)):
            tmpimg = pygame.Surface(self.imgsize, pygame.SRCALPHA)
            tmpimg.blit(imagemaster, (0, 0), (offsettitle[i], self.imgsize))  
            temptitle.append(tmpimg)
        reversetitle = temptitle[::-1]
        self.imgtitle = temptitle + reversetitle
        
        #walking animation for cutscene
        self.imgsquidge= []
        offsetsquidge = tuple((self.imgsize[0]*i,self.imgsize[1]*3) 
                             for i in xrange(5))
        for i in xrange(len(offsetsquidge)):
            tmpimg = pygame.Surface(self.imgsize, pygame.SRCALPHA)
            tmpimg.blit(imagemaster, (0, 0), (offsetsquidge[i], self.imgsize))            
            self.imgsquidge.append(tmpimg)
        
          
            
        
    def animation(self, time_delta):        
        self.pause += 1        
        if self.pause >= int(self.delay*time_delta):
            self.pause = 0
            self.frame += 1
            if self.frame >= self.number_of_frames:
                self.frame = 0               
        self.image = self.currentimage[self.frame]
        
    def update(self, time_delta):          
        
        self.check_bounds()
                                
        if self.dead == True:
            self.image = self.imgdead 
            self.rect.y += -1
            
        elif self.scene.time - self.scene.collision_time < self.scene.short_time*time_delta:
            if self.currentimage is not self.imgshield:            
                self.image = self.imgdamage                
            else: self.scene.collision_time = self.scene.time = 10000
        else:
            self.animation(time_delta)              
            if self.scene.time - self.scene.shield_time < (self.scene.long_time*2)*time_delta :    
                self.currentimage = self.imgshield                
            else: 
                self.currentimage = self.imgmoving
                self.scene.shield_time = self.scene.time - 100000
        self.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)  
            
    def check_bounds(self):    
        #Check Bounds. 
        screenwidth = self.scene.field_length
        screenheight = self.scene.field_height - self.size[0]
           

        if self.rect.x > screenwidth:            
            self.rect.x = screenwidth

        if self.rect.x < 0:
            self.rect.x = 0
            
        if self.rect.y >screenheight:            
            self.rect.y = screenheight

        if self.rect.y < 0:
            self.rect.y = 0

    def flip(self):
    
        self.image = pygame.transform.flip(self.image, True, False)

 

