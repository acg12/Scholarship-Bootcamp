class Missile():
    def __init__(self, rect, angle, X, Y): 
        self.__rect = rect
        self.__angle = angle
        self.__X = X
        self.__Y = Y
        self.__frame = 0

    def getRect(self):
        return self.__rect

    def getX(self):
        return self.__rect.x

    def getY(self):
        return self.__rect.y

    def getAngle(self):
        return self.__angle
    
    def getFrame(self):
        return self.__frame
    
    def setFrame(self, frame):
        self.__frame = frame
    
    def move(self):
        if self.__Y == 0:
            x = -3
            y = 0
        else:
            y = 3
            x = (y / self.__Y) * self.__X
        self.__rect.y += y
        self.__rect.x += x