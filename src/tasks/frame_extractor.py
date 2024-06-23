from concurrent.futures import ThreadPoolExecutor
from prefect import task
from src.utils import save_image
from src.utils.constants import (
    SAMPLE_VIDEO_FOLDER,
    get_frames_folder_path,
)

import os
import cv2


@task
def extract_frames_from_video(video_filename, frame_rate=1):
    # Create input video file path
    input_video_path = os.path.join(SAMPLE_VIDEO_FOLDER, video_filename)

    # Get frames output folder
    frames_folder = get_frames_folder_path(video_filename)

    # Open the video file
    cap = cv2.VideoCapture(input_video_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {input_video_path}")
        return

    # Get the frames per second (fps) of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"Frames per second: {fps}")

    frame_count = 0
    saved_frame_count = 0

    print(f"Starting frame extraction...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        while True:
            # Read the next frame from the video
            ret, frame = cap.read()

            # If the frame was not read successfully, break the loop
            if not ret:
                break

            # Save one frame per second
            if frame_count % (fps // frame_rate) == 0:
                frame_filename = os.path.join(
                    frames_folder, f"frame_{saved_frame_count:04d}.jpg"
                )
                executor.submit(save_image, frame, frame_filename)
                saved_frame_count += 1

            frame_count += 1
    # Release the video capture object
    cap.release()
    print("Finished extracting frames.")
