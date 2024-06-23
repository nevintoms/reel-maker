from prefect import flow
from src.tasks import (
    create_intermediate_output_folders,
    detect_and_recognize_faces,
    extract_frames_from_video,
)

import sys


@flow
def main():
    input_filename = "sample-2-ppl-1.mp4"
    # input_filename = sys.argv[1]
    # Step 1: Create intermediate output folders for `input_filename`.
    create_intermediate_output_folders(input_filename)
    # Step 2: Extract 1 frame per sec from input video.
    extract_frames_from_video(input_filename)
    # Step 3: Detect faces from each extracted frame and save them.
    distinct_faces = detect_and_recognize_faces(input_filename)
    # Output detected faces
    print(f"Detected {len(distinct_faces)} distinct faces: {distinct_faces}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_frames.py <input_video_filename>")
        exit(1)
    main()
