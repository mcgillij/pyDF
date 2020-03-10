try:
    from loader import load_png
    import configparser, os
except ImportError as err:
    print("couldn't load module. %s" % (err))
    sys.exit(2)

class Cursor():
    """ Cursor class, generic class for a Cursor """
    def __init__(self, tw, x, y):
        self.tw = tw
        self.position = [x, y]
        self.mapx = 0
        self.mapy = 0
        config = configparser.ConfigParser()
        config.read_file(open('cursor.cfg'))
        sectionname = "imagename" + str(tw)
        imagename = config.get('cursor', sectionname)
        self.image, self.rect = load_png(imagename)
    
