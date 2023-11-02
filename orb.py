import pygame
import random
import math
import sys
class orb():


    def __init__(self, radius, mass, x, y, color,speed):
        self.radius = radius
        self.mass = mass
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.font = pygame.font.SysFont("Arial", 24)

    def update(self,screen, orbs):
        # Apply gravity
        self.ay += 0.1


        # Update velocity
        self.vx += self.ax
        self.vy += self.ay


        # Limit maximum velocity
        max_speed = 5
        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if speed > max_speed:
            self.vx *= max_speed / speed
            self.vy *= max_speed / speed


        # Update position
        self.x += self.vx
        self.y += self.vy

        #check for collision with bottom of screen
        if self.y + self.radius >= screen.get_height():
            self.y = screen.get_height() - self.radius
            self.vy = -self.vy * 0.2
        # Check for collision with sides of screen
        if self.x + self.radius >= screen.get_width():
            self.x = screen.get_width() - self.radius
            self.vx = -self.vx * 0.2
            self.ax = -0.1
        elif self.x - self.radius <= 0:
            self.x = self.radius
            self.vx = -self.vx * 0.2
            self.ax = 0.1
        else:
            self.ax = 0

       # Check for collision with other orbs
        for other_orb in orbs:
            if other_orb != self:
                distance = math.sqrt((self.x - other_orb.x) ** 2 + (self.y - other_orb.y) ** 2)
                if distance <= self.radius + other_orb.radius:
                    if(self.radius <= 90):
                        if self.radius == other_orb.radius:
                            new_mass = self.mass + other_orb.mass
                            new_radius = self.radius + 10
                            new_color = self.getColor(new_radius)
                            new_orb = orb(new_radius, new_mass, self.x, self.y, new_color, self.speed)
                            orbs.remove(self)
                            orbs.remove(other_orb)
                            orbs.append(new_orb)
                        else:
                            if distance != 0:
                                # Calculate new velocities using conservation of momentum and energy
                                nx = (other_orb.x - self.x) / distance
                                ny = (other_orb.y - self.y) / distance
                                p = 2 * (self.vx * nx + self.vy * ny - other_orb.vx * nx - other_orb.vy * ny) / (self.mass + other_orb.mass)
                                self.vx -= p * other_orb.mass * nx
                                self.vy -= p * other_orb.mass * ny
                                other_orb.vx += p * self.mass * nx
                                other_orb.vy += p * self.mass * ny

                                # Separate the orbs to prevent them from overlapping
                                overlap = (self.radius + other_orb.radius - distance) / 2
                                self.x -= overlap * nx
                                self.y -= overlap * ny
                                other_orb.x += overlap * nx
                                other_orb.y += overlap * ny 
                    
        
        # Check for collision with line at y-coordinate 100
        if self.y <= 100:
            # End game and display game over screen
            self.game_over_screen(screen)
            pygame.quit()
            sys.exit()
        # Reset acceleration
        self.ax = 0
        self.ay = 0

    def game_over_screen(self, screen):
        screen.fill((255, 255, 255))
        game_over_text = self.font.render("Game Over", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = (screen.get_width() / 2, screen.get_height() / 2)
        screen.blit(game_over_text, game_over_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def setX(self,x):
        self.x = x

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def move(self) :
        self.y += self.speed
    
    def getColor(self,radius):
        color = (0,0,0)

        if radius == 40:
            color = (0,0,255)
        elif radius == 50:
            color = (0,255,0)
        elif radius == 60:
            color = (255,0,0)
        elif radius == 70:
            color = (0,255,255)
        elif radius == 80:
            color = (255,0,255)
        elif radius == 90:
            color = (255,255,0)
        elif radius == 100:
            color = (0,0,0)
        

        return color
        
