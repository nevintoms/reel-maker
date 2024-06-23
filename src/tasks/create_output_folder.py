from prefect import task
from src.utils.constants import (
    OUTPUT_FOLDER,
    get_frames_folder_path,
    get_face_detected_path,
)
from src.utils import get_filename


import os


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    return folder_path


@task
def create_intermediate_output_folders(input_filename):
    # Get only the filename without extension
    filename = get_filename(input_filename)

    # Create main output folder
    create_folder(os.path.join(".", OUTPUT_FOLDER, filename))

    # folder for extracted frames
    frames_folder = get_frames_folder_path(filename)
    create_folder(frames_folder)

    # folder for detected faces
    face_detected_folder = get_face_detected_path(filename)
    create_folder(face_detected_folder)
