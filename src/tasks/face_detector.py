from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context
from src.utils.constants import (
    get_frames_folder_path,
    get_face_detected_path,
)
from src.utils import save_image
from prefect import task

import os
import cv2
import face_recognition
import multiprocessing as mp


def process_frame(frame_file, known_face_encodings, known_face_names, output_folder):
    try:
        frame = face_recognition.load_image_file(frame_file)
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Convert the image to a format that OpenCV can work with
        frame_cv2 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        for (top, right, bottom, left), face_encoding in zip(
            face_locations, face_encodings
        ):
            matches = face_recognition.compare_faces(
                known_face_encodings, face_encoding
            )
            if not any(matches):
                known_face_encodings.append(face_encoding)
                known_face_names.append(f"person_{len(known_face_names)}")

                # Crop the face
                face_image = frame_cv2[top:bottom, left:right]

                # Save the image with rectangles
                result_filename = os.path.join(
                    output_folder, f"detected_{os.path.basename(frame_file)}"
                )
                save_image(face_image, result_filename)

                # Draw a rectangle around the face
                # cv2.rectangle(frame_cv2, (left, top), (right, bottom), (0, 255, 0), 2)
    except Exception as e:
        print(f"Error processing {frame_file}: {e}")


@task
def detect_and_recognize_faces(video_filename):
    known_face_encodings = []
    known_face_names = []
    frames_folder = get_frames_folder_path(video_filename)
    face_detected_folder = get_face_detected_path(video_filename)

    frame_files = [
        os.path.join(frames_folder, f)
        for f in os.listdir(frames_folder)
        if f.endswith(".jpg")
    ]

    # Using the `spawn`` start method for creating new processes can help
    # avoid issues related to resource sharing and potential deadlocks
    # that can occur with the default `fork`` method.
    ctx = mp.get_context("spawn")

    print(f"Starting face detection...")
    # ProcessPoolExecutor is added since face encoding and face location detection
    # are extremely CPU-intensive. It can split the work across multiple CPU cores.
    with ProcessPoolExecutor(max_workers=4, mp_context=ctx) as executor:
        futures = [
            executor.submit(
                process_frame,
                frame_file,
                known_face_encodings,
                known_face_names,
                face_detected_folder,
            )
            for frame_file in frame_files
        ]

        # Ensure all process have completed
        for future in futures:
            future.result()

    print(f"Finished detecting faces.")
    return known_face_names
