'''
Created on Aug 8, 2014

@author: DemiCow
'''

import pygame 
from pygame import display, image


# Import the android module. If we can't import it, set it to None - this
# lets us test it, and check to see if we want android-specific behavior.
try:
    import android
except ImportError:
    android = None
    import sys



class Scene(object):
    def __init__(self):    
        """sets up things needed in all scenes. not meant to be used on its own."""    
        pygame.init()  
        #inits android if it's been imported            
        if android:
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
            self.android = android
        else: self.android = None
        
        self.MASTER_SPEED = 3
        self.tick_speed = 35
        pygame.mixer.init()
        
        resolution = (1280, 768)
        self.screen = pygame.display.set_mode(resolution)
        self.field_length = resolution[0]
        self.field_height = resolution[1]
        self.fullscreen = 0
        self.time = pygame.time.get_ticks()/self.tick_speed    
        self.screen_center = ((resolution[0]/2), (resolution[1]/2))
        #camera determines what's visible and what's off screen
        self.camera = self.screen.get_rect()
        img_icon = image.load("images/icon.png")
        display.set_icon(img_icon)
        display.set_caption("it has a squid in it")
         
        #pygame.key.set_repeat(500, 500)      
        self.running = True 
        self.scene_end = False        
        self.sprites = []
        self.maps = []
        self.groups = []
        self.init_variables()
        self.init_objects()   
        self.clicked = False
        
     
    def accelerometer(self):
        accelerometer = android.accelerometer_reading()
        y = float(accelerometer[0])
        x = float (accelerometer[1]) 
        #the 6 keeps it so you can hold the phone at a comfortable angle 
        dx = x/1          
        dy = (y/1) - 6         
        return (dx,dy)    
        
    def vibrate(self, duration):
        if self.android:
            self.android.vibrate(duration)    
        else: pass
           
    def fill_background(self):
        pass
        
    
    def init_variables(self):
        """ place to store all variables needed in scene"""
        pass
        
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        pass
    
    def level_transition(self):        
        """transition to next level/scene"""   
        self.stop()            
        self.nextlevel.start()
            
    def make_sprite_group(self, sprites):

        """ create a group called groupName
            containing all the sprites in the sprites 
            list.  This group will be added after the 
            sprites group, and will automatically
            clear, update, and draw
        """
        tempgroup = pygame.sprite.LayeredDirty(sprites)
        return tempgroup

    

    def add_group(self, group):

        """ adds a sprite group to the groups list for
            automatic processing 
        """
        self.groups.append(group)
        
    def start(self):
        """inits clock, starts main loop """
        self.clock = pygame.time.Clock()
        while self.running:
            self.mainLoop()
 
    def stop(self):
        """ ends main loop """
        self.running = False 
                  
    def mainLoop(self):
        """ main loop, also updates stuff that gets updated regardless of scene """
        self.clock.tick(self.tick_speed)
        self.time = pygame.time.get_ticks()/self.tick_speed
        self.fill_background()
        for sprite in self.sprites:
            sprite.update()
        self.update() 
        pygame.display.flip()             
        self.handle_events() 
        self.mouse_controls()
        if android:
            self.accelerometer() 
        if self.scene_end == True:
            self.level_transition()        
         
        
    
    def update(self):
        pass
    
    def mouse_controls(self):
        pass
  
    def handle_events(self):
        """events- mouse click, escape to exit game. squid controlled by mouse if not android"""
        for event in pygame.event.get():      
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.vibrate(.1)
                self.clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                        pygame.quit() 
                        if not android: 
                            sys.exit(0) 
    
                
    
        
     
        

