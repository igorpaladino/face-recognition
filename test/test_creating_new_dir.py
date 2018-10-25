import os

index = 1
createDir = False
while not createDir:
    newpath = ((r'images/pack%s') %(index))
    if os.path.exists(newpath):
        index+=1
    else:
        os.makedirs(newpath)
        createDir = True