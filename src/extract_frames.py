import cv2
import os
import sys


def save_frames_from_video(video_path, output_folder):
    # Get the base name of the video file and remove the file extension
    video_filename = os.path.splitext(os.path.basename(video_path))[0]

    # Create output folder named after the video file
    output_folder = os.path.join(output_folder, video_filename)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video was opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Get the frames per second (fps) of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(f"Frames per second: {fps}")

    frame_count = 0
    saved_frame_count = 0

    while True:
        # Read the next frame from the video
        ret, frame = cap.read()

        # If the frame was not read successfully, break the loop
        if not ret:
            break

        # Save one frame per second
        if frame_count % fps == 0:
            frame_filename = os.path.join(
                output_folder, f"frame_{saved_frame_count:04d}.jpg"
            )
            cv2.imwrite(frame_filename, frame)
            print(f"Saved frame {saved_frame_count:04d}")
            saved_frame_count += 1

        frame_count += 1

    # Release the video capture object
    cap.release()
    print("Finished extracting frames.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_frames.py <video_path> <output_folder>")
    else:
        video_path = sys.argv[1]
        output_folder = sys.argv[2]
        save_frames_from_video(video_path, output_folder)
