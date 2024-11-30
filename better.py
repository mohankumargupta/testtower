from build123d import *
from ocp_vscode import show

length = 25
width = 25
height = 75
thickness = 2.5

xz_offset = width/2.0
first_groove = height / 3.0
second_groove = 2 * first_groove

# Create base tower
part = Box(length, width, height, align=(Align.CENTER, Align.CENTER, Align.MIN))

# front 

# front top
text1 = (Plane.XZ.offset(xz_offset) * 
         Pos(0,second_groove) *
         Pos(0, 15) * 
         Text("Slant", font_size=10, align=(Align.CENTER, Align.CENTER))
)
part -= extrude(text1, amount=-thickness)

text2 = (Plane.XZ.offset(xz_offset) * 
         Pos(0, second_groove) *
         Pos(0, 5) * 
         Text("3D", font_size=10, align=(Align.CENTER, Align.CENTER))
)
part -= extrude(text2, amount=-thickness)










show(part)
