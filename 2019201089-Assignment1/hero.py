from color import color
from stack import stack
from Cell import directions

direction = directions()

class hero:
    moving = None
    degree = None
    eye_status = None
    rolling_status = None
    walk_status = None
    goal_ceremony_status = None
    body_color = color(.3, .4, .6)

    __current_x, __current_y = None, None
    __old_x, __old_y = None, None

    get_goal, init_dest, dest = None, None, None

    recursion_stack = stack()
    top_of_stack = None

    def __init__(self, x_pos, y_pos, maze_width, maze_height):
        pass
        # self.__old_x = self.__current_x =
    
    def is_moving(self):
        return self.moving

    def set_dest(self, dir):
        self.init_dest = self.dest
        self.dest = dir
        self.rolling_status, self.moving = 0, True

    def move(self):
        pass

    def set_body_color(self, R, G, B):
        pass

    def draw(self):
        pass

    def update_status(self):
        pass

    def current_x(self):
        return self.__current_x

    def current_y(self):
        return self.__current_y

    def set_getgoal(self):
        self.get_goal = True

    def lists(self):
        pass

