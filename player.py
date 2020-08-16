class Player :
    def __init__(self, id_player, origin_coord) :
        self._id = id_player
        self._current_coord = origin_coord
        self._points = 0
        self._start_coord = origin_coord
    
    @property
    def id(self):
        return self._id

    @property
    def current_coord(self):
        return self._current_coord
    @current_coord.setter
    def current_coord(self, new_coord):
        self._current_coord = new_coord

    @property
    def x(self):
        x,_ = self.current_coord
        return x
    @x.setter
    def x(self, new_x):
        x,y = self.current_coord
        x = new_x
        self.current_coord((x,y))
    
    @property
    def y(self):
        _,y = self.current_coord
        return y
    @y.setter
    def y(self, new_y):
        x,y = self.current_coord
        y = new_y
        self.current_coord((x,y))

    @property
    def points(self):
        return self._points
    @points.setter
    def points(self, new_nb):
        self._points = new_nb

    def reset_player(self):
       self.current_coord = self._start_coord
       self._case_claimed = 0
    
    def move(self, direction = None):
        x,y = self._current_coord
        if direction == "up":
            new_x = x - 1
            new_y = y 
        elif direction == "down":
            new_x = x + 1
            new_y = y 
        elif direction == "left":
            new_x = x 
            new_y = y - 1
        elif direction == "right":
            new_x = x 
            new_y = y + 1
        else :
            new_x = x
            new_y = y
        return (new_x, new_y)
    
    def play(self):
        correct_moves = ["up", "down", "right", "left"]
        action = ""
        while(str.lower(action) not in correct_moves):
            action = input("Player {} >>> ".format(self.id))
        return action