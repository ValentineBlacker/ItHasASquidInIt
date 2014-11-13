'''
Created on Aug 11, 2014

@author: DemiCow
'''
import pygame
import scene
import squid
import label

class Title(scene.Scene):
    
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "INTRO"
    
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        self.speed = self.MASTER_SPEED
        self.scroll_to_left = None
        self.collisiontimer = 0
        self.shield_counter = 0
        self.squid = squid.Squid(self)
        self.squid.rect.center = (600,400)
        self.squid.currentimage = self.squid.imgtitle
        self.squid.dy = 0
        #self.squid.delay = 12
        self.squid.number_of_frames = 9
        self.label = label.Label(self)
        self.label.textlines = ["it has a squid in it"]
        self.menu = label.Label(self, font_size = 50)
        if self.android:
            self.menu.textlines = ["touch to begin"]
        else: self.menu.textlines = ["click to begin"]
        self.menu.clickable = True
        self.menu.rect.y += 300
        self.background = pygame.Surface(self.screen.get_size())
        self.backgroundrect = self.background.get_rect()
        self.background.fill(pygame.color.Color("black"))
        self.screen.blit(self.background, (0, 0))
        self.sprites = [self.label, self.menu,self.squid]
        self.click_sound = pygame.mixer.Sound('sounds/157539__nenadsimic__click.wav')
        
        
    def startup(self, time, persistant):
        self.init_objects()
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
        
    def mouse_controls(self, time_delta):        
        "make squid follow cursor"
        focuspos = pygame.mouse.get_pos()
        diffx =  (self.squid.rect.center[0] - focuspos[0])
        if abs(diffx) > 50:
            self.squid.dx += -int (diffx* .1)
        else: self.squid.dx = 0
          
    
    def fill_background(self):
        self.screen.blit(self.background, (0, 0))
        
                    
    def update_specifics(self, time, time_delta):       
        """update title screen"""         
        self.squid.currentimage = self.squid.imgtitle    
        if self.android:
            self.squid.dx = self.accelerometer()[0]
        if self.squid.rect.right> self.label.rect.right:
            if self.squid.dx > 0:
                self.squid.dx = 0
            else: pass
        if self.squid.rect.left < self.label.rect.left: 
            if self.squid.dx < 0:
                self.squid.dx = 0
            else: pass
        
        if self.clicked ==True:
            if self.menu.option_highlighted == 0:
                self.click_sound.play()
                self.done = True
        
        
    
def main():
    import gameplay
    import cutscene
    run_it = scene.Control()
    state_dict = {"TITLE" : Title(),
                  "INTRO" : cutscene.Cutscene0(),
                  "GAMEPLAY" : gameplay.gamePlay(),
                  "ENDING": cutscene.Cutscene1()
                   }
    run_it.setup_states(state_dict, "TITLE")
    run_it.main()   
    
if __name__ == "__main__":
    main()
        