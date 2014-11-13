'''
Created on Sep 13, 2014

@author: DemiCow
'''

import pygame
import scene
import label
import maphandler
import squid

class Cutscene0(scene.Scene):
    
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "GAMEPLAY"
    
    def init_variables(self):
        """ init all variables needed in scene"""
        self.speed = self.MASTER_SPEED
        self.scroll_to_left = True
        
        self.title_time = self.time      
        self.wave_number = 0
        self.collisiontimer = 0
        self.shield_counter = 0
        self.click_counter = 5
        self.text_delay = 100
        self.secret_line = True
                     
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        
        self.squid = squid.Squid(self)
        self.squid.rect.y += 325
        
        self.foreground_map = maphandler.ScrollingMap(self, 'splash')
        self.maps = [self.foreground_map]  
        
        self.ocean_noises =  pygame.mixer.Sound('sounds/31762__slanesh__ocean.wav')
        self.seagull_noises =  pygame.mixer.Sound('sounds/144836__eelke__sea-seagulls-crows-windfilter.wav')
        
        
        self.tutorial = label.Label(self, size = (800,150), location = (800,150), font_size = 20)
        if self.android:
            self.tutorialtext = [['Welcome to "it has a squid in it".', 'touch to skip'],
                                 ['this squid is going', 'on a journey', 'your task is to guide him'],
                                  ['what will you find', 'at the end?'],
                                  ['tilt to move around', 'eat shrimp for a power-up'],
                                  ['hit those who would stand in your way', 'with ink bullets'],
                                  ['target groups for', 'a combo bonus.'],
                                  ['when you run out of lives, your',' journey is over. good luck!'],
                                  ['"Fate is a sea without shore, and the soul is a rock that abides;',
                                   '"But her ears are vexed with the roar and her face with the foam of the tides."',
                                   "- Swinburne"]
                                  ]
            
        else: 
            self.tutorialtext = [['Welcome to "it has a squid in it".', 'click to skip'],
                                 ['this squid is going', 'on a journey', 'your task is to guide him'],
                                  ['what will you find', 'at the end?'],
                                  ['use the mouse pointer to move around', 'eat shrimp for a power-up'],
                                  ['hit those who would stand in your way', 'with ink bullets'],
                                  ['target groups for', 'a combo bonus.'],
                                  ['when you run out of lives, your',' journey is over. good luck!'],
                                  ['"Fate is a sea without shore, and the soul is a rock that abides;',
                                   '"But her ears are vexed with the roar and her face with the foam of the tides."',
                                   "- Swinburne"]
                                  ]
            
        self.linecounter = 0
       
        self.tutorial.textlines = self.tutorialtext[0]
        self.tutorial.clickable = False
        self.tutorial.textcolor = (pygame.color.Color("black"))
        self.tutorial.backgroundcolor = self.tutorial.transparent_color
        
        self.sprites = [self.foreground_map, self.squid,  
                        self.tutorial]  
        
    def startup(self, time, persistant):
        self.init_objects()
        self.ocean_noises.play()
        self.seagull_noises.play()
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
         
       
    def update_specifics(self, time, time_delta):               
        self.click_counter -= 1
        self.squid.dx = self.squid.dy = 0
        self.squid.currentimage = self.squid.imgsquidge
        
        if self.click_counter%2 == 0:
            self.squid.rect.x += 2
            self.squid.rect.y += 1
        else: pass
        
        if self.secret_line == True:
            if self.clicked == True:
                self.tutorialtext = self.tutorialtext[:-1]
                self.secret_line = False
                print self.tutorialtext
        
        if self.clicked ==True and self.click_counter < 0 or self.click_counter < -self.text_delay:
                self.click_counter = 30   
                self.linecounter += 1                 
                if self.linecounter == len(self.tutorialtext):
                    self.ocean_noises.fadeout(1000)
                    self.seagull_noises.fadeout(1000)
                    self.done = True
                else:
                    self.tutorial.image.fill(self.tutorial.fillcolor)
                    self.tutorial.textlines = self.tutorialtext[self.linecounter]
                    
                
class Cutscene1(scene.Scene):
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "TITLE"

    
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        self.speed = self.MASTER_SPEED
       
        self.label = label.Label(self, font_size = 50)
        self.label.textlines = ["THANK YOU FOR PLAYING", "IT HAS A SQUID IN IT"]
        self.menu = label.Label(self, font_size = 50)
        if self.android:
            self.menu.textlines = ["touch to go back to title"]
        else: self.menu.textlines = ["click to go back to title"]
        self.menu.clickable = True
        self.menu.rect.y += 300
        self.background = pygame.Surface(self.screen.get_size())
        self.backgroundrect = self.background.get_rect()
        self.background.fill(pygame.color.Color("black"))
        self.screen.blit(self.background, (0, 0))
        self.sprites = [self.label, self.menu]
        self.click_sound = pygame.mixer.Sound('sounds/157539__nenadsimic__click.wav')
        
        
    def mouse_controls(self, time_delta):
        pass
           
    
    def startup(self, time, persistant):
        self.init_objects()
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
           
    def fill_background(self):
        self.screen.blit(self.background, (0, 0))
                
    def update_specifics(self, time,time_delta):       
        """update title screen""" 
        if self.clicked ==True:
            if self.menu.option_highlighted == 0:
                self.click_sound.play()
                self.done = True
        
    
        
def main():
    import gameplay
    import title
    run_it = scene.Control()
    state_dict = {"TITLE" : title.Title(),
                  "INTRO" : Cutscene0(),
                  "GAMEPLAY" : gameplay.gamePlay(),
                  "ENDING": Cutscene1()
                   }
    run_it.setup_states(state_dict, "INTRO")
    run_it.main()   
    
if __name__ == "__main__":
    main()
        
        
