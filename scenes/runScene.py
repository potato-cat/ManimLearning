import sys

sys.path.append(r'C:\Users\potat\Documents\manim')
from manim.utils.module_ops import scene_classes_from_file
from pathlib import Path
from manim import config
from scenes.BinarySearchTableScene import BinarySearchTableScene as Scene
# from widgets.circuit.mosfet import TestScene as Scene

config.digest_file('./manim.cfg')
# config.disable_caching = True

Scene().render(True)