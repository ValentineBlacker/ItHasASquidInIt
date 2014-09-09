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

#TODO:
#CUTSCENES

class gamePlay(scene.Scene):
    def init_variables(self):
        """ init all variables needed in scene"""
        self.speed = self.MASTER_SPEED
        self.scroll_to_left = True
        self.number_of_baddies = 50
        self.number_of_baddies_used = 10
        self.number_of_powerups = 5
        self.number_of_bullets = 30
        self.wave_number = 0
        self.speed_increase = self.speed /(self.speed)
        #the shooting speed number is the delay between bullets. a LOWER number means the bullets fire faster.
        self.shooting_speed = self.speed * 10
        self.default_shooting_speed = self.shooting_speed
        self.powerup_shooting_speed = self.speed  *2 #also the minimum speed   
        self.shield_counter = 0
        self.timer = 5
        self.collisiontimer = 5
        self.maxlife = 3
        self.life = self.maxlife
        self.bullettimer = 20
        self.bullet_powerup_timer = 0
        self.bullet_order = 0
        self.title_time = self.time        
        self.next_level = None
        self.hudrect = pygame.rect.Rect(10,10,100,40)
        self.squid_controllable = True
                
    def init_objects(self):
        """ creates objects needed in specfic scenes"""
        
        self.squid = squid.Squid(self)
        
        self.background_map = maphandler.ScrollingMap(self, 'background')
        self.foreground_map = maphandler.ScrollingMap(self, 'foreground')
        self.maps = [self.background_map, self.foreground_map]  
        
        self.baddies = [baddie.Baddie(self, n) for n in xrange(self.number_of_baddies)]           
        self.baddieGroup = self.make_sprite_group(self.baddies)
        self.add_group(self.baddieGroup)        
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
        
              
        self.sprites = [self.background_map, self.foreground_map, self.squid, self.baddieGroup, self.boss, 
                        self.powerupGroup, self.bulletGroup, self.lifeGroup, self.label, self.scorelabel,self.continuelabel]  
        
        
        
    def detect_baddie_collisions(self):
        "detects collision between baddies and squid"
        collidedbaddie = pygame.sprite.spritecollideany(self.squid, self.baddieGroup)
        if collidedbaddie and collidedbaddie.currentimage is not collidedbaddie.imgdead and self.squid_controllable == True:
            if self.collisiontimer <= 0:                
                self.vibrate(.3)
                self.collisiontimer = 50
                collidedbaddie.frame = 0
                collidedbaddie.currentimage = collidedbaddie.imgdead
                self.hurt_squid()
        
            
    def hurt_squid(self):      
        "hurts squid, kills it if life goes BELOW 0"  
        self.squid.dx = self.squid.dy = 0
        if self.shield_counter <= 0 :
            self.life = self.life - 1
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
                self.vibrate(.2)
                self.collisiontimer = 5
                if collidedpowerup.color == 'blue':  
                    if self.life < self.maxlife:
                        self.life = self.life + 1
                        self.lifeGroup.add(self.lifedots[self.life-1])
                elif collidedpowerup.color == 'red':
                    self.bullet_powerup_timer = 250        
                elif collidedpowerup.color == 'yellow':            
                    self.shield_counter = 250
                collidedpowerup.reset()
                
                      
            
    def detect_boss_collision(self):
        "detects collision between boss and squid using mask."
        collision = pygame.sprite.collide_mask(self.squid, self.boss)
        if collision and self.boss.currentimage is not self.boss.imgdead and self.squid_controllable == True:
            if self.collisiontimer <= 0:                
                self.vibrate(.3)
                self.collisiontimer = 50
                self.hurt_squid()
        
        
    def squid_killed(self): 
        "when main character dies, kill it and display continue menu."
        self.squid.dx = 0
        self.squid.dy = -.5
        self.squid.dead = True 
        self.label.toggle_visible(True)
        self.label.textlines = ["it HAD a squid in it"]
        self.title_time= self.time
        self.squid_controllable = False
        self.continuelabel.toggle_visible(True)
        
    def handle_bullets(self):
        "fires bullets in bullet list on a delay"
        if self.bullettimer < 0 and self.squid_controllable == True:           
            bullet = self.bullets [self.bullet_order]                
            bullet._set_visible(True)           
            bullet.is_fired (self.squid.rect.centerx, self.squid.rect.centery) 
                
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
            if collidedbaddie:       
                if collidedbaddie.check_bounds() == True and collidedbaddie.currentimage is not collidedbaddie.imgdead:
                    self.vibrate(.1) 
                    collidedbaddie.frame = 0
                    collidedbaddie.currentimage = collidedbaddie.imgdead
                    self.increment_score('baddie')
                    if self.shooting_speed > self.powerup_shooting_speed:
                        self.shooting_speed = self.shooting_speed - self.shooting_speed/20
                    else: pass
                b.reset()
    
    def bullet_boss_collision(self):
        """checks to see if bullet has collided with a boss. """
        for b in self.bullets:
            collision = pygame.sprite.collide_mask(b, self.boss) 
            if collision:
                self.boss.hp -= 1  
                self.boss.hit = True 
                self.vibrate(.1) 
                b.reset()
                if self.boss.hp == 0:
                    self.boss.frame = 0
    
    def increment_score(self, enemy_type):
        if enemy_type == 'baddie':
            self.score += 10
        elif enemy_type == 'boss':
            self.score += 50
        self.scorelabel.image.fill(self.scorelabel.fillcolor)
        self.scorelabel.textlines =[' %0*d' % (5, self.score)]
    
    def new_wave(self, wave_number):   
        self.wave_number = wave_number
        self.label.toggle_visible(True)
        self.squid.dead = False
        self.title_counter = 50
        self.number_of_baddies_used += 5
        self.title_time = self.time 
        self.label.textlines = ["sphere {0}".format(self.label.int_to_roman[self.wave_number])]
        resetlist = self.maps + self.baddies + self.powerups + self.bullets
        for r in resetlist:
            r.reset()
        self.boss.reset()        
        self.squid.reset()
        self.squid_controllable = True
        
    def if_boss_dead(self):
        if self.boss.hp <= 0:
            self.boss.currentimage = self.boss.imgdead
            if self.boss.frame >= self.boss.number_of_frames-1:
                if self.wave_number <= 0:
                    self.new_wave(self.wave_number+1)
                else: self.quit_to_title()
                
    
    def mouse_controls(self):
        if self.squid_controllable == True:
            posx = pygame.mouse.get_pos()[0]
            posy = pygame.mouse.get_pos()[1]
            if self.squid.dead == False:
                if self.squid.rect.collidepoint(posx,posy) == False:
                    if posx < self.squid.rect.x:               
                        if posy  > self.squid.rect.top and posy < self.squid.rect.bottom :       
                            self.squid.dx = self.squid.dx - .2     
                    elif posx >  self.squid.rect.x:
                        if posy  > self.squid.rect.top and posy < self.squid.rect.bottom:    
                            self.squid.dx = self.squid.dx + .2   
                    if posy < self.squid.rect.y:  
                        if posx > self.squid.rect.left and posx < self.squid.rect.right:      
                            self.squid.dy = self.squid.dy - .2      
                    elif posy > self.squid.rect.y: 
                        if posx > self.squid.rect.left and posx < self.squid.rect.right:   
                            self.squid.dy = self.squid.dy + .2                    
                
            
    def accelerometer_controls(self):
        if self.squid_controllable == True and self.android:
                self.squid.dx = self.accelerometer()[0]
                self.squid.dy = self.accelerometer()[1]
    
    def handle_dead_menu(self):
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
            import title
            self.nextlevel = title.Title()       
            self.level_transition()
    
    def keyboard_controls(self, event):
        if self.squid_controllable == True:
            if event.key == pygame.K_UP:
                self.squid.dy = self.squid.dy - 1
            if event.key == pygame.K_DOWN:
                self.squid.dy = self.squid.dy + 1   
            if event.key == pygame.K_RIGHT:            
                self.squid.dx = self.squid.dx + 1 
            if event.key == pygame.K_LEFT:
                self.squid.dx = self.squid.dx - 1
        else: 
            if  event.key == pygame.K_UP :
                self.continuelabel.option_highlighted = 0
            elif event.key == pygame.K_DOWN:
                self.continuelabel.option_highlighted = 1
            
           
    def update(self): 
        """things that need to be updated in individual scenes""" 
        #rethink timers
        self.collisiontimer -=1
        self.shield_counter -= 1
        #draw the little rectangle around the lifedots
        pygame.draw.rect(self.screen, 
                             pygame.color.Color("black"), self.hudrect, 5)   
        self.detect_baddie_collisions()
        self.detect_powerup_collisions()
        self.handle_bullets()
        self.bullet_baddie_collision()
        self.accelerometer_controls()
        self.bullettimer -= 1  
        self.bullet_powerup_timer -=1
        
        if self.title_time <  self.time - 100 :
            self.label.toggle_visible(False)
            self.label.text = " "
            
        if self.boss.check_bounds() == True and self.boss.shootable == True:
            self.detect_boss_collision() 
            self.bullet_boss_collision()
            self.if_boss_dead()
        if self.squid.dead == True: 
            self.handle_dead_menu()
        
        
        
    
def main():

    game = gamePlay()

    game.start()
if __name__ == "__main__":

    main()