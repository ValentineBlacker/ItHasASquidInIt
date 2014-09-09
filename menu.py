'''
Created on Aug 8, 2014

@author: DemiCow
'''

import scene, squid

class Menu(scene.Scene):
    
           
        
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        self.squid = squid.Squid(self)
        self.sprites = [self.squid]
    

       
    def update(self):
          
        if self.mousebuttonpressed == True:
            from gameplay import gamePlay
            self.next_level = gamePlay
            self.level_transition()
