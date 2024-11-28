from build123d import *
from testtower import create_main_part


part = create_main_part()
export_step(part, file_path="testtower.step")
export_stl(part, file_path="testtower.stl")