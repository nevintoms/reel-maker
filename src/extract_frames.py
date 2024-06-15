from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from prefect import flow, task

import cv2
import os
import sys
import face_recognition


SAMPLE_VIDEO_BASE_PATH = "sample-videos"
EXTRACTED_FRAMES_BASE_PATH = "extracted-frames"
FACE_DETECTED_BASE_PATH = "face-detected"


def save_image(img, file_path):
    cv2.imwrite(file_path, img)
    print(f"Saved frame {os.path.basename(file_path)}")


def create_output_folder(BASE_PATH, folder_name):
    # Get the basename if folder_name is a file path
    base_folder_name = os.path.basename(folder_name)

    # Create output folder in the base folder
    output_folder = os.path.join(BASE_PATH, base_folder_name)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    return output_folder


@task
def extract_frames_from_video(video_filename, frame_rate=1):
    # Create input video file path
    input_video_path = os.path.join(SAMPLE_VIDEO_BASE_PATH, video_filename)

    # Create output folder
    output_folder = create_output_folder(EXTRACTED_FRAMES_BASE_PATH, video_filename)

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
                    output_folder, f"frame_{saved_frame_count:04d}.jpg"
                )
                executor.submit(save_image, frame, frame_filename)
                saved_frame_count += 1

            frame_count += 1
    # Release the video capture object
    cap.release()
    print("Finished extracting frames.")


def process_frame(frame_file, known_face_encodings, known_face_names, output_folder):
    frame = face_recognition.load_image_file(frame_file)
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Convert the image to a format that OpenCV can work with
    frame_cv2 = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    for (top, right, bottom, left), face_encoding in zip(
        face_locations, face_encodings
    ):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
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


@task
def detect_and_recognize_faces(video_filename):
    known_face_encodings = []
    known_face_names = []
    # Create frames folder path
    frames_folder = os.path.join(EXTRACTED_FRAMES_BASE_PATH, video_filename)

    # Create output folder
    output_folder = create_output_folder(FACE_DETECTED_BASE_PATH, video_filename)

    frame_files = [
        os.path.join(frames_folder, f)
        for f in os.listdir(frames_folder)
        if f.endswith(".jpg")
    ]

    print(f"Starting face detection...")
    # ProcessPoolExecutor is added since face encoding and face location detection
    # are extremely CPU-intensive. It can split the work across multiple CPU cores.
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                process_frame,
                frame_file,
                known_face_encodings,
                known_face_names,
                output_folder,
            )
            for frame_file in frame_files
        ]

        # Ensure all threads have completed
        for future in futures:
            future.result()

    print(f"Finished detecting faces.")
    return known_face_names


@flow
def main():
    input_filename = sys.argv[1]
    extract_frames_from_video(input_filename)
    distinct_faces = detect_and_recognize_faces(os.path.join(input_filename))
    print(f"Detected {len(distinct_faces)} distinct faces: {distinct_faces}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_frames.py <input_video_filename>")
        exit(1)
    main()
