class Explosion():
    def __init__(self, frame, x, y):
        self.__frame = frame
        self.__x = x
        self.__y = y
    
    def getFrame(self):
        return self.__frame
    
    def setFrame(self, frame):
        self.__frame = frame
        
    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y