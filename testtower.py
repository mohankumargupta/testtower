from build123d import *
from ocp_vscode import *

# parameters

# tower dimensions
length = 25 * MM
width = 25 * MM
height = 75 * MM
minicube_height = 25 * MM

# grooves
groove_profile_width = 1.0 * MM
groove_depth = 2.0 * MM
first_groove_offset = 25.0 * MM
second_groove_offset = 50.0 * MM

# text
text_from_top_offset = 10.0 * MM

# origin is in the bottom center of the tower
# face offsets from origin
front_face_offset = width/2.0
back_face_offset = -width/2.0
left_face_offset = width/2.0
right_face_offset = -width/2.0

def main_part():
    return Compound(Box(length,width,height, align=(Align.CENTER, Align.CENTER, Align.MIN)))


def front_top():
    text = Plane.XZ.offset(front_face_offset) * Pos(0,height-text_from_top_offset) * Text("Slant", font_size=10.0, align=(Align.CENTER, Align.MIN))
    return extrude(text, amount=2)

def front_middle():
    pass

def front_bottom():
    pass

def front():
    return Compound([front_top()])

def back():
    pass

def right():
    pass

def left():
    pass

def top():
    pass

if __name__ == "__main__":
    part = Compound([main_part(),
                     front()
                     ])
    show_object(part)


