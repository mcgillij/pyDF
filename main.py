#!C:\python26\python.exe
try:
    import sys
    from engine import engine
except ImportError as err:
    print("couldn't load module, %s" % (err))
    sys.exit(2)

# giver
if __name__ == '__main__':
    e = engine()
    e.run()
