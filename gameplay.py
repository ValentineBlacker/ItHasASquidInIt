'''
Created on Aug 8, 2014

@author: DemiCow
'''


import pygame
import scene
import squid
import baddie
import boss
import lifedot
import bullet
import powerup
import maphandler
import label
import baddie_movement
import prepare


#TODO:
#make enemy movement work with time_delta
# BOSS MOVEMENT
#DIFFICULTY SHOULD INCREASE
#instructions in options?

#put all music in startup EXCEPT that for first scene.





class gamePlay(scene.Scene):
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "ENDING"
        self.init_variables()
        self.init_objects()   
        
       
    def init_variables(self):
        """ init all variables needed in scene"""
        self.speed = self.MASTER_SPEED * 3
        self.scroll_to_left = True
        self.number_of_baddies = 100
        
        self.number_of_powerups = 3
        self.number_of_bullets = 30
        self.wave_number = 0
        #the shooting speed number is the delay between bullets. a LOWER number means the bullets fire faster.
        self.shooting_speed = self.long_time/2
        self.default_shooting_speed = self.shooting_speed 
        self.powerup_shooting_speed = self.shooting_speed / 10 #also the minimum speed           
        self.shooting_difference = self.shooting_speed - self.powerup_shooting_speed
        print self.shooting_difference
        self.maxlife = 3
        self.life = self.maxlife
        self.bullet_order = 0
        #timers!
        self.shield_time = self.time - 100000   
        self.collision_time = self.time-5000
        self.bullet_time = self.time      
        self.bullet_power_time = self.time  - 100000                
        
        self.boss_dead = False
        self.squid_controllable = False
        
        self.start_time = self.start_time + self.short_time/2
                                                            
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        self.background_songs = ['precipice', 'call', 'hack attack', 'tilt', 'depths', 'drive me',
                                  'rolling on', 'wormhole', 'oomph', 'ourou', 'try', 'jumpstyle', 'laconia',
                                  'oceania', 'freefade']
        self.baddie_damage_sound = pygame.mixer.Sound(prepare.SOUNDS['34172__glaneur-de-sons__woosh-02'])
        self.squid_damage_sound = pygame.mixer.Sound(prepare.SOUNDS['92736__robinhood76__01522-swoosh-1'])
        self.powerup_sound = pygame.mixer.Sound(prepare.SOUNDS['174462__yottasounds__power-up-001'])
            
        self.squid = squid.Squid(self)
        
        self.background_map = maphandler.ScrollingMap(self, 'background')
        self.foreground_map = maphandler.ScrollingMap(self, 'foreground')
        self.maps = [self.background_map, self.foreground_map]  
        
        self.baddies = [baddie.Baddie(self) for n in xrange(self.number_of_baddies)]           
        self.baddieGroup = self.make_sprite_group(self.baddies)
        self.add_group(self.baddieGroup)        
        self.create_baddie_lists()
        
        self.powerups = [powerup.Powerup(self) for n in xrange(self.number_of_powerups)]        
        self.powerupGroup = self.make_sprite_group(self.powerups)
        self.add_group(self.powerupGroup)    
        
        self.bullets = []#[bullet.Bullet(self) for n in xrange(self.number_of_bullets)]      
        self.bulletGroup = self.make_sprite_group(self.bullets)
        self.add_group(self.bulletGroup)
        
        self.hudrect = pygame.rect.Rect(10,10,100,40)
        self.lifedots = [lifedot.LifeDot(self, n) for n in range(self.maxlife)]        
        self.lifeGroup = self.make_sprite_group(self.lifedots)
        self.add_group(self.lifeGroup)  
              
        
        self.label = label.Label(self)
        self.label.textlines = ["sphere {0}".format(self.label.int_to_roman[self.wave_number])]
        self.label.backgroundcolor = self.label.transparent_color
        
        self.continuelabel = label.Label(self,(700,200), (600,400),50)
        self.continuelabel.textlines = ["continue", "quit"]
        self.continuelabel.backgroundcolor = self.continuelabel.transparent_color
        self.continuelabel.clickable = True
        self.continuelabel.toggle_visible(False)
        
        
        
        self.scorelabel = label.Label(self, (120,40), (self.field_length- 80, 40),24)
        self.scorelabel.backgroundcolor = self.scorelabel.transparent_color
        self.scorelabel.border_on = True
        self.scorelabel.textcolor = (pygame.color.Color("black"))
        self.score = 0
        self.scorelabel.textlines =[' %0*d' % (5, self.score)]
                
        #self.boss = boss.Boss(self)
        self.boss = None
              
        self.sprites = [self.background_map, self.foreground_map, self.squid,  self.baddieGroup,  
                        self.powerupGroup, self.bulletGroup, self.lifeGroup, self.label, self.scorelabel,self.continuelabel]  
        
                
       
        
    def create_baddie_lists(self):
        self.baddie_lists = []
        b_l = [self.baddies[x*5:(x*5)+ 5] for x in range(len(self.baddies)/5)]
        for b in b_l:
            self.baddie_lists.append(baddie_movement.baddie_List(self,b,b_l.index(b))    )      
                
                
    def startup(self, time, persistant):        
        self.start_time = time 
        self.set_music()    
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
    
    def set_music(self):
        if prepare.MUSIC_ON == True:
            self.background_music = pygame.mixer.Sound(prepare.SOUNDS[self.background_songs[self.wave_number]])              
            self.background_music.play(loops=-1)
    
        
    def detect_baddie_collisions(self, time_delta):
        "detects collision between baddies and squid"
        collidedbaddie = pygame.sprite.spritecollideany(self.squid, self.baddieGroup)
        if collidedbaddie and collidedbaddie.currentimage is not collidedbaddie.imgdead and self.squid_controllable == True:
            if self.time- self.collision_time > self.short_time*time_delta:
            #if self.collisiontimer <= 0:                
                self.vibrate(.3)
                self.collisiontimer = self.MASTER_SPEED
                collidedbaddie.frame = 0
                collidedbaddie.currentimage = collidedbaddie.imgdead
                self.hurt_squid(time_delta)
                self.collision_time = self.time            
        
            
    def hurt_squid(self, time_delta):      
        "hurts squid, kills it if life goes BELOW 0"  
        self.squid.dx = self.squid.dy = 0
        if self.squid.currentimage is not self.squid.imgshield: 
            self.life = self.life - 1
            if prepare.MUSIC_ON == True:
                self.squid_damage_sound.play()
            if self.life> -1:
                self.lifedots[self.life].kill()
            self.shooting_speed = self.default_shooting_speed
            if self.life < 0 and self.squid_controllable == True:
                self.squid_killed()            
                        
    def detect_powerup_collisions(self, time_delta):
        "detects collision between squid and powerup"
        collidedpowerup = pygame.sprite.spritecollideany(self.squid, self.powerupGroup)
        if collidedpowerup:
            if self.time- self.collision_time > self.short_time*time_delta:
                if prepare.MUSIC_ON == True:   
                    self.powerup_sound.play() 
                self.vibrate(.2)
                self.collision_time = self.time  
                if collidedpowerup.color == 'blue':  
                    if self.life < self.maxlife:
                        self.life = self.life + 1
                        self.lifeGroup.add(self.lifedots[self.life-1])
                elif collidedpowerup.color == 'red':
                    self.bullet_power_time = self.time
                    #self.bullet_powerup_timer = self.speed * 4        
                elif collidedpowerup.color == 'yellow':     
                    self.shield_time = self.time                          
                collidedpowerup.reset()
                
                      
            
    def detect_boss_collision(self, time_delta):
        "detects collision between boss and squid using mask."
        collision = pygame.sprite.collide_mask(self.squid, self.boss)
        if collision and self.boss.currentimage is not self.boss.imgdead and self.squid_controllable == True:
            if self.time- self.collision_time > self.short_time*time_delta:               
                self.vibrate(.3)
                self.collision_time = self.time  
                self.hurt_squid(time_delta)
        
        
    def squid_killed(self): 
        "when main character dies, kill it and display continue menu."
        self.squid_controllable = False    
        self.squid.dead = True 
        self.label.toggle_visible(True)
        self.label.textlines = ["it HAD a squid in it"]
        self.start_time= self.time
        
        self.continuelabel.toggle_visible(True)
        
    def handle_bullets(self, time_delta):
        "fires bullets in bullet list on a delay"
        if self.time - self.bullet_time > self.shooting_speed*time_delta  and self.squid_controllable == True:               
            newbullet = bullet.Bullet(self)#self.bullets [self.bullet_order]   
            self.bulletGroup.add(newbullet)             
            #bullet._set_visible(True)           
            newbullet.is_fired (self.squid.rect.centerx, self.squid.rect.centery, time_delta)                 
           
            if self.time - self.bullet_power_time > (self.long_time*4) * time_delta:
                self.bullettimer = self.shooting_speed * time_delta
                self.bullet_time = self.time
            else: 
                self.bullettimer = self.powerup_shooting_speed  * time_delta              
                self.bullet_time = self.time
        elif self.squid_controllable == False:
            pass
            
                     
    def bullet_baddie_collision(self, time_delta):
        """checks to see if bullet has llided with an enemy. Sets enemy to dead."""
        for b in self.bulletGroup:
            collidedbaddie = pygame.sprite.spritecollideany(b,self.baddieGroup)
            if collidedbaddie and collidedbaddie.check_bounds() == True\
             and collidedbaddie.currentimage is not collidedbaddie.imgdead:   
                collidedbaddie.hp -= 1  
                collidedbaddie.hit = True
                self.vibrate(.1) 
                if prepare.MUSIC_ON == True:
                    self.baddie_damage_sound.play()
                self.increment_score('baddie')
                b.kill()
                if collidedbaddie.hp <= 0:
                    self.kill_baddie(collidedbaddie, time_delta)
                    self.check_for_combo(collidedbaddie)
                                  
    def check_for_combo(self, collidedbaddie):
        """kills other enemies in same line as enemy killed."""        
        if collidedbaddie.list_index == collidedbaddie.magic_index:
            for b in self.baddies:
                if b.list_id == collidedbaddie.list_id: 
                    if b.currentimage is not b.imgdead:
                        self.kill_baddie(b)
                        #this is a score bonus
                        self.increment_score('baddie')
                       
    def kill_baddie(self, baddie, time_delta):
        """called when baddie HP is 0"""
        baddie.frame = 0
        baddie.currentimage = baddie.imgdead
        if self.shooting_speed > self.powerup_shooting_speed:
            self.shooting_speed -= (self.shooting_difference/20)* time_delta
        else: pass
    
    def bullet_boss_collision(self):
        """checks to see if bullet has collided with a boss. """
        if self.boss is not None:
            for b in self.bulletGroup:
                collision = pygame.sprite.collide_mask(b, self.boss) 
                if collision:
                    self.boss.hp -= 1  
                    self.boss.hit = True 
                    self.vibrate(.1) 
                    b.kill()#reset()
                    if self.boss.hp <= 0:
                        self.start_time = self.time
                        self.if_boss_dead()
                        self.ending_label()
                    
    def ending_label(self):
        self.label.textlines = ["sphere cleared", "score = {0}".format(self.score)]
        self.label.toggle_visible(True)
    
    def increment_score(self, enemy_type):
        """raises score, refreshes score box"""
        if enemy_type == 'baddie':
            self.score += 10
        elif enemy_type == 'boss':
            self.score += 50
        
        self.scorelabel.image.fill(self.scorelabel.fillcolor)
        self.scorelabel.textlines =[' %0*d' % (5, self.score)]
    
    def new_wave(self, wave_number):   
        """resets everything between waves"""
        self.wave_number = wave_number
        self.start_time = self.time 
        self.label.toggle_visible(True)
        self.squid.dead = False
        self.boss_dead = False                
        self.label.textlines = ["sphere {0}".format(self.label.int_to_roman[self.wave_number])]
        resetlist = self.maps + self.baddies + self.powerups +  self.baddie_lists
        for r in resetlist:
            r.reset()
        for b in self.bulletGroup:
            b.kill()             
        self.squid.reset()
        #self.squid_controllable = True
        self.set_music()
        
    def if_boss_dead(self):
        "if boss is killed, start next wave."
        self.boss.shootable = False
        self.boss.frame = 0
        self.boss.currentimage = self.boss.imgdead
        for b in self.baddies:
            b.currentimage = b.imgdead            
        self.boss_dead = True
        self.boss = None
        
        
    def end_wave(self, time_delta):
        """ends current wave"""
        self.squid_controllable = False
        if self.scroll_to_left:
            self.squid.rect.x += self.speed*time_delta
        else: self.squid.rect.x += -self.speed*time_delta
        self.squid.dy = 1
        if self.squid.rect.x > self.field_length or self.squid.rect.x <0\
         and self.start_time <  self.time - self.short_time:
            if prepare.MUSIC_ON == True:
                self.background_music.fadeout(1000)
            if self.wave_number <= 2:
                self.new_wave(self.wave_number+1)
            else: self.quit_to_title()            
                        
    def accelerometer_controls(self):
        if self.squid_controllable == True and self.android:
                self.squid.dx = self.accelerometer()[0]
                self.squid.dy = self.accelerometer()[1]
    
    def mouse_controls(self, time_delta):
        "make squid follow cursor"
        max_speed = 400 * time_delta
        if self.squid_controllable == True:
            focuspos = pygame.mouse.get_pos()
            diffx =  (self.squid.rect.center[0] - focuspos[0])
            diffy =   (self.squid.rect.center[1] - focuspos[1])
            if abs(diffx) > 50 or abs(diffy) > 50:
                self.squid.delay = 600
            else: self.squid.delay = 800
            if abs(diffx) > 50:
                if diffx > 0:
                    self.squid.rect.x += -max_speed
                else: self.squid.rect.x += max_speed                
            if abs(diffy) > 50:
                if diffy > 0:
                    self.squid.rect.y += -max_speed
                else: self.squid.rect.y += max_speed               
        else: pass
    
    def handle_dead_menu(self):
        """called if player runs out of lives"""        
        key_pressed =  pygame.key.get_pressed()
        if self.clicked == True or key_pressed[pygame.K_RETURN]:
            if self.continuelabel.option_highlighted == 0:
                for i in xrange(self.maxlife+1):
                    self.life += 1
                    self.lifeGroup.add(self.lifedots[self.life-1])
                self.label.toggle_visible(False)
                self.continuelabel.toggle_visible(False)
                self.new_wave(self.wave_number)
            elif self.continuelabel.option_highlighted == 1:
                self.quit_to_title()
        else: pass
            
    def quit_to_title(self):
        self.done = True
    
    def spawn_boss(self):
        self.boss = boss.Boss(self)
        self.sprites.append(self.boss)           
    
    def update_specifics(self, time, time_delta): 
        """things that need to be updated in individual scenes"""     
        if self.squid_controllable == True:
            self.detect_baddie_collisions(time_delta)
            self.detect_powerup_collisions(time_delta)
            self.handle_bullets(time_delta)
            self.bullet_baddie_collision(time_delta)
        self.accelerometer_controls()      
        if self.time - self.start_time > (self.mid_time)*time_delta:
            self.label.toggle_visible(False)
            self.squid_controllable = True
        if self.boss is not None:    
            if self.boss.check_bounds() == True and self.boss.shootable == True:
                self.detect_boss_collision(time_delta) 
                self.bullet_boss_collision()
        else: 
            if self.foreground_map.at_end == True and not self.boss_dead:
                self.spawn_boss()
        if self.squid.dead == True:
            if prepare.MUSIC_ON == True:     
                self.background_music.fadeout(1000)
            self.handle_dead_menu()
        if self.boss_dead == True:
            self.end_wave(time_delta)
        for b in self.baddie_lists:            
            b.update(time_delta)
            
        
            
        pygame.draw.rect(self.screen, 
                             pygame.color.Color("black"), self.hudrect, 5) 
            
    
                
        
def main():
    import cutscene
    import title
    
    run_it = scene.Control()
    state_dict = {"TITLE" : title.Title(),
                  "INTRO" : cutscene.Cutscene0(),
                  "GAMEPLAY" : gamePlay(),
                  "ENDING": cutscene.Cutscene1()
                   }
    run_it.setup_states(state_dict, "GAMEPLAY")
    run_it.main()   
    
if __name__ == "__main__":
    main() 