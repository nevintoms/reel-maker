# reel-maker
This project helps to generate a reel out of small videos of the selected face/character and combine all the frames in which  the person is present into a reel.

## Overview

This project provides a pipeline to process video frames, detect faces, and track one specific face throughout the video. The pipeline is built using Python, Prefect, OpenCV, and face_recognition libraries, and is containerized using Docker and orchestrated with Docker Compose.

## Features
* Extract frames from video at a rate of 1 frame per second.
* Detect faces in the extracted frames.
* Track a specific face throughout the video.
* Save processed frames and a video.
* Containerized using Docker and orchestrated with Docker Compose.

## Getting Started
### Prerequisites
* Docker
* Docker Compose

There are 2 services in the `docker-compose.yaml` namely `prefect` and `reel-maker`. The `prefect` container runs the prefect UI application on port `4200` which is exposed to the `4200` for your system. You can access this UI on http://localhost:4200.

The `reel-maker` container is the worker container which runs the code to extract the frames and then detect faces on the extracted frames. This container is to be run only once the `prefect` contaienr is running.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/face-recognition-pipeline.git
    cd face-recognition-pipeline
   ```
2. Build the Docker images:
Open your terminal in the root directory which containing the `Dockerfile`, `requirements.txt` and then run:
    ```
    docker compose build .
    ```

1. Run the services:
Assuming you have sample vidoes `sample-2-ppl-1.mp4` in the `sample-videos` directory, you can run the containers:

    ```
    docker compose up
    ```

## Configuration
* Video Input: Place your videos in the `sample-videos` directory.
* Output: Processed frames and video will be saved in the `outputs` directory.

## File Descriptions
* Dockerfile: Dockerfile to build the image for the face recognition service.
* docker-compose.yaml: Docker Compose file to orchestrate the services.
* src/flows/main.py: Main script to run the pipeline.
* src/tasks/: Directory containing tasks for frame extraction, face detection, and face tracking.
* src/utils/: Utility functions for saving images and defining constants.


## Acknowledgements
* [OpenCV](https://opencv.org/)
* [face_recognition](https://github.com/ageitgey/face_recognition)
* [Prefect](https://www.prefect.io/)
