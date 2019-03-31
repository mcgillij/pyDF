from utilities import noisemapgenerator as util
from random import randint
import pygame

screen = None
clock = None

class MapGen():
    
    def __init__(self,width,height):
        pygame.init()
        self.FPS = 60
        self.running = True
        self.width = width
        self.height = height
        self.mainfont = pygame.font.SysFont("Arial", 16)
        self.clock = pygame.time.Clock()
        self.noise = None
        self.seed = randint(12134,48799)
        self.lunacracity = 2
        self.scale = 100
        self.texture = None
    def run(self):
        
        self.screen = pygame.display.set_mode((self.width,self.height),False)
        pygame.display.set_caption("Map Generator")
        self.noise = util.NoiseMapGenerator(300,300,4,0.5,self.seed)

        needupdate=True
        xoff =0
        yoff= 0
        while self.running:
            if needupdate:
                self.noise.seed = self.seed
                self.texture  = self.noise.generate_image(self.scale,x_offset=xoff,y_offset=yoff)
            
                mode = self.texture.mode
                size = self.texture.size
                data = self.texture.convert('RGB').tobytes()
                py_image = pygame.image.fromstring(data, size,'RGB').convert()
                needupdate =False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.scale -= 5
                    if event.key == pygame.K_RIGHT:
                        self.scale += 5
                    if event.key == pygame.K_UP:
                        self.seed += 1
                    if event.key == pygame.K_DOWN:
                        self.seed -= 1

                    if event.key == pygame.K_a:
                        xoff -= 0.25
                    if event.key == pygame.K_d:
                        xoff += 0.25

                    if event.key == pygame.K_w:
                        yoff -= 0.25
                    if event.key == pygame.K_s:
                        yoff += 0.25

                    needupdate = True
                print(event)
            

            ####################
            self.screen.fill(pygame.Color('black'))
            fps = self.mainfont.render(f'FPS: {str(int(self.clock.get_fps()))}', True, pygame.Color('white'))
            scal = self.mainfont.render(f'SCALE: {self.scale}', True, pygame.Color('white'))
            seed = self.mainfont.render(f'SEED: {self.seed}', True, pygame.Color('white'))


            self.screen.blit(py_image,(400-150,300-150))
            self.screen.blit(fps, (10, 10))
            self.screen.blit(scal, (10, 30))
            self.screen.blit(seed, (10, 45))
            #pygame.display.update()
            pygame.display.flip()
            self.clock.tick(60)
            #pygame.display.flip()



    def shutdown(self):
        pygame.quit()







if __name__ == "__main__":
    MapGen(800,600).run()
    
    


