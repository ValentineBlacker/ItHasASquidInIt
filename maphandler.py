'''
Created on Aug 8, 2014

@author: DemiCow
'''
import pygame
import prepare
#CREDIT FOR PORTIONS OF MAP CODE: Christopher Breinholt (BreinyGames). 
#Link to orginal code not available.

imagedict = {0: 'sun', 1: 'moon', 2: 'mercury' , 3: 'venus', 4: 'mars', 5: 'jupiter', 6: 'saturn', 7: 'fixed_stars'}

class MapTile(pygame.sprite.DirtySprite):
    """create tile object used for map"""
    def __init__(self, image, x, y):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
class ScrollingMap:
    """Puts the map together and scrolls it horiziontally. 
    Map can be any number of tiles wide or high."""
    def __init__(self, scene, maptype):
        self.scene = scene  
        #this is the number of tiles making up the background- 0 for this game
        self.map_width, self.map_height = 4, 1
        self.screen = scene.screen
        self.maptype = maptype
        self.masterspeed = scene.MASTER_SPEED
        self.reset()
        
    def load_images(self):
        """Load map images depending on map type. Get tile size based on image size."""
        if self.maptype == 'background':           
            #background tile half the length of foreground tile, scrolls half as fast. 
            self.speed = (self.speed//2)
            self.tileset= prepare.MAPS['{0}background'.format(imagedict[self.scene.wave_number])]
            #pygame.image.load\
                            #("images/maps/{0}background.png".format 
                            #(imagedict[self.scene.wave_number])).convert_alpha()            
            
        elif self.maptype == 'foreground':  
            self.tileset = prepare.MAPS['{0}foreground'.format(imagedict[self.scene.wave_number])]
                            #pygame.image.load\
                            #("images/maps/{0}foreground.png".format 
                            #(imagedict[self.scene.wave_number])).convert_alpha()            
        
        elif self.maptype == 'splash':
            self.speed = 0
            self.tileset =  prepare.MAPS['cutscene{0}'.format(self.scene.wave_number)]

            
            #                              
            
        self.tile_size = self.tileset.get_size()    
        self.tile_size_x = self.tile_size[0]
        self.tile_size_y = self.tile_size[1]
         
    def reset(self):  
        """creates our map images"""   
        self.speed = self.masterspeed
        self.dx = 0 
        self.at_end = False   
        self.load_images()    
        self.tiles = []  
        if self.scene.scroll_to_left == True:
            starting_location = (0,0)        
            self.speed *= -1  
            
        else: 
            starting_location = (self.tile_size_x + 
                                   self.scene.field_length,0)
                   
        for y in range(0, self.map_height):
            for x in range(0, self.map_width):
                
                tile_image = pygame.surface.Surface(self.tile_size,
                                                     pygame.SRCALPHA)                
              
                tile_image.blit(self.tileset, (starting_location))
                self.tiles.append(MapTile
                                  (tile_image, x*self.tile_size_x, 
                                   y*self.tile_size_y))
        
               
    def check_visible(self, tile):
        "check that tile is visible on map"
        if tile.rect.right < 0 or tile.rect.left > self.scene.field_length:
            return False
        else: return True
        
    def evaluate_endpoint(self):
        "returns TRUE if map is not at end, FALSE if it is not."
        if self.scene.scroll_to_left == True:
            if self.tiles[len(self.tiles)-1].rect.right> self.scene.field_length:
                return True
            else: return False
            
        else:
            if self.tiles[len(self.tiles)-1].rect.left < 0:
                return True
            else: return False

    def update(self, time_delta):  
        """"Scroll tiles, draw to screen."""
        
        if self.maptype == 'foreground':
            if self.evaluate_endpoint()== True:
                self.dx = self.speed*3
            else: 
                self.dx = 0
                self.at_end = True
            
        elif self.maptype == 'background':
            if self.evaluate_endpoint()== True and self.scene.foreground_map.dx is not 0:
                self.dx = self.speed
            else: self.dx = 0
        
        for tile in self.tiles: 
            tile.rect.x += int(self.dx* time_delta)  #this must be an int          
            if self.check_visible(tile) == True:
                self.screen.blit(tile.image, (tile.rect.x , tile.rect.y), 
                                 (0, 0, self.tile_size_x, self.tile_size_y))