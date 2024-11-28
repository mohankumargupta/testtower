from build123d import *
from testtower import TowerBuilder

tower_builder = TowerBuilder()
part = tower_builder.create_main_part()

export_step(part, file_path="testtower.step")
export_stl(part, file_path="testtower.stl")