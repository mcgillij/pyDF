import numpy as np
from PIL import Image


# TODO: better naming
class ColorMapping:
    """
    Maps a color to a specific intensity range
    """

    def __init__(self, color, value_min, value_max):
        self.color = color
        self.min_value = value_min
        self.max_value = value_max

    def check(self, intensity) -> bool:
        return np.all(intensity <= self.max_value) and np.all(intensity > self.min_value)


class ColorMap:
    def __init__(self, data_array):
        self.data_array = data_array

    def generate_image(self, mode='L') -> Image:
        return Image.fromarray(self.data_array, mode)

    def colorize(self, color_ranges=None) -> Image:
        noise_image = self.generate_image()
        color_image = noise_image.convert('RGB')  # TODO: should check if it is already RGB or not
        data = np.array(color_image)

        # we need a structure for colors, maybe its own class?
        if not color_ranges:
            color_ranges = [
                ColorMapping((14, 41, 163), -1, 50),  # deep water
                ColorMapping((74, 190, 237), 50, 100),  # water
                ColorMapping((244, 218, 113), 100, 120),  # beaches
                ColorMapping((133, 178, 89), 120, 180),  # grass
                ColorMapping((147, 149, 158), 180, 200),  # rocks
                ColorMapping((207, 208, 213), 200, 255),  # snow
            ]

        height = data.shape[0]
        width = data.shape[1]

        for y in range(height):
            for x in range(width):
                intensity = data[y][x]

                for color_range in color_ranges:
                    if color_range.check(intensity):
                        data[y][x] = color_range.color

        return Image.fromarray(data)
