import os

if __name__ == '__main__':
    for path, subdirs, files in os.walk("Letters"):
        for name in files:
            nameshort = name[-5:]
            join = os.path.join(path, name)
            joinupdated = os.path.join(path, nameshort)
            print(join, joinupdated)
            os.rename(join, joinupdated)
