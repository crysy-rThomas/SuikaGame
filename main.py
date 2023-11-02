import sys
import pygame
from orb import orb
from random import choice
import asyncio

class main():
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((500, 600))
        pygame.display.set_caption("Suika game")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.orbs = []
        self.font = pygame.font.SysFont("Arial", 24)

    async def run(self):
        while True:
            self.clock.tick(60)
            self.check_events()
            for orb in self.orbs:
                orb.update(self.screen, self.orbs)
            self.draw()
            await asyncio.sleep(0)
    

    def random_orb(self, x):
        radius = choice([40,50,60])

        def switch(radius):
            if radius == 40:
                mass = 1
                color = (0,0,255)
                return mass,color
            elif radius == 50:
                mass = 2
                color = (0,255,0)
                return mass,color
            elif radius == 60:
                mass = 3
                color = (255,0,0)
                return mass,color
            
        new_orb = orb(radius,switch(radius)[0],x,101,switch(radius)[1],1)
        return new_orb
        


    async def wait_for_click(self, new_orb):
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    new_orb.x = event.pos[0]
                    new_orb.draw(self.screen)
                    pygame.display.flip()
                    self.draw()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.orbs.append(new_orb)
                    self.score = 0
                    for orb in self.orbs:
                        self.score += orb.mass
                    waiting_for_click = False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Generate orb at mouse position and draw it on screen
                new_orb = self.random_orb(event.pos[0])
                # Wait for click event before adding orb to list
                asyncio.create_task(self.wait_for_click(new_orb))
                self.screen.fill((255, 255, 255))
                new_orb.draw(self.screen)
                pygame.display.flip()

    def draw(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.line(self.screen, (0, 0, 0), (0, 100), (self.screen.get_width(), 100))

        for orb in self.orbs:
            orb.draw(self.screen)
          # Draw score on the right side of the screen
        score_text = self.font.render("Score: " + str(self.score), True, (0, 0, 0))
        score_rect = score_text.get_rect()
        score_rect.right = self.screen.get_width() - 10
        score_rect.top = 10
        self.screen.blit(score_text, score_rect)
        pygame.display.flip()

if __name__ == '__main__':
    game = main()
    asyncio.run(game.run())