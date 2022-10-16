RED = (255, 0, 0)
GREEN = (144, 229, 150)
BLUE = (158, 219, 227)
YELLOW = (255, 255, 0)  # meaning?
WHITE = (255, 255, 255)
BLACK = (56, 55, 56)
PURPLE = (175, 117, 173)
ORANGE = (234, 194, 84)
GREY = (126, 126, 121)
TURQUOISE = (47, 66, 206)


def new_color(base_color=WHITE, target_color=ORANGE, ratio=0):
    new_color = []
    for i in range(3):
        calculation = float(target_color[i] - base_color[i]) * ratio + float(base_color[i])
        new_color.append(int(calculation))
    return new_color

print(new_color(ratio=0.5))