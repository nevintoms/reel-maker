from prefect import task, get_run_logger
from src.utils.constants import (
    BASE_OUTPUT_FOLDER,
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
    logger = get_run_logger()
    # Get only the filename without extension
    filename = get_filename(input_filename)

    # Create main output folder
    output_folder = os.path.join(".", BASE_OUTPUT_FOLDER, filename)
    create_folder(output_folder)
    logger.info(f"Created output folder: {output_folder}")

    # folder for extracted frames
    frames_folder = get_frames_folder_path(filename)
    create_folder(frames_folder)
    logger.info(f"Created frames folder: {frames_folder}")

    # folder for detected faces
    face_detected_folder = get_face_detected_path(filename)
    create_folder(face_detected_folder)
    logger.info(f"Created detection folder: {face_detected_folder}")
