from noise import pnoise2
import numpy as np
import random
import colormap


class NoiseMapGenerator():
    def __init__(self, width, height, octaves=4, persitancy=0.5, seed: int = None):
        self.seed = seed
        self.width = width
        self.height = height
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.octaves = octaves
        self.persistance = persitancy

    def generate(self, scale=100, lacunarity=2, xoffset=0,
                 yoffset=0):  # TODO: probably should allow  to change more settings on each generate
        random.seed(self.seed)
        max_range = 10000
        offsetX = random.random() * max_range - max_range + xoffset
        offsetY = random.random() * max_range - max_range + yoffset

        if scale < 0:
            scale = 0.0001

        noisemap = np.zeros((self.height, self.width), dtype=np.float32)  # TODO: remove dependency on numpy ?
        h2 = self.height / 2
        w2 = self.width / 2
        for y in range(self.height):
            for x in range(self.width):
                sampleX = (x - w2) / scale + offsetX
                sampleY = (y - h2) / scale + offsetY
                perlinValue = pnoise2(sampleX, sampleY, octaves=4, lacunarity=lacunarity)
                noisemap[y][x] = perlinValue

        # normalize
        noisemap = np.interp(noisemap, (noisemap.min(), noisemap.max()), (255, 0)).astype(
            np.uint8)  # TODO: remove dependency on numpy ?
        return noisemap


if __name__ == '__main__':
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    OCTAVES = 4
    SEED = random.random() * 1000
    PERSISTENCE = 0.5

    print(f'Generating sample noise map {SCREEN_WIDTH} x {SCREEN_HEIGHT} using: ')
    print(f'SEED: {SEED}')
    print(f'OCTAVES: {OCTAVES}')
    print(f'PERSISTENCE: {PERSISTENCE}')
    current_noise_map = NoiseMapGenerator(SCREEN_WIDTH, SCREEN_HEIGHT, OCTAVES, PERSISTENCE, SEED).generate()
    color_mapping = colormap.ColorMap(current_noise_map)
    print(' generating greyscale image')
    greyscale = color_mapping.generate_image()
    print('displaying greyscale image')
    greyscale.show()
    print(' generating colors')
    colorised = color_mapping.colorize()
    print('displaying colorised image')
    colorised.show()

    print('done')
