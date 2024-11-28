from typing import Dict, Union, List
from dataclasses import dataclass, field
from build123d import *

@dataclass
class TowerDimensions:
    """Dataclass to store and manage tower dimensions."""
    length: float = 25 * MM
    width: float = 25 * MM
    height: float = 75 * MM
    minicube_height: float = 25 * MM
    thickness: float = 2.5 * MM

    text_from_top_offset: float = 10.0 * MM

    # Face offsets
    front_face_offset: float = field(init=False)
    back_face_offset: float = field(init=False)
    left_face_offset: float = field(init=False)
    right_face_offset: float = field(init=False)
    
    def __post_init__(self):
        """Calculate face offsets after initialization."""
        self.front_face_offset = self.width / 2.0
        self.back_face_offset = -self.width / 2.0
        self.left_face_offset = -self.width / 2.0
        self.right_face_offset = self.width / 2.0

class TowerBuilder:
    def __init__(self, dimensions: TowerDimensions = None):
        """
        Initialize the tower builder with optional custom dimensions.
        
        Args:
            dimensions (TowerDimensions, optional): Custom tower dimensions. 
                Defaults to standard dimensions if not provided.
        """
        self.dims = dimensions or TowerDimensions()

    def create_main_part(self) -> Compound:
        """
        Create the main part of the tower by adding and subtracting components.
        
        Returns:
            Compound: The constructed tower part
        """
        # Use dictionary unpacking and list comprehension for cleaner component handling
        parts_to_add = [
            self.main_part(),
            *self._get_additive_parts()
        ]
        
        parts_to_subtract = [
            *self._get_subtractive_parts()
        ]
        
        part = Compound(parts_to_add)
        part -= Compound(parts_to_subtract)
        
        return part
    
    def main_part(self) -> Compound:
        """Create the base box for the tower."""
        return Compound(Box(
            self.dims.length, 
            self.dims.width, 
            self.dims.height, 
            align=(Align.CENTER, Align.CENTER, Align.MIN)
        ))
    
    def _get_additive_parts(self) -> List[Compound]:
        """Collect parts to be added to the main part."""
        return [
            part['add'] 
            for part in [self.right(), self.back(), self.left(), self.front()] 
            if 'add' in part
        ]

    def _get_subtractive_parts(self) -> List[Compound]:
        """Collect parts to be subtracted from the main part."""
        return [
            part['subtract'] 
            for part in [self.right(), self.back(), self.left(), self.front()] 
            if 'subtract' in part
        ]
    
    def front(self) -> Dict[str, Union[Compound, None]]:
        """Create front face components."""
        return {
            "add": Compound([self.front_top()])
        }
    
    def front_top(self) -> Compound:
        """Create text on the front top of the tower."""
        gap = 5.0
        text1 = (
            Plane.XZ.offset(self.dims.front_face_offset) * 
            Pos(0, self.dims.height - self.dims.text_from_top_offset) * 
            Text("Slant", font_size=10.0, align=(Align.CENTER, Align.MIN))
        )
        text2 = (
            Plane.XZ.offset(self.dims.front_face_offset) * 
            Pos(0, self.dims.height - self.dims.text_from_top_offset - gap) * 
            Text("3D", font_size=10.0, align=(Align.CENTER, Align.MAX))
        )
        return Compound([extrude(text1, amount=2), extrude(text2, amount=2)])
    
    def right(self):
        return {
            "subtract": Compound([self.right_top(), self.right_bottom()])
        }
    
    def right_top(self):
        """Create text on the right top of the tower."""
        gap = 5.0
        text1 = (
            Plane.YZ.offset(self.dims.right_face_offset) * 
            Pos(0, self.dims.height - self.dims.text_from_top_offset) * 
            Text("Slant", font_size=10.0, align=(Align.CENTER, Align.MIN))
        )
        text2 = (
            Plane.YZ.offset(self.dims.right_face_offset) * 
            Pos(0, self.dims.height - self.dims.text_from_top_offset - gap) * 
            Text("3D", font_size=10.0, align=(Align.CENTER, Align.MAX))
        )
        return Compound([extrude(text1, amount=-2), extrude(text2, amount=-2)])
    
    def right_bottom(self):
        """Create bottom features on the right face."""
        """
        shapes = Sketch() + [
            Plane.YZ.offset(self.dims.right_face_offset) * Pos((0, 20)) * 
                Rectangle(15, 5, align=(Align.CENTER, Align.MAX)),
            Plane.YZ.offset(self.dims.right_face_offset) * Pos((-2.5, 12)) * Circle(1), 
            Plane.YZ.offset(self.dims.right_face_offset) * Pos((-2.5, 6)) * Circle(4),
            Plane.YZ.offset(self.dims.right_face_offset) * Pos((4, 11)) * Rectangle(4, 4),
            Plane.YZ.offset(self.dims.right_face_offset) * Pos((4, 6)) * Rectangle(2, 2), 
        ]
        """
        shapes_xy = Sketch() + [
            Pos((0, 20)) * 
            Rectangle(15, 5, align=(Align.CENTER, Align.MAX)),
            Pos((-2.5, 12)) * Circle(1), 
            Pos((-2.5, 6)) * Circle(4),
            Pos((4, 11)) * Rectangle(4, 4),
            Pos((4, 6)) * Rectangle(2, 2), 
        ]
        shapes = Plane.YZ.offset(self.dims.right_face_offset) * shapes_xy
        return Compound(extrude(shapes, amount=-self.dims.thickness))
    
    def back(self):
        """Create back face components."""
        return { 
            'subtract': Compound([self.back_top(), self.back_middle()]),
            
        }
    
    def back_top(self):
        """
        Create a filleted hole on the back top of the tower.
        
        Returns:
            Compound: A filleted hole component
        """
        plane = Plane.XZ.rotated((0,0,180)).offset(self.dims.width/2.0)
        hole = (
            plane * 
            Pos(0.0, self.dims.height - 15.0*MM) * 
            Hole(radius=8, depth=self.dims.thickness)
        )
        edges = hole.edges()
        circle_edges = edges.filter_by(GeomType.CIRCLE)
        return fillet(circle_edges, radius=2.0*MM)
    
    def back_middle(self):
        plane = Plane.XZ.rotated((0,0,180)).offset(self.dims.width/2.0)
        #rect = plane * Pos(-10.0*MM,45.0*MM) * Rectangle(1.5*MM, 1.5*MM)
        rects = Sketch() + [
                loc * Rectangle(1.5*MM, 1.5*MM)
                for loc in GridLocations(2.0*MM, 2.0*MM, 9, 11)
        ]
        return extrude(plane * Pos(0,35.0*MM) * rects, amount=-2.0*MM)


    def left(self):
        """Create left face components."""
        return { 
            'subtract': Compound([self.left_top(), self.left_middle()]) 
        }
    
    def left_top(self):
        """
        Create a chamfered hole on the left top of the tower.
        
        Returns:
            Compound: A chamfered hole component
        """
        hole = (
            Plane.YZ.offset(-self.dims.width/2.0) * 
            Pos(0.0, self.dims.height - 15.0*MM) * 
            Hole(radius=8, depth=self.dims.thickness)
        )
        edges = hole.edges()
        circle_edges = edges.filter_by(GeomType.CIRCLE)
        return chamfer(circle_edges[1], length=self.dims.thickness)

    def left_middle(self):
        plane = Plane.YZ.offset(-self.dims.width/2.0)
        #rect = plane * Pos(-10.0*MM,45.0*MM) * Rectangle(1.5*MM, 1.5*MM)
        #spheres = Compound( [
        #        loc * Sphere(radius=2.5*MM)
        #        for loc in GridLocations(2.0*MM, 2.0*MM, 1, 1)
        #]
        #)
        return plane * Pos(0*MM, 35.0*MM) * Compound([
            loc * Sphere(radius=1.0*MM)
            for loc in GridLocations(2.7, 2.7, 7,9)
            #Sphere(radius=2.0*MM)
        ])
        
        #return extrude(plane * Pos(0,35.0*MM) * rects, amount=-2.0*MM)


def main():
    """Main function to create and visualize the tower."""
    tower_builder = TowerBuilder()
    part = tower_builder.create_main_part()
    try:
        from ocp_vscode import show_object
        show_object(part)
    except ImportError:
        print("VSCode OCP extension not available. Unable to show object.")

if __name__ == "__main__":
    main()