from noise import pnoise2
from PIL import Image
import numpy as np
import random

class NoiseMapGenerator():
    def __init__(self,width,height,octaves=4,persitancy=0.5,seed:int=None):
        self.seed = seed 
        self.width = width
        self.height = height
        self.center_x = self.width/2
        self.center_y = self.height/2
        self.octaves = octaves
        self.persistance = persitancy


    def generate(self,scale=100,lacunarity=2,xoffset=0,yoffset=0): # TODO: probably should allow  to change more settings on each generate
        random.seed(self.seed)
        max_range = 10000
        offsetX = random.random()*max_range - max_range + xoffset
        offsetY = random.random()*max_range - max_range + yoffset

        if scale < 0:
            scale = 0.0001

        noisemap = np.zeros((self.height,self.width),dtype=np.float32) #TODO: remove dependency on numpy ?
        h2 = self.height/2
        w2 = self.width/2
        for y in range(self.height):
            for x in range(self.width):
                sampleX = (x-w2)/scale + offsetX
                sampleY = (y-h2)/scale + offsetY
                perlinValue = pnoise2(sampleX,sampleY,octaves=4,lacunarity=lacunarity)
                noisemap[y][x] = perlinValue

        # normalize
        noisemap = np.interp(noisemap, (noisemap.min(), noisemap.max()), (255, 0)).astype(np.uint8) #TODO: remove dependency on numpy ?
        return noisemap

    def generate_image(self,scale=100,lacunarity=2,x_offset=0,y_offset=0): #TODO: remove dependency on numpy  and PIL - this could be a seperate util class
        noisemap = self.generate(scale,lacunarity,x_offset,y_offset)
        return Image.fromarray(noisemap,'L')

    def colorize(self, noisemap): #TODO: remove dependency on numpy  and PIL - this could be a seperate util class
        colorimage = noisemap.convert('RGB')
        data = np.array(colorimage)
        
        deep_water = (14, 41, 163)
        water = (74, 190, 237)
        beach = (244, 218, 113)
        grass = (133, 178, 89)
        rock = (147, 149, 158)
        snow = (207, 208, 213)

        for y in range(self.height):
            for x in range(self.width):
                color = data[y][x]
              
              
                if np.all(color <= 50):
                    data[y][x] = deep_water
                elif np.all(color > 50) and np.all(color <= 100):
                    data[y][x] = water
                elif np.all(color > 100) and np.all(color <= 120):
                    data[y][x] = beach
                elif np.all(color > 120) and np.all(color <= 180):
                    data[y][x] = grass
                elif np.all(color > 180) and np.all(color <= 200):
                    data[y][x] = rock
                elif np.all(color > 200):
                    data[y][x] = snow

        return Image.fromarray(data)

if __name__ == '__main__':
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    print(f'Generating sample noise map {SCREEN_WIDTH} x {SCREEN_HEIGHT} ..')
    n = NoiseMapGenerator(SCREEN_WIDTH,SCREEN_HEIGHT,4,0.5,1)
    newmap = n.generate_image()
    n.colorize(newmap).show()
    newmap.show()
    print('done')