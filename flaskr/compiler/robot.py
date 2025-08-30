class Robot():
    def __init__(self):
        self.MAX_X = 10000
        self.MIN_X = 0

        self.MAX_Y = 10000
        self.MIN_Y = 0

        self.MAX_Z = 10000
        self.MIN_Z = 0

        self.__x = 0
        self.__y = 0
        self.__z = 0


    def move_x(self, value):
        if not value == None:
            if self.MIN_X < value < self.MAX_X:
                self.__x += value
                print(f"Move {value} on X axis, position on x: {self.__x}")
            else:
                print(f"[ERROR] move to far! X would be {value}")
        else:
                print(f"[ERROR] value is an 'NoneType'")

    def move_y(self, value):
        if not value == None:
            if self.MIN_Y < value < self.MAX_Y:
                self.__y += value
                print(f"Move {value} on Y axis, position on y: {self.__y}")
            else:
                print(f"[ERROR] move to far! Y would be {value}")
        else:
                print(f"[ERROR] value is an 'NoneType'")        

    def move_z(self, value):
        if not value == None:
            if self.MIN_Z < value < self.MAX_Z:
                self.__z += value
                print(f"Move {value} on Z axis, position on z: {self.__z}")
            else:
                print(f"[ERROR] move to far! Z would be {value}")
        else:
                print(f"[ERROR] value is an 'NoneType'")

    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    def get_z(self):
        return self.__z