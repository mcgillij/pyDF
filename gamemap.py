try:
    import pygame
#    from time import time
    import pickle
#    from pprint import pprint
    import loader
    import random
    from math import sqrt
    import configparser
    import maptile
    import noise
    import selected
    import sys
except ImportError as err:
    print("couldn't load module, %s" % (err))
    sys.exit(2)


class GameMap(object):
    """ Gamemap object aka the Grid """

    def __init__(self, tw, mapw, maph, startXTile, startYTile, numXTiles, numYTiles):
        """ NEED TO MOVE THIS SHIT INTO THE RIGHT CONFIG FILE """
        self.tw = tw
        self.mapw = mapw
        self.maph = maph
        self.startXTile = startXTile
        self.startYTile = startYTile
        self.numXTiles = numXTiles
        self.numYTiles = numYTiles
        self.tiledBG = pygame.Surface((numXTiles * self.tw, numYTiles * tw)).convert()

        config = configparser.ConfigParser()
        config.read_file(open("gamemap.cfg"))
        self.zlevels = config.getint("map", "zlevels")
        self.currentZlevel = 0
        if not pygame.font.get_init():
            pygame.font.init()
        self.arialFnt = pygame.font.SysFont("Arial", 12)
        imageset = "images" + str(tw)
        digset = "digimages" + str(tw)
        self.images = str(config.get("tiles", imageset)).split(", ")
        self.digimages = str(config.get("tiles", digset)).split(", ")  # ['digx32.png']
        self.mapdata = [
            [[0 for cols in range(self.maph)] for rows in range(self.mapw)]
            for z in range(self.zlevels)
        ]  # [row for row in xrange(self.zlevels)]
        self.emapdata = [row for row in range(self.zlevels)]
        # ["wall1x32.png", "grassx32.png", "grass2x32.png", "grass3x32.png", "grass4x32.png", "waterx32.png", "magmax32.png", 'uprampx32.png', 'downrampx32.png']
        self.tileimages = []
        for i in self.images:
            tempimg, temprect = loader.load_png(i)
            self.tileimages.append((tempimg, temprect))

        self.digtileimages = []
        for i in self.digimages:
            tempimg, temprect = loader.load_png(i)
            self.digtileimages.append((tempimg, temprect))

    def initMap(self):
        mynoise = noise.Noise(self.mapw, self.maph, self.tw)
        mylist = mynoise.generate()
        # pprint(mylist)
        self.maprect = pygame.Rect(0, 0, self.mapw, self.maph)
        for z in range(self.zlevels):
            for x in range(self.mapw):
                for y in range(self.maph):
                    if self.firstnum(mylist[x][y]) == z:  # tile on the current layer
                        # print "grass"
                        # self.mapdata[z][x][y] = maptile.MapTile(random.randint(1, 4))
                        if self.secondnum(mylist[x][y]) < 7:
                            self.mapdata[z][x][y] = maptile.MapTile(
                                random.randint(1, 4)
                            )
                        else:
                            self.mapdata[z][x][y] = maptile.MapTile(7)
                        # put some ground
                    elif self.firstnum(mylist[x][y]) > z:  # tiles on the layers above
                        # print "dirt"
                        self.mapdata[z][x][y] = maptile.MapTile(0)
                        # dirt
                    elif self.firstnum(mylist[x][y]) < z:  # tiles below the z level
                        # print "nothing"
                        self.mapdata[z][x][y] = maptile.MapTile(5)
                    else:
                        print("x:", x)
                        print(" y:", y)
                        print("z:", z)
                        print("BOMBED")
                        exit()
                        # put nothing

    #        for z in xrange(self.zlevels):
    #            for x in xrange(self.mapw):
    #                for y in xrange(self.maph):
    #                    if self.firstnum(mylist[x][y]) == z:
    #                        if self.secondnum(mylist[x][y]) < 8:
    #                            self.mapdata[z][x][y] = maptile.MapTile(random.randint(1, 4))
    #                        else:
    #                            self.mapdata[z][x][y] = maptile.MapTile(7)
    #                    elif self.firstnum(mylist[x][y]) > z and self.firstnum(mylist[x][y]) == z + 1:
    #                        self.mapdata[z][x][y] = maptile.MapTile(0)
    #                    elif self.firstnum(mylist[x][y]) > z and self.firstnum(mylist[x][y]) != z + 1:
    #                        self.mapdata[z][x][y] = maptile.MapTile(0)
    #                    else:
    #                        self.mapdata[z][x][y] = maptile.MapTile(5)

    def firstnum(self, num):
        return int(str(num)[0])

    def secondnum(self, num):
        return int(str(num)[1])

    def belongs_to(self, num, start, end):
        if num >= start and num <= end:
            return True
        return False

    def initEMap(self):
        for z in range(self.zlevels):
            self.emapdata[z] = [
                [selected.Selected(1) for col in range(self.maph)]
                for row in range(self.mapw)
            ]
        self.emaprect = pygame.Rect(0, 0, self.mapw, self.maph)

    def drawEMap(self, zlevel):
        for x in range(int(self.startXTile), int(self.startXTile + self.numXTiles)):
            for y in range(int(self.startYTile), int(self.startYTile + self.numYTiles)):
                val = self.checkEMap(x, y, zlevel)
                for z in self.mapdata[zlevel][x][y].content:
                    if z is not None:
                        if z.selected:
                            self.tiledBG.blit(
                                z.image,
                                (
                                    (x - self.startXTile) * self.tw,
                                    (y - self.startYTile) * self.tw,
                                ),
                            )
                            self.tiledBG.blit(
                                self.digtileimages[3][0],
                                (
                                    (x - self.startXTile) * self.tw,
                                    (y - self.startYTile) * self.tw,
                                ),
                            )
                if val == 2:  # replace this with a big hash of images
                    image = 0
                    self.tiledBG.blit(
                        self.digtileimages[image][0],
                        (
                            (x - self.startXTile) * self.tw,
                            (y - self.startYTile) * self.tw,
                        ),
                    )
                elif val == 3:
                    image = 1
                    self.tiledBG.blit(
                        self.digtileimages[image][0],
                        (
                            (x - self.startXTile) * self.tw,
                            (y - self.startYTile) * self.tw,
                        ),
                    )
                elif val == 4:  # Drop location
                    image = 2
                    self.tiledBG.blit(
                        self.digtileimages[image][0],
                        (
                            (x - self.startXTile) * self.tw,
                            (y - self.startYTile) * self.tw,
                        ),
                    )
                elif val == 1:  # 1 empty
                    continue
        return self.tiledBG

    def drawMap(self, zlevel):
        for x in range(int(self.startXTile), int(self.startXTile + self.numXTiles)):
            for y in range(int(self.startYTile), int(self.startYTile + self.numYTiles)):
                val = self.checkMap(x, y, zlevel)
                if val == 5:
                    if self.checkMap(x, y, zlevel - 1) == 7:  # incline
                        val = 8
                    if self.checkMap(x, y, zlevel - 1) == 5:  # sky
                        val = 9
                self.tiledBG.blit(
                    self.tileimages[val][0],
                    ((x - self.startXTile) * self.tw, (y - self.startYTile) * self.tw),
                )
                for z in self.mapdata[zlevel][x][y].content:
                    if z is not None:
                        self.tiledBG.blit(
                            z.image,
                            (
                                (x - self.startXTile) * self.tw,
                                (y - self.startYTile) * self.tw,
                            ),
                        )

        return self.tiledBG

    def setBlocked(self, x, y, zlevel, blocked=True):
        """ True for blocked, False for passable """
        self.mapdata[zlevel][x][y].blocked = blocked

    def isBlocked(self, x, y, zlevel):
        x = int(x)
        y = int(y)
        val = self.mapdata[zlevel][x][y].blocked
        return val

    def checkMapContent(self, x, y, zlevel):
        x = int(x)
        y = int(y)
        val = self.mapdata[zlevel][x][y].content
        if val != []:
            return val
        else:
            return None

    def checkMap(self, x, y, zlevel):
        x = int(x)
        y = int(y)
        val = self.mapdata[zlevel][x][y].value
        # print str(val)
        return val

    def checkEMapQueue(self, x, y, zlevel):
        x = int(x)
        y = int(y)
        val = self.emapdata[zlevel][x][y].inqueue
        return val

    def checkEMap(self, x, y, zlevel):
        x = int(x)
        y = int(y)
        val = self.emapdata[zlevel][x][y].value
        return val

    def writeMap(self, x, y, zlevel, v):
        self.mapdata[zlevel][x][y].digTile(v)
        return v

    def writeEMapQueue(self, x, y, zlevel, v):
        x = int(x)
        y = int(y)
        # print str(x) + " , " + str(y) + " , " + str(zlevel)
        self.emapdata[zlevel][x][y].inqueue = v
        return v

    def writeEMap(self, x, y, zlevel, v):
        x = int(x)
        y = int(y)
        self.emapdata[zlevel][x][y].value = v
        return v

    def updateEMap(self, x, y, zlevel, v):
        mi = self.checkMap(x, y, zlevel)
        md = self.checkEMap(x, y, zlevel)
        if v[0] == "designate" and v[1] == "mining":
            if mi == 0:
                # print "Mining here: " + str(x) + ", " + str(y) + ", zlevel: " + str(zlevel)
                self.writeEMap(x, y, zlevel, 2)
            # else:
            # print "Cannot mine here: " + str(x) + ", " + str(y) + ", zlevel: " + str(zlevel)
        if v[0] == "designate" and v[1] == "remove":
            if md == 2:  # set this to just always remove
                # print "Removing here: " + str(x) + ", " + str(y) + ", zlevel: " + str(zlevel)
                self.writeEMap(x, y, zlevel, 1)
            # else:
            #    print "Cannot mine here: " + str(x) + ", " + str(y)
        if v[0] == "designate" and v[1] == "channel":
            if (
                mi != 0
            ):  # will need to fix this to appropriate tiles that can be channeled, righ now anything but walls works.
                # print "Channeling here: " + str(x) + ", " + str(y) + ", zlevel: " + str(zlevel)
                self.writeEMap(x, y, zlevel, 3)
            # else:
            #    print "Cannot channel here: " + str(x) + ", " + str(y)
        if v[0] == "designate" and v[1] == "drop":  # dropping items
            # only allow 1 drop off location
            drops = self.get_selected(4)
            for drop in drops:
                self.writeEMap(drop[0], drop[1], drop[2], 1)
            if mi != 0:
                #    print "setting Drop location: " + str(x) + ", " + str(y) + ", zlevel: " + str(zlevel)
                self.writeEMap(x, y, zlevel, 4)
            # else:
            #    print "Cannot cannot drop here: " + str(x) + ", " + str(y)

    def get_items_in_queue(self, x, y, z):
        content = self.checkMapContent(x, y, z)
        for item in content:
            if item.inqueue:
                return item
        return None

    def get_items(self, x, y, z):
        val = self.checkMapContent(x, y, z)
        if val is None:
            return None
        else:
            return val

    def select_items(self, x, y, z):
        val = self.checkMapContent(x, y, z)
        if val is not None:
            for item in val:
                if not item.inqueue:
                    item.selected = True
        else:
            return None

    def get_selected_items(self):
        selected = []
        for z in range(self.zlevels):
            for x in range(int(self.startXTile), int(self.startXTile + self.numXTiles)):
                for y in range(
                    int(self.startYTile), int(self.startYTile + self.numYTiles)
                ):
                    val = self.checkMapContent(x, y, z)
                    if val is not None:
                        for item in val:
                            if item.selected and not item.inqueue:
                                selected.append((x, y, z))
        return selected

    def get_selected(self, type):
        # will need to fix this also at some point to adjust for zlevels
        selected = []
        for z in range(self.zlevels):
            for x in range(int(self.startXTile), int(self.startXTile + self.numXTiles)):
                for y in range(
                    int(self.startYTile), int(self.startYTile + self.numYTiles)
                ):
                    val = self.checkEMap(x, y, z)
                    if val == 1:
                        continue
                    elif val == type:
                        selected.append((x, y, z))
        return selected

    def move_cost(self, c1, c2):
        """ Calculate the cost of moving between spots on the map (Euclidean) """
        return sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)

    def successors(self, c):
        # def successors(self, c, recurse = True):
        """Compute the successors of coordinate 'c': all the
        coordinates that can be reached by one step from 'c'.
        """
        slist = []
        calc_z = c[2]  # zlevel
        rangez = list(range(self.zlevels))
        minz = rangez.pop(0)
        maxz = rangez.pop()

        for drow in (-1, 0, 1):
            for dcol in (-1, 0, 1):
                if drow == 0 and dcol == 0:
                    continue
                newrow = c[0] + drow
                newcol = c[1] + dcol
                if newrow > self.mapw - 1:
                    continue
                if newcol > self.maph - 1:
                    continue
                tilevalue = self.mapdata[calc_z][newrow][newcol].value
                tileblocked = self.mapdata[calc_z][newrow][newcol].blocked
                if (
                    0 <= newrow <= self.mapw - 1 and 0 <= newcol <= self.maph - 1
                ) and not tileblocked:
                    slist.append((newrow, newcol, calc_z))  # fire the move in the queue
                    if (
                        tilevalue == 7
                        and calc_z + 1 <= maxz
                        and self.checkMap(newrow, newcol, calc_z + 1) == 5
                    ):  # up ramp
                        slist.append((newrow, newcol, calc_z + 1))
                elif (
                    tilevalue == 5
                    and calc_z - 1 >= minz
                    and self.checkMap(newrow, newcol, calc_z - 1) == 7
                ):  # down ramp
                    slist.append((newrow, newcol, calc_z - 1))
        return slist

    def valid_move(self, c):
        check = self.checkMap(c[0], c[1], c[2])
        if check == 5 or check == 0:
            return False
        return True

    def save_map(self):
        mapfile = open("./map.dat", "wb")
        pickle.dump(self.mapdata, mapfile, 2)
        mapfile.close

    def load_map(self):
        mapfile = open("./map.dat", "rb")
        self.mapdata = pickle.load(mapfile)
        mapfile.close

    def find_open_spot(self):
        for z in range(self.zlevels):
            for x in range(self.mapw):
                for y in range(self.maph):
                    if self.successors((x, y, z)):
                        val = self.checkMap(x, y, z)
                        if val == 1:
                            # if val == 7:
                            return (x, y, z)
