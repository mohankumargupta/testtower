from build123d import *
from ocp_vscode import *

# parameters

# tower dimensions
length = 25 * MM
width = 25 * MM
height = 75 * MM
minicube_height = 25 * MM
thickness = 2.5 * MM

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
left_face_offset = -width/2.0
right_face_offset = width/2.0

def main_part():
    return Compound(Box(length,width,height, align=(Align.CENTER, Align.CENTER, Align.MIN)))


def front_top():
    gap = 5.0
    text1 = Plane.XZ.offset(front_face_offset) * Pos(0,height-text_from_top_offset) * Text("Slant", font_size=10.0, align=(Align.CENTER, Align.MIN))
    text2 = Plane.XZ.offset(front_face_offset) * Pos(0,height-text_from_top_offset-gap) * Text("3D", font_size=10.0, align=(Align.CENTER, Align.MAX))
    return Compound([extrude(text1, amount=2), extrude(text2, amount=2)])

def front_middle():
    pass

def front_bottom():
    pass

def front():
    return  {
        "add": Compound([front_top()])
    }
    
def back():
    return { 'subtract': Compound([back_top()])}

def back_top():
    """
    filleted hole
    """
    #hole = Plane.XZ.rotated((0,0,180)).offset(width/2.0) * Pos(0.0,0.0) * Cylinder(radius=15, height=3, align=(Align.CENTER, Align.MIN, Align.MAX))
    hole = Plane.XZ.rotated((0,0,180)).offset(width/2.0) * Pos(0.0,height - 15.0*MM) * Hole(radius=8, depth=thickness)
    edges = hole.edges()
    print(len(edges))
    return hole

def right():
    return {
        "subtract": Compound([right_top(), right_bottom()])
    }

def right_top():
    gap = 5.0
    text1 = Plane.YZ.offset(right_face_offset) * Pos(0,height-text_from_top_offset) * Text("Slant", font_size=10.0, align=(Align.CENTER, Align.MIN))
    text2 = Plane.YZ.offset(right_face_offset) * Pos(0,height-text_from_top_offset-gap) * Text("3D", font_size=10.0, align=(Align.CENTER, Align.MAX))
    return Compound([extrude(text1, amount=-2), extrude(text2, amount=2)])

def right_bottom():
    shapes = Sketch() + [
        Plane.YZ.offset(right_face_offset) * Pos((0,20)) * Rectangle(15, 5, align=(Align.CENTER, Align.MAX)),
        Plane.YZ.offset(right_face_offset) * Pos((-2.5, 12)) * Circle(1), 
        Plane.YZ.offset(right_face_offset) * Pos((-2.5, 6)) * Circle(4),
        Plane.YZ.offset(right_face_offset) * Pos((4, 11)) * Rectangle(4,4),
        Plane.YZ.offset(right_face_offset) * Pos((4, 6)) * Rectangle(2,2), 
    ]
    return Compound(extrude(shapes, amount=-thickness))


def left():
    pass

def top():
    pass

if __name__ == "__main__":
    front_part = front()
    right_part = right()
    back_part = back()


    part = Compound([main_part(),
                     front_part['add'],

                     ])
    part -= Compound([right_part['subtract'], back_part['subtract']])
    #part -= right_bottom()
    show_object(part)


