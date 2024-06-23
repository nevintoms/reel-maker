import os
from src.utils import get_filename

OUTPUT_FOLDER = "outputs"
SAMPLE_VIDEO_FOLDER = "sample-videos"
EXTRACTED_FRAMES_FOLDER = "extracted-frames"
FACE_DETECTED_FOLDER = "face-detected"

get_frames_folder_path = lambda f: os.path.join(
    OUTPUT_FOLDER, get_filename(f), EXTRACTED_FRAMES_FOLDER
)
get_face_detected_path = lambda f: os.path.join(
    OUTPUT_FOLDER, get_filename(f), FACE_DETECTED_FOLDER
)
