import cv2
import face_recognition


def initialize_tracker(frame):
    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        top, right, bottom, left = face_locations[0]  # Take the first detected face
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, (left, top, right - left, bottom - top))
        return tracker, (left, top, right - left, bottom - top)
    return None, None


def track_face(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        return

    tracker, bbox = initialize_tracker(frame)
    if not tracker:
        print("Failed to detect face in the first frame")
        return

    # Get the width and height of the video frames
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize the VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # You can use other codecs like 'XVID'
    out = cv2.VideoWriter(
        output_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (frame_width, frame_height)
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Update the tracker
        success, bbox = tracker.update(frame)
        if success:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

        # Write the frame with the bounding box to the output video
        out.write(frame)

    cap.release()
    out.release()


if __name__ == "__main__":
    video_path = "sample-videos/sample-2-ppl-1.mp4"
    output_path = "output_video.mp4"
    track_face(video_path, output_path)
