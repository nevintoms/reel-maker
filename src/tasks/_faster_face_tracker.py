import cv2
import face_recognition
import multiprocessing
import tempfile


def initialize_tracker(frame):
    face_locations = face_recognition.face_locations(frame)
    if face_locations:
        top, right, bottom, left = face_locations[0]
        tracker = cv2.TrackerKCF_create()
        tracker.init(frame, (left, top, right - left, bottom - top))
        return tracker, (left, top, right - left, bottom - top)
    return None, None


def process_chunk(
    start_frame, end_frame, video_path, output_path, frame_skip=1, scale=0.5
):
    cap = cv2.VideoCapture(video_path)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * scale)
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * scale)
    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    frame_count = start_frame
    ret, frame = cap.read()
    if not ret:
        print(f"Failed to read frame at position {start_frame}")
        return

    frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
    tracker, bbox = initialize_tracker(frame)
    if not tracker:
        print(
            f"Failed to detect face in the first frame of chunk starting at {start_frame}"
        )
        return

    while frame_count < end_frame:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip == 0:
            frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)
            success, bbox = tracker.update(frame)
            if success:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            out.write(frame)

        frame_count += 1

    cap.release()
    out.release()


def split_video(video_path, num_chunks):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    chunk_size = total_frames // num_chunks
    cap.release()
    return [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_chunks)]


def merge_videos(chunk_paths, output_path):
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = None

    for chunk_path in chunk_paths:
        cap = cv2.VideoCapture(chunk_path)
        if out is None:
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)
        cap.release()

    if out is not None:
        out.release()


def main(video_path, output_path, num_chunks=4, frame_skip=1, scale=0.5):
    chunks = split_video(video_path, num_chunks)
    chunk_paths = []

    with multiprocessing.Pool(processes=num_chunks) as pool:
        results = []
        for i, (start_frame, end_frame) in enumerate(chunks):
            chunk_output_path = tempfile.mktemp(suffix=".mp4")
            chunk_paths.append(chunk_output_path)
            result = pool.apply_async(
                process_chunk,
                (
                    start_frame,
                    end_frame,
                    video_path,
                    chunk_output_path,
                    frame_skip,
                    scale,
                ),
            )
            results.append(result)

        for result in results:
            result.get()

    merge_videos(chunk_paths, output_path)


if __name__ == "__main__":
    video_path = "sample-videos/sample-2-ppl-1.mp4"
    output_path = "output_video_f.mp4"
    main(video_path, output_path, num_chunks=4, frame_skip=2, scale=0.5)
