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
    
MASTER_SPEED = 3

class Control(object):
    """Control class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here."""
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.state_dict = {}
        self.state_name = None
        self.state = None
        
        self.tick_speed = 35
        self.time = 0
        
        self.time = pygame.time.get_ticks()/self.tick_speed    
        
        
        img_icon = image.load("images/icon.png")
        display.set_icon(img_icon)
        display.set_caption("it has a squid in it")
        self.done = False 
    
    def setup_states(self, state_dict, start_state):
        """Given a dictionary of States and a State to start in,
        builds the self.state_dict."""
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]    
        
    def update(self):
        """Checks if a state is done or has called for a game quit.
        State is flipped if neccessary and State.update is called."""
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update()

    def flip_state(self):
        """When a State changes to done necessary startup and cleanup functions
        are called and the current State is changed."""
        previous,self.state_name = self.state_name, self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.time, persist)
        self.state.previous = previous
        
        
    def event_loop(self):
        """events- mouse click, escape to exit game. squid controlled by mouse if not android"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # event.key == pygame.K_ESCAPE or 
                self.done = True               
                #pygame.quit() 
                #if not android: 
                    #sys.exit(0) 
            
            self.state.get_event(event)
            
    def main(self):
        """Main loop for entire program."""
        while not self.done:
            self.event_loop()
            self.update()
            self.clock.tick(self.tick_speed)
            self.time = pygame.time.get_ticks()/self.tick_speed 
            pygame.display.flip()               
            if android:
                self.accelerometer() 
    
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
        
        pygame.mixer.init()
        
        self.start_time = 0
        self.time = 0
        resolution = (1280, 768)
        self.screen = pygame.display.set_mode(resolution)
        self.screen_center = ((resolution[0]/2), (resolution[1]/2))
        self.field_length = resolution[0]
        self.field_height = resolution[1]
        self.fullscreen = 0
        self.screen_center = ((resolution[0]/2), (resolution[1]/2))
       
        self.MASTER_SPEED = MASTER_SPEED
        #camera determines what's visible and what's off screen
        self.camera = self.screen.get_rect()
                 
        #pygame.key.set_repeat(500, 500)      
        self.sprites = []
        self.maps = []
        self.groups = []
        self.init_variables()
        self.init_objects()   
        self.clicked = False
        
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}
        
    def startup(self, time, persistant):
        """Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time."""
        self.persist = persistant
        self.time = time
            
    def cleanup(self):
        """Add variables that should persist to the self.persist dictionary.
        Then reset State.done to False."""
        self.done = False
        return self.persist
        
    def get_event(self, event):
        """Processes events that were passed from the main event loop.
        Must be overloaded in children."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.vibrate(.1)
            self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
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
                   

    def update(self):
        self.fill_background()
        for sprite in self.sprites:
            sprite.update()        
        self.mouse_controls()
        self.update_specifics()
        
    def update_specifics(self):
        pass
        
    
    def mouse_controls(self):
        pass
  
    

