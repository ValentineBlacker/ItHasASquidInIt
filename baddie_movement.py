'''
Created on Oct 31, 2014

@author: DemiCow
'''
import random
import pycurve

class baddie_List:
    def __init__(self, scene, baddie_list, list_id):
        self.scene = scene
        self.baddie_list = baddie_list        
        self.list_id = list_id
        for x in self.baddie_list:
            x.list_id = self.list_id
            x.list_index = self.baddie_list.index(x)  
        self.reset()
        
    def update(self):      
        self.movement_counter += 1  
        if self.movement_counter > self.startmovement:
            #calculates when last member has gone offscreen
            if self.movement_counter - self.startmovement > (len(self.path)-1) + (len(self.baddie_list)-1) * 50 :
                self.reset()
                        
            else:
                for x in self.baddie_list:
                    if x.dead == False:
                        #make sure it's baddie's turn
                        if (self.movement_counter-self.startmovement)- self.baddie_list.index(x)*50 > 0  : 
                            #if baddie is at end of list, reset it
                            if (self.movement_counter-self.startmovement)- self.baddie_list.index(x)*50 > len(self.path)-1:
                                x.reset()
                            else: 
                                #else, put in proper spot on list
                                x.rect.x, x.rect.y = self.path[(self.movement_counter-self.startmovement)- self.baddie_list.index(x)*50]
                        
    def reset(self):
        self.paths = [pycurve.make_b_spline(self.scene,pycurve.PATHS[pycurve.PATHS.index(x)]) for x in pycurve.PATHS]
        self.path = self.paths[random.randrange(0,len(self.paths))]        
        self.startmovement = random.randrange\
                        (0,(self.scene.field_length*1.5)- (self.scene.wave_number* 50))          
        self.movement_counter = 0
        for x in self.baddie_list:
            x.dead = False    
                  
            x.reset()
            