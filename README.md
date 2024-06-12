# reel-maker
This project helps to generate a reel out of small videos of the selected face/character and combine all the frames in which  the person is present into a reel.

## Building and Running the Docker Container

1. Build the Docker image:
Open your terminal in the directory containing the Dockerfile, requirements.txt, and extract_frames.py, then run:
```
docker build -t reel-maker .
```

2. Run the Docker container:
Assuming you have an input_video.mp4 in the current directory, you can run the container like this:

```
docker run -it -v $(pwd):/app reel-maker python src/extract_frames.py sample-videos/sample-2-ppl-1.mp4 extracted_frames
```
