'''
Created on Aug 8, 2014

@author: DemiCow
'''

import pygame, prepare

class Label(pygame.sprite.DirtySprite):    
    """label class prints text on screen. You can change size and color no problem."""
    def __init__(self, scene, size = (700,200), location = (600,300), 
                 font_size = 72, font_name = prepare.FONT):
        
        pygame.sprite.DirtySprite.__init__(self)     
        self.scene = scene 
        self.int_to_roman = {0: 'zero', 1: "one", 2: 'two', 3: "three", 4: "four",
                             5: "five", 6: "six", 7: "seven", 8: "eight"}
        self.font = pygame.font.Font(font_name, font_size)
        self.textlines = ["wooooo"]
        self.transparent_color = pygame.color.Color("gray8")
        self.textcolor = (pygame.color.Color("darkred"))
        self.backgroundcolor = (pygame.color.Color("black"))     
        self.highlightcolor = (pygame.color.Color("white"))
        self.fillcolor = (self.transparent_color)
        self.image = pygame.Surface(size)
        self.image = self.image.convert()
        
        self.image.set_colorkey(self.transparent_color)
        self.image.fill(self.fillcolor)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.visible_location = location
        self.bordercolor = (pygame.color.Color("black"))
        self.border_on = False 
        self.clickable = False
        self.option_rects()
        self.option_highlighted = None
        self.visible = True
        
    def toggle_visible(self, visible):
        "toggles visiblity, also refills background to overwrite previous text"
        if visible == True:
            self.rect.center = self.visible_location
            self.image.fill(self.fillcolor)
            self.visible = True
        elif visible == False:
            self.rect.center = (5000,5000)
            self.visible = False
            
    def option_rects(self):
        "allows clicking on different lines to select options in menu"
        lefthandcorner = (self.rect.left,self.rect.top)
        
        self.rectlist = []
        self.rect = self.image.get_rect()
        self.rect.centerx = lefthandcorner[0] + self.rect.width/2
        self.rect.centery = lefthandcorner[1] + self.rect.height/2
        
        for i in range  (len(self.textlines) ):
            temprect = pygame.Rect(self.rect.left, self.rect.top + (i * (self.rect.height/len(self.textlines))), 
                                   self.rect.width, self.rect.height/len(self.textlines))
            self.rectlist.append(temprect) 
        
    def get_mouse_collision(self, rect):      
        return   rect.collidepoint(pygame.mouse.get_pos()) 
    
    def get_highlighted_option(self):
        for t in range(len(self.rectlist)):
            if self.get_mouse_collision(self.rectlist[t]):                  
                self.option_highlighted = t
            elif self.get_mouse_collision(self.rect) == 0:
                self.option_highlighted = None
       
    def update(self, time_delta):
        #change any color to PINK to make that part transparent.
        #border defaults to transparent    
        #add self.backgroundcolor to this to have a bg color
        if self.visible == True:
         
            numlines = len(self.textlines)
            vSize = self.image.get_height() / numlines
            
            if self.clickable == True:
                self.option_rects()
                self.get_highlighted_option()
            for linenum in range(numlines):
                currentLine = self.textlines[linenum]
                #add self.backgroundcolor to this to have a bg color
                if self.option_highlighted == linenum:
                    fontsurface = self.font.render(currentLine, True, self.highlightcolor, self.backgroundcolor)
                else:
                    fontsurface = self.font.render(currentLine, True, self.textcolor, self.backgroundcolor)            
                #center the text
                xpos = (self.image.get_width() - fontsurface.get_width())/2
                yPos = (linenum * vSize)            
                self.image.blit(fontsurface, (xpos, yPos), special_flags= 0)  
            self.scene.screen.blit(self.image, (self.rect.x, self.rect.y), special_flags= 0)
            
            
            if self.border_on:
                pygame.draw.rect(self.scene.screen, self.bordercolor, (self.rect), 5)  
        else: pass
                
                