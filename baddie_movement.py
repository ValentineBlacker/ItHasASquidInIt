'''
Created on Oct 31, 2014

@author: DemiCow
'''
import random
import prepare

class baddie_List:
    def __init__(self, scene, baddie_list, list_id):
        self.scene = scene
        self.baddie_list = baddie_list        
        self.list_id = list_id
        for x in self.baddie_list:
            x.list_id = self.list_id
            x.list_index = self.baddie_list.index(x)  
        self.reset()
        
           
    def update(self, time_delta):      
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
        magic_index = random.randrange(0, len(self.baddie_list)-1)
        self.path = prepare.PATHS[random.randrange(0,len(prepare.PATHS))]        
        self.startmovement = random.randrange\
                        (0,(self.scene.field_length*4)- (self.scene.wave_number* 50))   
        if self.scene.foreground_map.at_end == True:
            self.startmovement = self.startmovement * 2
                   
        self.movement_counter = 0
        for x in self.baddie_list:
            x.dead = False 
            x.magic_index = magic_index                     
            x.reset()
            