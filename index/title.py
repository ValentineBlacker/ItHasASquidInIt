'''
Created on Aug 11, 2014

@author: DemiCow
'''
import pygame
import scene
import squid
import label

class Title(scene.Scene):
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
        self.squid.delay = 12
        self.squid.number_of_frames = 5
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
        self.squid.number_of_frames = 9
        
    
    def start_game(self):
        from gameplay import gamePlay
        self.nextlevel = gamePlay()
        self.level_transition()
                                 
    def keyboard_controls(self, event):
        """Enter or click starts game. Arrows move squid back and forth."""
        if event.key == pygame.K_RETURN :
            self.start_game()
        if event.key == pygame.K_LEFT: 
            self.squid.dx = self.squid.dx - 1 
        if event.key == pygame.K_RIGHT:
            self.squid.dx = self.squid.dx +1
            
    def mouse_controls(self):
        if self.clicked ==True:
            if self.menu.option_highlighted == 0:
                self.start_game()
        posx = pygame.mouse.get_pos()[0]
        posy = pygame.mouse.get_pos()[1]
        if self.time % 6 == 0:
            if posx < self.squid.rect.x:               
                if posy  > self.squid.rect.top and posy < self.squid.rect.bottom :       
                    self.squid.dx = self.squid.dx - 1         
                    return 'left'
            elif posx >  self.squid.rect.x:
                if posy  > self.squid.rect.top and posy < self.squid.rect.bottom:    
                    self.squid.dx = self.squid.dx + 1 
    
    def fill_background(self):
        self.screen.blit(self.background, (0, 0))
                
    def update(self):       
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
        self.squid.dy = 0
        
        
    
def main():
    game = Title()
    game.start()
if __name__ == "__main__":
    main()
        