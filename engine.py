try:
    import pygame
    import sys

    # from pygame.locals import *
    from time import time
    import pickle
    from pprint import pprint
    import loader
    import mob
    import gamemap
    from job import Job
    import math
    import configparser, os
    import cursor
    import time
    import ezmenu
    from collections import defaultdict
    from pathfinder import PathFinder
    from intro import Intro
except ImportError as err:
    print("couldn't load module, %s" % (err))
    sys.exit(2)


class engine:
    def __init__(self):
        self.running = True  # set the game loop good to go
        config = configparser.ConfigParser()
        config.read_file(open("main.cfg"))
        self.fsw = config.getint("main", "fullscreenwidth")
        self.fsh = config.getint("main", "fullscreenheight")
        self.ww = config.getint("main", "windowedwidth")
        self.wh = config.getint("main", "windowedheight")
        self.tw = config.getint("main", "tilewidth")
        self.mapw = config.getint("main", "mapwidth")
        self.maph = config.getint("main", "mapheight")
        self.fullscreen = config.getboolean("main", "fullscreen")
        self.paused = False
        self.white = (255, 255, 255)  # the colour :)

        # fullscreen = False
        self.FPS = 60
        pygame.init()
        # setup the default screen size
        if self.fullscreen == True:
            self.screen = pygame.display.set_mode(
                (self.fsw, self.fsh), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode((self.ww, self.wh), pygame.RESIZABLE)

        pygame.display.set_caption("pyDF")
        # Intro's on by default, will need to add a config file entry for this.
        self.intro = True
        self.mainclock = pygame.time.Clock()
        # various rendering offsets
        self.vpRenderOffset = (self.tw, self.tw)
        self.statsOffset = (math.floor(int(0.8 * self.ww) + 2 * self.tw), self.tw)
        self.menuOffset = (math.floor(int(0.8 * self.ww) + 2 * self.tw), 4 * self.tw)
        self.menuOffset2 = (math.floor(int(0.8 * self.ww) + 2 * self.tw), 5 * self.tw)
        self.menuOffset3 = (
            math.floor(int(0.8 * self.ww) + 2 * self.tw),
            6 * self.tw,
        )  # testing for ezmenu
        self.idleOffset = (
            math.floor(int(0.8 * self.ww) + 2 * self.tw),
            0,
        )  # testing for ezmenu
        self.pauseDisplayOffset = (self.tw, 0)
        self.digTypeOffset = (math.floor(int(0.8 * self.ww) + 2 * self.tw), 4 * self.tw)
        self.showmenu = False
        self.currentmenu = None
        self.vpCoordinate = [0, 0]  # Starting coordinates for the view port
        self.vpDimensions = (
            math.floor(int(0.8 * self.ww) / self.tw) * self.tw,
            math.floor(int(0.9 * self.wh) / self.tw) * self.tw,
        )  # resolution of the view port
        self.vpStep = self.tw  # move 1 tile over.
        self.vpShiftStep = self.tw * 10  # move 10 tile over.
        self.minHorizScrollBound = 0
        self.minVertScrollBound = 0
        self.maxHorizScrollBound = self.mapw * self.tw
        self.maxVertScrollBound = self.maph * self.tw
        self.numXTiles = int(
            math.ceil(int(self.vpDimensions[0]) / self.tw)
        )  # the number of tiles to be shown at one time for X
        self.numYTiles = int(
            math.ceil(int(self.vpDimensions[1]) / self.tw)
        )  # the number of tiles to be shown at one time for y
        self.startXTile = math.floor(int(self.vpCoordinate[0]) / self.tw)
        self.startYTile = math.floor(int(self.vpCoordinate[1]) / self.tw)

        if not pygame.font.get_init():
            pygame.font.init()
        self.arialFnt = pygame.font.SysFont("Arial", 16)
        self.m = gamemap.GameMap(
            self.tw,
            self.mapw,
            self.maph,
            self.startXTile,
            self.startYTile,
            self.numXTiles,
            self.numYTiles,
        )
        self.m.initMap()
        self.m.initEMap()
        self.editmode = [None, None]
        self.selectmode = False
        self.testmode = False
        self.room_tiles = []
        self.selectcursor = cursor.Cursor(
            self.tw, self.m.numXTiles / 2 * self.tw, self.m.numYTiles / 2 * self.tw
        )
        self.queued_jobs = []
        self.mobs = []
        self.mapvalue = None
        self.tilecontent = None
        # self.currentZlevel = self.m.currentZlevel
        openspot = self.m.find_open_spot()
        self.currentZlevel = openspot[2]
        self.mobs.append(mob.Mob(openspot, self.tw))
        self.addTileMob(openspot[0], openspot[1], openspot[2], self.mobs[0])
        self.mobs.append(mob.Mob(openspot, self.tw))
        self.addTileMob(openspot[0], openspot[1], openspot[2], self.mobs[0])
        self.mobs.append(mob.Mob(openspot, self.tw))
        self.addTileMob(openspot[0], openspot[1], openspot[2], self.mobs[0])
        self.buttons = {}
        # self.keys = set()
        self.motion = None

    def _recompute_path(self, _map, start, end):
        pf = PathFinder(_map.successors, _map.move_cost, _map.move_cost)
        # t = time.process_time()
        pathlines = list(pf.compute_path(start, end))

        # dt = time.process_time() - t
        if pathlines == []:
            print("No path found")
            return pathlines
        else:
            print("Found path (length %d)" % len(pathlines))
            return pathlines
        # self.path_valid = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return
            elif event.type == pygame.KEYDOWN:
                self.handle_keyboard(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.buttons[event.button] = event.pos
            elif event.type == pygame.MOUSEMOTION:
                dir(event)
                pprint(event)
                self.motion = event.pos
                # self.motion = event
            elif event.type == pygame.MOUSEBUTTONUP:
                del self.buttons[event.button]
            elif event.type == pygame.VIDEORESIZE:
                # allow for the window to be resized manually.
                self.ww, self.wh = event.w, event.h
                pygame.display.set_mode((self.ww, self.wh), pygame.RESIZABLE)
                newwidth = math.floor(int(0.8 * self.ww) / self.tw)
                newheight = math.floor(int(0.9 * self.wh) / self.tw)
                self.statsOffset = (
                    math.floor(int(0.8 * self.ww) + 2 * self.tw),
                    self.tw,
                )
                self.vpDimensions = (
                    newwidth * self.tw,
                    newheight * self.tw,
                )  # resolution of the view port
                self.m.numXTiles = int(
                    math.ceil(int(self.vpDimensions[0]) / self.tw)
                )  # the number of tiles to be shown at one time for X
                self.m.numYTiles = int(
                    math.ceil(int(self.vpDimensions[1]) / self.tw)
                )  # the number of tiles to be shown at one time for y
                self.m.tiledBG = pygame.Surface(
                    (self.m.numXTiles * self.tw, self.m.numYTiles * self.tw)
                ).convert()
                self.fullscreen = False

    def logic(self):
        self.handle_events()
        self.handle_mouse()
        self.handle_viewport()
        if self.paused == False:

            # build the queue
            self.mining()
            self.channel()
            self.moveitem()
            # process the queue
            pprint(self.queued_jobs)
            self.move_mobs()
            self.mob_logic()
            self.handle_logic()

    def showIntro(self):
        intro = Intro()
        text_list = [
            "Welcome to PyDF",
            "d + mouse for digging",
            "h + mouse for channeling",
            "i + mouse to designate item dump",
            "o + mouse selects items for dumping",
            "k + arrows to inspect tile content",
            "s to save or l to load map from disk",
            "arrow keys to move the viewport around",
            "shift + < or > goes UP and DOWN Z levels",
            "shift + arrow keys to move 10 tiles at a time",
            "spacebar unpauses the game or pauses",
            "Esc quits",
            "",
            "Press any key to continue",
        ]
        hoffset = self.tw
        voffset = self.tw * 2
        for item in text_list:
            intro.drawText(item, self.screen, hoffset, voffset)
            voffset += self.tw * 2

        pygame.display.update()
        intro.waitForKey()
        self.intro = False

    def cleanup(self):
        pygame.quit()

    def quit(self):
        self.running = False

    def pausegame(self):
        if self.paused == True:
            self.showmenu = False
            self.selectMode = False
            self.editmode = [None, None]
            self.paused = False
        else:
            self.paused = True
        # no longer running a seperate loop for pause, handled by the various modes
        # while self.paused:
        #    for event in pygame.event.get():
        #        if event.type == KEYDOWN and event.key == K_SPACE:
        #            self.paused = False

    def moveitem(self):
        selected = self.m.get_selected_items()
        dropoff = self.m.get_selected(4)
        if dropoff == []:
            return
        else:
            for coord in selected:  # change this at some point
                adjacent_open_tiles = self.m.successors(coord)
                queue = []
                if adjacent_open_tiles != []:
                    queue.append(coord)
                if len(queue):
                    for move in queue:
                        if len(self.m.successors(move)):
                            content = self.m.get_items(move[0], move[1], move[2])
                            if content != None:
                                for item in content:
                                    if item.selected == True and item.inqueue == False:
                                        item.inqueue = True
                                        self.queued_jobs.append(
                                            Job("MoveItem", move, dropoff)
                                        )
                                        continue

    def channel(self):
        selected = self.m.get_selected(3)
        for coord in selected:  # change this at some point
            # checking if the neighboring tiles are accessible from 1 tile away in every direction
            # would have to make this more intelligent in the future, but it works for now.
            adjacent_open_tiles = self.m.successors(coord)
            queue = []
            if adjacent_open_tiles != []:
                queue.append(coord)
            if len(queue):
                dest = queue.pop(0)
                # if self.m.checkEMapQueue(dest[0], dest[1], dest[2]) == True:
                #   continue
                list_of_moves = self.m.successors(dest)
                for move in list_of_moves:
                    if len(self.m.successors(move)):
                        # dest[2] = dest[2] -1 #channel digs a zlevel below but creates a ramp
                        self.m.writeEMapQueue(dest[0], dest[1], dest[2], True)
                        self.queued_jobs.append(Job("Channeling", move, dest))
                        continue

    def mining(self):
        selected = self.m.get_selected(2)
        print("Selected: ", selected)
        for coord in selected:  # change this at some point
            # checking if the neighboring tiles are accessible from 1 tile away in every direction
            # would have to make this more intelligent in the future, but it works for now.
            job = self.find_mining_job(coord)
            inqueue = False
            if job:  # check if the dorfs already have that job
                for m in self.mobs:
                    if m.job != None:
                        if (
                            m.job.name == job.name
                            and m.job.move == job.move
                            and m.job.dest == job.dest
                        ):
                            inqueue = True
                        continue

            if inqueue == False and job:
                self.m.writeEMapQueue(job.dest[0], job.dest[1], job.dest[2], True)
                self.queued_jobs.append(job)

    def find_mining_job(self, coord):
        adjacent_open_tiles = self.m.successors(coord)
        queue = []
        if adjacent_open_tiles != []:
            queue.append(coord)
        if len(queue):
            dest = queue.pop(0)
            # if self.m.checkEMapQueue(dest[0], dest[1], dest[2]) == True:
            #   continue
            list_of_moves = self.m.successors(dest)
            for move in list_of_moves:
                if len(self.m.successors(move)):
                    return Job("Mining", move, dest)
        return None

    def expand_selection(self, coord):
        pprint(coord)
        list_selection = self.m.successors(coord)
        for item in list_selection:
            if item in self.room_tiles:
                print("already in list")
            else:
                self.room_tiles.append(item)

    def menu(self, menu_list):
        if self.showmenu == False:
            self.currentmenu = ezmenu.EzMenu(menu_list)
            self.currentmenu.set_pos(self.menuOffset3[0], self.menuOffset3[1])
            self.currentmenu.set_font(self.arialFnt)
            self.currentmenu.set_highlight_color((0, 255, 0))
            self.currentmenu.set_normal_color(self.white)
        self.showmenu = True

    def handle_keyboard(self, event):
        keymods = pygame.key.get_mods()
        if event.key == ord("k"):  # and self.selectmode == False:
            self.paused = True
            if self.selectmode == False:
                self.selectmode = True
            else:
                self.selectmode = False
                self.showmenu = False

        elif event.key == ord("d"):
            self.paused = True
            # print "mining"
            self.editmode = ["designate", "mining"]
        elif event.key == ord("h"):
            self.paused = True
            # print "channeling"
            self.editmode = ["designate", "channel"]
        elif event.key == ord("i"):
            self.paused = True
            # print "Item Drop location"
            self.editmode = ["designate", "drop"]
        elif event.key == ord("o"):
            self.paused = True
            # print "select items to move"
            self.editmode = ["designate", "itemselect"]
        elif event.key == ord("x"):
            self.paused = True
            # print "REMOVE MODE"
            self.editmode[1] = "remove"
        elif event.key == ord("l"):
            self.paused = True
            # print "Loading map"
            self.m.load_map()
        elif event.key == ord("s"):
            self.paused = True
            # print "Saving map"
            self.m.save_map()
        elif event.key == ord("t"):
            self.paused = True
            # print "Testing "
            if self.testmode == False:
                pprint(self.testmode)
                self.testmode = True
            else:
                print("testing")
                pprint(self.testmode)
                self.testmode = False
                self.room_tiles = []

        elif (
            event.key == ord("n") and self.testmode == True and self.selectmode == True
        ):
            mapx = (self.selectcursor.position[0] + self.vpCoordinate[0]) / self.tw
            mapy = (self.selectcursor.position[1] + self.vpCoordinate[1]) / self.tw
            if self.room_tiles == []:
                self.expand_selection((mapx, mapy, self.currentZlevel))
            else:
                room_list = self.room_tiles
                for item in room_list:
                    self.expand_selection((item[0], item[1], self.currentZlevel))

            pprint(self.room_tiles)
        elif (
            event.key == ord("m") and self.testmode == True and self.selectmode == True
        ):
            print("Decreasing")

        elif event.key == pygame.K_ESCAPE:
            self.quit()
        elif event.key == pygame.K_SPACE:
            # print "PAUSING OR UNPAUSING"
            self.pausegame()

        # move the menu selector:
        elif (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and (
            keymods & pygame.KMOD_LALT
            and self.showmenu == True
            and self.currentmenu != None
        ):
            self.currentmenu.update(event)
        elif (
            event.key == pygame.K_RETURN
            and self.showmenu == True
            and self.currentmenu != None
            and self.selectmode == True
        ):
            self.currentmenu.update(event)

        # Movement Keys l,r,u,d
        # Cursor Movement

        elif event.key == pygame.K_LEFT and self.selectmode == True:
            if keymods & pygame.KMOD_LSHIFT:
                self.selectcursor.position[0] = (
                    self.selectcursor.position[0] - self.vpShiftStep
                )
            else:
                self.selectcursor.position[0] = (
                    self.selectcursor.position[0] - self.vpStep
                )

        elif event.key == pygame.K_RIGHT and self.selectmode == True:
            if keymods & pygame.KMOD_LSHIFT:
                self.selectcursor.position[0] = (
                    self.selectcursor.position[0] + self.vpShiftStep
                )
            else:
                self.selectcursor.position[0] = (
                    self.selectcursor.position[0] + self.vpStep
                )

        elif (
            event.key == pygame.K_UP
            and self.selectmode == True
            and self.testmode == False
        ):
            if keymods & pygame.KMOD_LSHIFT:
                self.selectcursor.position[1] = (
                    self.selectcursor.position[1] - self.vpShiftStep
                )
            else:
                self.selectcursor.position[1] = (
                    self.selectcursor.position[1] - self.vpStep
                )

        elif (
            event.key == pygame.K_DOWN
            and self.selectmode == True
            and self.testmode == False
        ):
            if keymods & pygame.KMOD_LSHIFT:
                self.selectcursor.position[1] = (
                    self.selectcursor.position[1] + self.vpShiftStep
                )
            else:
                self.selectcursor.position[1] = (
                    self.selectcursor.position[1] + self.vpStep
                )

        # move up and down zlevels.
        elif (
            event.key == pygame.K_COMMA
            and self.selectmode == False
            and keymods & pygame.KMOD_LSHIFT
        ):
            if self.currentZlevel + 1 in range(self.m.zlevels):
                self.currentZlevel = self.currentZlevel + 1
        elif (
            event.key == pygame.K_PERIOD
            and self.selectmode == False
            and keymods & pygame.KMOD_LSHIFT
        ):
            if self.currentZlevel - 1 in range(self.m.zlevels):
                self.currentZlevel = self.currentZlevel - 1

        # View port Movement
        elif event.key == pygame.K_LEFT and self.selectmode == False:
            if keymods & pygame.KMOD_LSHIFT:
                self.vpCoordinate[0] = self.vpCoordinate[0] - self.vpShiftStep
            else:
                self.vpCoordinate[0] = self.vpCoordinate[0] - self.vpStep

        elif event.key == pygame.K_RIGHT and self.selectmode == False:
            if keymods & pygame.KMOD_LSHIFT:
                self.vpCoordinate[0] = self.vpCoordinate[0] + self.vpShiftStep
            else:
                self.vpCoordinate[0] = self.vpCoordinate[0] + self.vpStep

        elif event.key == pygame.K_UP and self.selectmode == False:
            if keymods & pygame.KMOD_LSHIFT:
                self.vpCoordinate[1] = self.vpCoordinate[1] - self.vpShiftStep
            else:
                self.vpCoordinate[1] = self.vpCoordinate[1] - self.vpStep
        elif event.key == pygame.K_DOWN and self.selectmode == False:
            if keymods & pygame.KMOD_LSHIFT:
                self.vpCoordinate[1] = self.vpCoordinate[1] + self.vpShiftStep
            else:
                self.vpCoordinate[1] = self.vpCoordinate[1] + self.vpStep

        # reset viewport
        elif event.key == pygame.K_F11:
            if self.fullscreen == False:
                pygame.display.set_mode((self.fsw, self.fsh), pygame.FULLSCREEN, 32)
                newwidth = math.floor(int(0.8 * self.fsw) / self.tw)
                newheight = math.floor(int(0.9 * self.fsh) / self.tw)
                self.statsOffset = (
                    math.floor(int(0.8 * self.fsw) + 2 * self.tw),
                    self.tw,
                )
                self.vpDimensions = (
                    newwidth * self.tw,
                    newheight * self.tw,
                )  # resolution of the view port
                self.m.numXTiles = int(
                    math.ceil(int(self.vpDimensions[0]) / self.tw)
                )  # tiles to be shown at one time for X
                self.m.numYTiles = int(
                    math.ceil(int(self.vpDimensions[1]) / self.tw)
                )  # tiles to be shown at one time for y
                self.m.tiledBG = pygame.Surface(
                    (self.m.numXTiles * self.tw, self.m.numYTiles * self.tw)
                ).convert()
                self.fullscreen = True
            elif self.fullscreen == True:
                pygame.display.set_mode((self.ww, self.wh), pygame.RESIZABLE)
                newwidth = math.floor(int(0.8 * self.ww) / self.tw)
                newheight = math.floor(int(0.9 * self.wh) / self.tw)
                self.statsOffset = (
                    math.floor(int(0.8 * self.ww) + 2 * self.tw),
                    self.tw,
                )
                self.vpDimensions = (
                    newwidth * self.tw,
                    newheight * self.tw,
                )  # resolution of the view port
                self.m.numXTiles = int(
                    math.ceil(int(self.vpDimensions[0]) / self.tw)
                )  # tiles to be shown at one time for X
                self.m.numYTiles = int(
                    math.ceil(int(self.vpDimensions[1]) / self.tw)
                )  # tiles to be shown at one time for y
                self.m.tiledBG = pygame.Surface(
                    (self.m.numXTiles * self.tw, self.m.numYTiles * self.tw)
                ).convert()
                self.fullscreen = False

    def handle_mouse(self):
        MOUSE_BUTTON_ONE = 1
        pprint(f"mousemotion: {pygame.MOUSEMOTION}")
        pprint(f"self.motion: {self.motion}")
        if (
            MOUSE_BUTTON_ONE in self.buttons
            and self.editmode[0] == "designate"
            and self.editmode[1] == "itemselect"
        ):
            mx, my = pygame.mouse.get_pos()
            # mx = self.motion.pos[0]
            # my = self.motion.pos[1]
            if (
                mx < self.m.numXTiles * self.tw + self.vpRenderOffset[0]
                and my < self.m.numYTiles * self.tw + self.vpRenderOffset[1]
            ):  # within the map viewport
                self.m.select_items(
                    (mx - self.vpRenderOffset[0] + self.vpCoordinate[0]) / self.tw,
                    (my - self.vpRenderOffset[1] + self.vpCoordinate[1]) / self.tw,
                    self.currentZlevel,
                )

        # drop point for items
        if (
            MOUSE_BUTTON_ONE in self.buttons
            and self.editmode[0] == "designate"
            and self.editmode[1] == "drop"
        ):
            mx, my = pygame.mouse.get_pos()
            # mx = self.motion.pos[0]
            # my = self.motion.pos[1]
            if (
                mx < self.m.numXTiles * self.tw + self.vpRenderOffset[0]
                and my < self.m.numYTiles * self.tw + self.vpRenderOffset[1]
            ):  # within the map viewport
                self.m.updateEMap(
                    (mx - self.vpRenderOffset[0] + self.vpCoordinate[0]) / self.tw,
                    (my - self.vpRenderOffset[1] + self.vpCoordinate[1]) / self.tw,
                    self.currentZlevel,
                    self.editmode,
                )

        if MOUSE_BUTTON_ONE in self.buttons and self.editmode[0] == "designate":
            mx, my = pygame.mouse.get_pos()
            # mx = self.motion.pos[0]
            # my = self.motion.pos[1]
            if (
                mx < self.m.numXTiles * self.tw + self.vpRenderOffset[0]
                and my < self.m.numYTiles * self.tw + self.vpRenderOffset[1]
            ):  # within the map viewport
                self.m.updateEMap(
                    (mx - self.vpRenderOffset[0] + self.vpCoordinate[0]) / self.tw,
                    (my - self.vpRenderOffset[1] + self.vpCoordinate[1]) / self.tw,
                    self.currentZlevel,
                    self.editmode,
                )

        # if MOUSE_BUTTON_ONE in self.buttons and self.editmode[0] == "designate":

    #   if MOUSE_BUTTON_ONE in self.buttons and self.motion == pygame.MOUSEMOTION.pos and self.editmode[0] == "designate":
    #        mx = self.motion.pos[0]
    #       my = self.motion.pos[1]
    #       if mx < self.m.numXTiles * self.tw + self.vpRenderOffset[0] and my < self.m.numYTiles * self.tw + self.vpRenderOffset[1]: #within the map viewport
    #           self.m.updateEMap((mx - self.vpRenderOffset[0] + self.vpCoordinate[0]) / self.tw, (my - self.vpRenderOffset[1] + self.vpCoordinate[1]) / self.tw, self.currentZlevel, self.editmode)

    def handle_viewport(self):
        # Restrict Cursor Movement.
        if self.selectmode == True:
            if self.selectcursor.position[0] < 0:
                self.selectcursor.position[0] = 0
            if self.selectcursor.position[0] > self.m.numXTiles * self.tw:
                self.selectcursor.position[0] = self.vpDimensions[0] - self.tw
            if self.selectcursor.position[1] < 0:
                self.selectcursor.position[1] = 0
            if self.selectcursor.position[1] > self.m.numYTiles * self.tw:
                self.selectcursor.position[1] = self.vpDimensions[1] - self.tw

            self.selectcursor.mapx = (
                self.selectcursor.position[0] + self.vpCoordinate[0]
            ) / self.tw
            self.selectcursor.mapy = (
                self.selectcursor.position[1] + self.vpCoordinate[1]
            ) / self.tw
            # list = [['item1', 'data1'],['item2', 'data2'],['item3', 'data3']]
            self.mapvalue = self.m.checkMap(
                self.selectcursor.mapx, self.selectcursor.mapy, self.currentZlevel
            )
            self.tilecontent = self.m.checkMapContent(
                self.selectcursor.mapx, self.selectcursor.mapy, self.currentZlevel
            )
            if self.tilecontent != None:
                self.menu(self.tilecontent)
            else:
                self.showmenu = False
                self.currentmenu = None
        # view port reset.
        if self.vpCoordinate[0] < 0:
            self.vpCoordinate[0] = 0
        if self.vpCoordinate[0] + self.vpDimensions[0] > self.maxHorizScrollBound:
            self.vpCoordinate[0] = self.maxHorizScrollBound - self.vpDimensions[0]
        if self.vpCoordinate[1] < 0:
            self.vpCoordinate[1] = 0
        if self.vpCoordinate[1] + self.vpDimensions[1] > self.maxVertScrollBound:
            self.vpCoordinate[1] = self.maxVertScrollBound - self.vpDimensions[1]

    def addTileContent(self, x, y, zlevel, content):
        val = self.m.mapdata[zlevel][x][y].addMob(content)
        return val

    def delTileContent(self, x, y, zlevel, content):
        val = self.m.mapdata[zlevel][x][y].removeMob(content)
        return val

    def addTileMob(self, x, y, zlevel, mob):
        val = self.m.mapdata[zlevel][x][y].addMob(mob)
        return val

    def delTileMob(self, x, y, zlevel, mob):
        val = self.m.mapdata[zlevel][x][y].removeMob(mob)
        return val

    def moveMob(self, x, y, zlevel, mob):
        # x, y, z
        oldx, oldy, oldz = mob.position[0], mob.position[1], mob.position[2]
        self.addTileMob(x, y, zlevel, mob)  # this will need to be adjusted
        self.delTileMob(oldx, oldy, oldz, mob)  # this also will need to be adjusted
        mob.position = (x, y, zlevel)

    def idle_dwarves(self):
        counter = 0
        for mo in self.mobs:
            if mo.job == None:
                #   print "+1 idler"
                counter = counter + 1
        return counter

    def move_mobs(self):
        for mob in self.mobs:
            if len(mob.pathlines) > 0:
                # print "Has a path, walking 1 step of the path"
                move = mob.pathlines.pop(0)
                self.moveMob(move[0], move[1], move[2], mob)
            else:
                if mob.job:
                    print("No pathlines, attempting to snag some")
                    path = self._recompute_path(self.m, mob.position, mob.job.move)
                    # pprint(path)
                    if path != []:
                        # print "path found"
                        mob.pathlines = path
                    else:
                        mob.job = None

    def mob_logic(self):
        for mob in self.mobs:
            if mob.job != None:
                if mob.position == mob.job.move:
                    if mob.job.name == "Channeling":
                        # print "Channeling..."
                        digtype = 7  # create an up ramp
                        diglevel = mob.job.dest[2] - 1  # the z level below
                        self.m.writeMap(
                            mob.job.dest[0], mob.job.dest[1], diglevel, digtype
                        )  # default to a green tile for now.
                        self.m.setBlocked(
                            mob.job.dest[0], mob.job.dest[1], diglevel, False
                        )  # unblock the tile
                        digtype = 5  # put an empty tile on top
                        self.m.writeMap(
                            mob.job.dest[0], mob.job.dest[1], mob.job.dest[2], digtype
                        )  # default to a green tile for now.
                        self.m.writeEMap(
                            mob.job.dest[0], mob.job.dest[1], mob.job.dest[2], 1
                        )  # default to a empty tile for now.
                        self.m.writeEMapQueue(
                            mob.job.dest[0], mob.job.dest[1], mob.job.dest[2], False
                        )
                        self.m.setBlocked(
                            mob.job.dest[0], mob.job.dest[1], mob.job.dest[2], True
                        )  # unblock the tile
                        mob.job = None
                    elif mob.job.name == "Mining":
                        # print "Mining..."
                        digtype = 1
                        self.m.writeMap(
                            mob.job.dest[0], mob.job.dest[1], mob.job.dest[2], digtype
                        )  # default to a green tile for now.
                        self.m.writeEMap(
                            mob.job.dest[0], mob.job.dest[1], mob.job.dest[2], 1
                        )  # default to a empty tile for now.
                        self.m.writeEMapQueue(
                            mob.job.dest[0], mob.job.dest[1], mob.job.dest[2], False
                        )
                        self.m.setBlocked(
                            mob.job.dest[0], mob.job.dest[1], mob.job.dest[2], False
                        )  # unblock the tile
                        mob.job = None
                    elif mob.job.name == "MoveItem":
                        # print "Picking up Item"
                        if (
                            self.m.get_items_in_queue(
                                mob.position[0], mob.position[1], mob.position[2]
                            )
                            != None
                        ):
                            val = self.m.mapdata[mob.position[2]][mob.position[0]][
                                mob.position[1]
                            ].pickup()
                            mob.carrying = val
                            mob.job = Job("DropItem", mob.job.dest[0], mob.job.dest[0])
                            mob.pathlines = self._recompute_path(
                                self.m, mob.position, mob.dest
                            )
                        else:
                            print("Job Canceled, no items left")
                            print("SHOULD NOT GET HERE")
                            # mob.job = None #.clearjob()
                    elif mo.job.name == "DropItem":
                        # print "Dropping Item"
                        # print "Item"
                        # pprint(mo.carrying)
                        mob.carrying.selected = (
                            False  # set the item to false before dropping it.
                        )
                        mob.carrying.inqueue = (
                            False  # set the item to false before dropping it.
                        )
                        self.m.mapdata[mob.job.dest[2]][mob.job.dest[0]][
                            mob.job.dest[1]
                        ].add(mob.carrying)
                        mob.carrying = None
                        mob.job = None  # .clearjob()

            else:
                # print "no Job" # get one
                if len(self.queued_jobs) > 0:
                    mob.job = self.queued_jobs.pop(0)

    def handle_logic(self):
        # pprint (self.queued_jobs)
        # Move Loop
        self.m.startXTile = math.floor(float(self.vpCoordinate[0]) / self.tw)
        self.m.startYTile = math.floor(float(self.vpCoordinate[1]) / self.tw)
        # tick busy
        dt = self.mainclock.tick_busy_loop(self.FPS)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.m.drawMap(self.currentZlevel)
        self.finalmap = self.m.drawEMap(self.currentZlevel)
        self.screen.blit(
            self.arialFnt.render("Idle: " + str(self.idle_dwarves()), True, self.white),
            self.idleOffset,
        )
        # Cursor
        if self.selectmode == True:
            self.finalmap.blit(self.selectcursor.image, self.selectcursor.position)
            if self.testmode == True and self.room_tiles:
                for pos in self.room_tiles:
                    self.finalmap.blit(
                        self.selectcursor.image,
                        [
                            pos[0] * self.tw + self.vpCoordinate[0],
                            pos[1] * self.tw + self.vpCoordinate[1],
                        ],
                    )
            self.screen.blit(
                self.arialFnt.render("value: " + str(self.mapvalue), True, self.white),
                self.menuOffset,
            )
            self.screen.blit(
                self.arialFnt.render(
                    "content: " + str(self.tilecontent), True, self.white
                ),
                self.menuOffset2,
            )
        if self.showmenu == True:
            self.currentmenu.draw(self.screen)
        if self.paused == True:
            self.screen.blit(
                self.arialFnt.render("Paused", True, self.white),
                self.pauseDisplayOffset,
            )
        if self.editmode != [None, None]:
            self.screen.blit(
                self.arialFnt.render(
                    "Digging: " + str(self.editmode[1]), True, self.white
                ),
                self.digTypeOffset,
            )

        self.screen.blit(
            self.finalmap,
            self.vpRenderOffset,
            (
                self.vpCoordinate[0] - (self.m.startXTile * self.tw),
                (self.vpCoordinate[1] - (self.m.startYTile * self.tw)),
            )
            + self.vpDimensions,
        )
        self.screen.blit(
            self.arialFnt.render(
                "coordinates: "
                + str(self.vpCoordinate[0])
                + ", "
                + str(self.vpCoordinate[1])
                + " Z: "
                + str(self.currentZlevel),
                True,
                self.white,
            ),
            self.statsOffset,
        )
        # screen filling goes here
        for mo in self.mobs:
            if (
                mo.position[2] == self.currentZlevel
            ):  # only render the dorfs on the current level
                self.screen.blit(
                    mo.image,
                    self.vpRenderOffset,
                    (
                        self.vpCoordinate[0] - (mo.position[0] * self.tw),
                        (self.vpCoordinate[1] - (mo.position[1] * self.tw)),
                    )
                    + self.vpDimensions,
                )

        self.mainclock.tick(self.FPS)
        # pygame.display.update()
        pygame.display.flip()

    def run(self):
        if self.intro == True:
            self.showIntro()
        while self.running:
            self.logic()
            self.render()
        self.cleanup()


# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    e = engine()
    e.run()
