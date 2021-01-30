try:
    from item import Item
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)


class MapTile:
    """ MapTile class, generic class for a tile """

    def __init__(self, value):
        self.value = value
        self.content = []
        self.mobs = []
        if int(self.value) == int(0) or int(self.value) == int(5):
            self.blocked = True
        else:
            self.blocked = False

    def digTile(self, value):
        oldvalue = self.value
        self.value = value
        self.add(Item("crumbledwall", 16))

    def addMob(self, mob):
        self.mobs.append(mob)
        return self.mobs

    def removeMob(self, mob):
        self.mobs.append(mob)
        return self.mobs

    def add(self, content):
        self.content.append(content)
        return self.content

    def remove(self, content):
        self.content.remove(content)
        return self.content

    def pickup(self):
        for item in self.content:
            if item.selected == True:
                val = item
                self.remove(item)
                return val
        return None
