import pygame
from pygame.locals import *
import sys, os, random
from math import *


class Noise(object):
    def __init__(self, width, height, tw):
        self.width = width
        self.height = height
        #self.zlevels = zlevels
        self.tw = tw   #In nodes
        self.repeats = 1 # 1    #number of repetitions on screen

        self.tilesize = float(self.width) / self.repeats
        self.tilesize /= self.tw
        self.p = []
        for x in xrange(2 * self.tw):
            self.p.append(0)
            
        self.permutation = []
        for value in xrange(self.tw):
            self.permutation.append(value)
        random.shuffle(self.permutation)

        for i in xrange(self.tw):
            self.p[i] = self.permutation[i]
            self.p[self.tw + i] = self.p[i]

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    def lerp(self, t, a, b):
        return a + t * (b - a)
    def grad(self, hash, x, y, z):
        #CONVERT LO 4 BITS OF HASH CODE INTO 12 GRADIENT DIRECTIONS.
        h = hash & 15
        if h < 8: u = x
        else:     u = y
        if h < 4: v = y
        else:
            if h == 12 or h == 14: v = x
            else:                  v = z
        if h & 1 == 0: first = u
        else:        first = -u
        if h & 2 == 0: second = v
        else:        second = -v
        return first + second

        
    def noise(self, x, y, z):
        #FIND UNIT CUBE THAT CONTAINS POINT.
        X = int(x) & (self.tw - 1)
        Y = int(y) & (self.tw - 1)
        Z = int(z) & (self.tw - 1)
        #FIND RELATIVE X,Y,Z OF POINT IN CUBE.
        x -= int(x)
        y -= int(y)
        z -= int(z)
        #COMPUTE FADE CURVES FOR EACH OF X,Y,Z.
        u = self.fade(x)
        v = self.fade(y)
        w = self.fade(z)
        #HASH COORDINATES OF THE 8 CUBE CORNERS
        A = self.p[X  ] + Y; AA = self.p[A] + Z; AB = self.p[A + 1] + Z
        B = self.p[X + 1] + Y; BA = self.p[B] + Z; BB = self.p[B + 1] + Z
        #AND ADD BLENDED RESULTS FROM 8 CORNERS OF CUBE
        return self.lerp(w, self.lerp(v,
                           self.lerp(u, self.grad(self.p[AA  ], x  , y  , z),
                                  self.grad(self.p[BA  ], x - 1, y  , z)),
                           self.lerp(u, self.grad(self.p[AB  ], x  , y - 1, z),
                                  self.grad(self.p[BB  ], x - 1, y - 1, z))),
                      self.lerp(v,
                           self.lerp(u, self.grad(self.p[AA + 1], x  , y  , z - 1),
                                  self.grad(self.p[BA + 1], x - 1, y  , z - 1)),
                           self.lerp(u, self.grad(self.p[AB + 1], x  , y - 1, z - 1),
                                  self.grad(self.p[BB + 1], x - 1, y - 1, z - 1))))

    def generate(self):
        octaves = 2 # 8 seems decent but using 2 for speed
        #octaves = 1
        persistence = 0.25
        #persistence = 0.8
        
        amplitude = 1.0
        maxamplitude = 1.0
        mapdata = [[0 for cols in xrange(self.height)] for rows in xrange(self.width)]
        for octave in xrange(octaves):
            amplitude *= persistence
            maxamplitude += amplitude
            for x in xrange(self.width):
                for y in xrange(self.height):
                    sc = float(self.width) / self.tilesize
                    frequency = 1.0
                    amplitude = 1.0
                    color = 0.0
                    for octave in xrange(octaves):
                        sc *= frequency
                        grey = abs(self.noise(sc * float(x) / self.width, sc * float(y) / self.height, 0.0)) #Turbulence noise in theory
                        #grey = self.noise(sc*float(x)/self.width,sc*float(y)/self.height,0.0) # regular perlin
                        #grey = self.noise(sc*float(x)/self.width,sc*float(y)/self.height,sc*float(z)/self.zlevels)
                        #grey = noise(sc*float(x)/width,sc*float(y)/height,0.0)
                        grey = (grey + 1.0) / 2.0
                        grey *= amplitude
                        color += grey
                        frequency *= 2.0
                        amplitude *= persistence
                    color /= maxamplitude
                    color = int(round(color * 100.0)) # If you adjust the multiplyer you need to adjust the tile mappings in gamemap.py
                    #color = int(round(color*255.0))
                    mapdata[x][y] = color
        return mapdata

    def printme(self, mapdata):
        for x in xrange(self.width):
            for y in xrange(self.height):
                print str(mapdata[x][y]),
            print ''


if __name__ == '__main__':
    n = Noise(10, 10, 16)
    map = n.generate()
    n.printme(map)
