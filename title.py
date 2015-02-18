'''
Created on Aug 11, 2014

@author: DemiCow
'''
import pygame
import scene
import squid
import label
import prepare

class Title(scene.Scene):
    
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "INTRO"
        self.init_variables()
        self.init_objects()   
    
    def init_variables(self):
        self.click_time = self.time - 100
        self.collision_time = -100
        self.shield_time = -100
    
    def init_objects(self):
        """ creates objects needed in specfic scenes"""        
        self.background_music =  pygame.mixer.Sound(prepare.SOUNDS['freefade'])
        if pygame.mixer.get_busy() == False and prepare.MUSIC_ON == True:
            self.background_music.play(loops= -1)                 
        self.speed = self.MASTER_SPEED
        self.scroll_to_left = None
        
        self.squid = squid.Squid(self)
        self.squid.rect.center = (600,400)
        self.squid.currentimage = self.squid.imgtitle
        self.squid.dy = 0
        #self.squid.delay = 12
        self.squid.number_of_frames = 9
        self.label = label.Label(self)
        self.label.textlines = ["it has a squid in it"]
        self.menu = label.Label(self, font_size = 50)
        self.menu_phase = 0
        self.set_menu_lines()
        
        self.menu.clickable = True
        self.menu.rect.y += 300
        self.background = pygame.Surface(self.screen.get_size())
        self.backgroundrect = self.background.get_rect()
        self.background.fill(pygame.color.Color("black"))
        self.screen.blit(self.background, (0, 0))
        self.sprites = [self.label, self.menu,self.squid]
        
        self.click_sound = pygame.mixer.Sound(prepare.SOUNDS['157539__nenadsimic__click'])        
               
        
    def startup(self, time, persistant): 
        self.start_time = time    
        if prepare.MUSIC_ON == True:
            self.background_music.play(loops= -1)      
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
    
    def set_menu_lines(self):        
        options_dict = {True: "on", False: "off"}
        self.menu.image.fill(self.menu.fillcolor)
        if self.menu_phase == 0:
            if self.android:
                self.menu.textlines = ["touch to begin", "options"]
            else: self.menu.textlines = ["click to begin", "options"]
        elif self.menu_phase == 1:
            self.menu.textlines = ["music {0}".format(options_dict[prepare.MUSIC_ON]), "back"]            
           
    def mouse_controls(self, time_delta):        
        "make squid follow cursor"
        focuspos = pygame.mouse.get_pos()
        diffx =  (self.squid.rect.center[0] - focuspos[0])
        if abs(diffx) > 50:
            self.squid.dx += -int (diffx* .1)
        else: self.squid.dx = 0
          
    
    def fill_background(self):
        self.screen.blit(self.background, (0, 0))
        
    def toggle_music(self):
        
        music_on = prepare.MUSIC_ON
        if music_on ==True:
            prepare.MUSIC_ON = False
            self.background_music.stop()
        elif music_on == False:
            prepare.MUSIC_ON = True
            if pygame.mixer.get_busy() == False:
                self.background_music.play(loops= -1)   
            
                    
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
                
        if self.clicked ==True and self.time - self.click_time > self.short_time* time_delta:        
            if self.menu_phase == 0:
                if self.menu.option_highlighted == 0:
                    if prepare.MUSIC_ON == True:
                        self.click_sound.play()
                        pygame.mixer.stop()              
                    self.done = True
                elif self.menu.option_highlighted == 1:                    
                    self.menu_phase = 1                    
                    self.set_menu_lines()
            elif self.menu_phase == 1:
                if self.menu.option_highlighted == 0:
                    self.toggle_music()                    
                    self.set_menu_lines()
                elif self.menu.option_highlighted == 1:
                    self.menu_phase = 0
                    self.set_menu_lines()
            self.click_time= self.time
            
    
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
        