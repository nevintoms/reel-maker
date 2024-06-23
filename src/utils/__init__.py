from .save_image import save_image

import os

get_filename = lambda f: os.path.basename(f).split(".")[0]
