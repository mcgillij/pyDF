from noise import pnoise2
from PIL import Image
import numpy as np
import random

class NoiseMapGenerator():
    def __init__(self,width,height,scale=100,octaves=4,persitancy=0.5,lacunarity=2,seed:int=None):
        self.seed = seed 
        self.width = width
        self.height = height
        self.center_x = self.width/2
        self.center_y = self.height/2
        self.scale = scale
        self.octaves = octaves
        self.persistance = persitancy
        self.lacunarity = lacunarity

    def generate(self,xoffset=0,yoffset=0): # TODO: probably should allow  to change more settings on each generate
        random.seed(self.seed)
        max_range = 10000
        offsetX = random.random()*max_range - max_range + xoffset
        offsetY = random.random()*max_range - max_range + yoffset

        if self.scale < 0:
            self.scale = 0.0001

        noisemap = np.zeros((self.height,self.width),dtype=np.float32)
        h2 = self.height/2
        w2 = self.width/2
        for y in range(self.height):
            for x in range(self.width):
                sampleX = (x-w2)/self.scale + offsetX
                sampleY = (y-h2)/self.scale + offsetY
                perlinValue = pnoise2(sampleX,sampleY,octaves=4)
                noisemap[y][x] = perlinValue

        # normalize
        noisemap = np.interp(noisemap, (noisemap.min(), noisemap.max()), (255, 0)).astype(np.uint8)
        return noisemap

    def generate_image(self,x_offset=0,y_offset=0):
        noisemap = self.generate(x_offset,y_offset)
        return Image.fromarray(noisemap,'L')


    



if __name__ == '__main__':
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    print(f'Generating sample noise map {SCREEN_WIDTH} x {SCREEN_HEIGHT} ..')
    NoiseMapGenerator(SCREEN_WIDTH,SCREEN_HEIGHT,100,4,0.5,2,1).generate_image().show()
    print('done')