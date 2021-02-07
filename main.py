try:
    import sys
    from engine import Engine
except ImportError as err:
    print("couldn't load module, %s" % (err))
    sys.exit(2)

# giver
if __name__ == "__main__":
    e = Engine()
    e.run()
