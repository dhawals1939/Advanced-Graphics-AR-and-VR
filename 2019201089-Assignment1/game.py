from Cell import Cell

width, height = -1, -1

while width not in range(0, 10) and height not in range(0, 10):
    width, height = int(input('Width?')), int(input('Height?'))

time_factor, zoom_factor = 20, 20
view_change_x, view_change_y = 0, 0

cell = [Cell()]*(width * height)

