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

#TODO: END OF WAVE BADDIES


class gamePlay(scene.Scene):
    def __init__(self):        
        scene.Scene.__init__(self)
        self.next = "ENDING"
    
    def init_variables(self):
        """ init all variables needed in scene"""
        self.speed = self.MASTER_SPEED * 3
        self.scroll_to_left = True
        self.number_of_baddies = 50
        
        self.number_of_powerups = 5
        self.number_of_bullets = 30
        self.wave_number = 0
        #the shooting speed number is the delay between bullets. a LOWER number means the bullets fire faster.
        self.shooting_speed = self.speed / 2
        self.default_shooting_speed = self.shooting_speed
        self.powerup_shooting_speed = self.shooting_speed  / 4 #also the minimum speed   
        self.shield_counter = 0
        self.timer = 5
        self.collisiontimer = -1
        self.maxlife = 3
        self.life = self.maxlife
        self.bullettimer = self.shooting_speed
        self.bullet_powerup_timer = 0
        self.bullet_order = 0
        self.hudrect = pygame.rect.Rect(10,10,100,40)
        self.boss_dead = False
        self.squid_controllable = False
        #self.paths = [pycurve.make_b_spline(self,pycurve.PATHS[pycurve.PATHS.index(x)]) for x in pycurve.PATHS]
                                                    
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        
        self.baddie_damage_sound = pygame.mixer.Sound('sounds/34172__glaneur-de-sons__woosh-02.wav')
        self.squid_damage_sound = pygame.mixer.Sound('sounds/92736__robinhood76__01522-swoosh-1.wav')
        self.powerup_sound = pygame.mixer.Sound('sounds/174462__yottasounds__power-up-001.wav')
        
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
        
        self.bullets = [bullet.Bullet(self) for n in xrange(self.number_of_bullets)]      
        self.bulletGroup = self.make_sprite_group(self.bullets)
        self.add_group(self.bulletGroup)
        
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
                
        self.boss = boss.Boss(self)
        
              
        self.sprites = [self.background_map, self.foreground_map, self.squid, self.boss, self.baddieGroup,  
                        self.powerupGroup, self.bulletGroup, self.lifeGroup, self.label, self.scorelabel,self.continuelabel]  
        
    def create_baddie_lists(self):
        self.baddie_lists = []
        b_l = [self.baddies[x*5:(x*5)+ 5] for x in range(len(self.baddies)/5)]
        for b in b_l:
            self.baddie_lists.append(baddie_movement.baddie_List(self,b,b_l.index(b))    )      
                
                
    def startup(self, time, persistant):
        self.init_objects()
        self.start_time = time
        return scene.Scene.startup(self, time, persistant)
    
    def cleanup(self):        
        return scene.Scene.cleanup(self)
    
        
    def detect_baddie_collisions(self):
        "detects collision between baddies and squid"
        collidedbaddie = pygame.sprite.spritecollideany(self.squid, self.baddieGroup)
        if collidedbaddie and collidedbaddie.currentimage is not collidedbaddie.imgdead and self.squid_controllable == True:
            if self.collisiontimer <= 0:                
                self.vibrate(.3)
                self.collisiontimer = self.MASTER_SPEED
                collidedbaddie.frame = 0
                collidedbaddie.currentimage = collidedbaddie.imgdead
                self.hurt_squid()
        
            
    def hurt_squid(self):      
        "hurts squid, kills it if life goes BELOW 0"  
        self.squid.dx = self.squid.dy = 0
        if self.shield_counter <= 0 :
            self.life = self.life - 1
            self.squid_damage_sound.play()
            if self.life> -1:
                self.lifedots[self.life].kill()
            self.shooting_speed = self.default_shooting_speed
            if self.life < 0 and self.squid_controllable == True:
                self.squid_killed()            
                        
    def detect_powerup_collisions(self):
        "detects collision between squid and powerup"
        collidedpowerup = pygame.sprite.spritecollideany(self.squid, self.powerupGroup)
        if collidedpowerup:
            if self.collisiontimer < 0:   
                self.powerup_sound.play() 
                self.vibrate(.2)
                self.collisiontimer = self.MASTER_SPEED/4
                if collidedpowerup.color == 'blue':  
                    if self.life < self.maxlife:
                        self.life = self.life + 1
                        self.lifeGroup.add(self.lifedots[self.life-1])
                elif collidedpowerup.color == 'red':
                    self.bullet_powerup_timer = self.speed * 2        
                elif collidedpowerup.color == 'yellow':            
                    self.shield_counter = self.speed *2
                collidedpowerup.reset()
                
                      
            
    def detect_boss_collision(self):
        "detects collision between boss and squid using mask."
        collision = pygame.sprite.collide_mask(self.squid, self.boss)
        if collision and self.boss.currentimage is not self.boss.imgdead and self.squid_controllable == True:
            if self.collisiontimer <= 0:                
                self.vibrate(.3)
                self.collisiontimer = self.MASTER_SPEED
                self.hurt_squid()
        
        
    def squid_killed(self): 
        "when main character dies, kill it and display continue menu."
        self.squid.dx = 0
        self.squid.dy = -1
        self.squid.dead = True 
        self.label.toggle_visible(True)
        self.label.textlines = ["it HAD a squid in it"]
        self.start_time= self.time
        self.squid_controllable = False
        self.continuelabel.toggle_visible(True)
        
    def handle_bullets(self, time_delta):
        "fires bullets in bullet list on a delay"
        if self.bullettimer < 0 and self.squid_controllable == True:           
            bullet = self.bullets [self.bullet_order]                
            bullet._set_visible(True)           
            bullet.is_fired (self.squid.rect.centerx, self.squid.rect.centery, time_delta) 
                
            if self.bullet_powerup_timer < 0:
                self.bullettimer = self.shooting_speed
            else: self.bullettimer = self.powerup_shooting_speed
            
            if self.bullet_order == self.number_of_bullets-1:
                self.bullet_order = 0
            else:         
                self.bullet_order += 1
                
    def bullet_baddie_collision(self):
        """checks to see if bullet has llided with an enemy. Sets enemy to dead."""
        for b in self.bullets:
            collidedbaddie = pygame.sprite.spritecollideany(b,self.baddieGroup)
            if collidedbaddie and collidedbaddie.check_bounds() == True\
             and collidedbaddie.currentimage is not collidedbaddie.imgdead:   
                collidedbaddie.hp -= 1  
                collidedbaddie.hit = True
                self.vibrate(.1) 
                self.baddie_damage_sound.play()
                self.increment_score('baddie')
                b.reset()
                if collidedbaddie.hp <= 0:
                    self.kill_baddie(collidedbaddie)
                    self.check_for_combo(collidedbaddie)
                                  
    def check_for_combo(self, collidedbaddie):
        """kills other enemies in same line as enemy killed."""        
        if collidedbaddie.list_index == 0:
            for b in self.baddies:
                if b.list_id == collidedbaddie.list_id: 
                    if b.currentimage is not b.imgdead:
                        self.kill_baddie(b)
                        #this is a score bonus
                        self.increment_score('baddie')
                       
    def kill_baddie(self, baddie):
        """called when baddie HP is 0"""
        baddie.frame = 0
        baddie.currentimage = baddie.imgdead
        if self.shooting_speed > self.powerup_shooting_speed:
            self.shooting_speed = self.shooting_speed - self.shooting_speed/30
        else: pass
    
    def bullet_boss_collision(self):
        """checks to see if bullet has collided with a boss. """
        for b in self.bullets:
            collision = pygame.sprite.collide_mask(b, self.boss) 
            if collision:
                self.boss.hp -= 1  
                self.boss.hit = True 
                self.vibrate(.1) 
                b.reset()
                if self.boss.hp <= 0:
                    self.start_time = self.time
                    self.if_boss_dead()
                    self.ending_label()
                    
    def ending_label(self):
        self.label.textlines = ["You Win!", "Score = {0}".format(self.score)]
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
        resetlist = self.maps + self.baddies + self.powerups + self.bullets+ self.baddie_lists
        for r in resetlist:
            r.reset()
        self.boss.reset()        
        self.squid.reset()
        self.squid_controllable = True
        
    def if_boss_dead(self):
        "if boss is killed, start next wave."
        self.boss.shootable = False
        self.boss.frame = 0
        self.boss.currentimage = self.boss.imgdead
        for b in self.baddies:
            b.currentimage = b.imgdead            
        self.boss_dead = True
        
        
    def end_wave(self):
        """ends current wave"""
        self.squid_controllable = False
        if self.scroll_to_left:
            self.squid.dx = self.speed*2
        else: self.squid.dx = -self.speed*2
        self.squid.dy = 1
        if self.squid.rect.x > self.field_length or self.squid.rect.x <0\
         and self.start_time <  self.time - 10000:
            if self.wave_number <= 2:
                self.new_wave(self.wave_number+1)
            else: self.quit_to_title()            
                        
    def accelerometer_controls(self):
        if self.squid_controllable == True and self.android:
                self.squid.dx = self.accelerometer()[0]
                self.squid.dy = self.accelerometer()[1]
    
    def mouse_controls(self, time_delta):
        "make squid follow cursor"
        if self.squid_controllable == True:
            focuspos = pygame.mouse.get_pos()
            diffx =  (self.squid.rect.center[0] - focuspos[0])
            diffy =   (self.squid.rect.center[1] - focuspos[1])
            if abs(diffx) > 50:
                self.squid.dx += -diffx * time_delta
            else: self.squid.dx = 0
            if abs(diffy) > 50:
                self.squid.dy += -diffy * time_delta
            else: self.squid.dy = 0
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
           
    def update_specifics(self, time, time_delta): 
        """things that need to be updated in individual scenes"""        
        self.collisiontimer -=1
        self.shield_counter -= 1
        #draw the little rectangle around the lifedots
        pygame.draw.rect(self.screen, 
                             pygame.color.Color("black"), self.hudrect, 5)   
        if self.squid_controllable == True:
            self.detect_baddie_collisions()
            self.detect_powerup_collisions()
            self.handle_bullets(time_delta)
            self.bullet_baddie_collision()
        self.accelerometer_controls()
        self.bullettimer -= 1  
        self.bullet_powerup_timer -=1    
        if self.time - self.start_time > 10000:
            self.label.toggle_visible(False)
            self.squid_controllable = True
            
        if self.boss.check_bounds() == True and self.boss.shootable == True:
            self.detect_boss_collision() 
            self.bullet_boss_collision()
        if self.squid.dead == True: 
            self.handle_dead_menu()
        if self.boss_dead == True:
            self.end_wave()
        for b in self.baddie_lists:
            b.update()
                
        
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