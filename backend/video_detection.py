import sys
import cv2
import base64
import tempfile
from ultralytics import YOLO
import os
import logging

logging.getLogger('ultralytics').setLevel(logging.CRITICAL)

# Load YOLO model
chosen_model = YOLO("yolov8s.pt", verbose=False)

def process_video(video_data, chosen_model, conf=0.3):
    # Create a temporary file to hold the video data in memory
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    try:
        # Write video data to the temporary file
        temp_video.write(video_data)
        temp_video.flush()
        temp_video.close()

        # Open the temporary video file
        video_stream = cv2.VideoCapture(temp_video.name)

        if not video_stream.isOpened():
            print("Error: Could not open video stream", file=sys.stderr)
            return None

        # Prepare output video
        frame_width = int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(video_stream.get(cv2.CAP_PROP_FPS))
        output_frames = []

        while True:
            ret, frame = video_stream.read()
            if not ret:
                break

            # Perform object detection
            results = chosen_model.predict(frame, conf=conf)

            # Annotate frame
            for result in results:
                for box in result.boxes:
                    cv2.rectangle(frame, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                                     (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), 2)
                    cv2.putText(frame, f"{result.names[int(box.cls[0])]}",
                                   (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            output_frames.append(frame)

        video_stream.release()

        # Write annotated frames to a temporary output file
        temp_output_path = tempfile.mktemp(suffix='.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_output_path, fourcc, fps, (frame_width, frame_height))

        for frame in output_frames:
            out.write(frame)
        out.release()

        # Read the annotated video and convert to base64
        with open(temp_output_path, "rb") as f:
            base64_video = base64.b64encode(f.read()).decode("utf-8")

        # Clean up the temporary file
        os.remove(temp_output_path)

    finally:
        os.remove(temp_video.name)

    return base64_video

def main():
    # Read the video data from stdin
    video_data = sys.stdin.buffer.read()

    # Process video and get the base64-encoded video
    base64_video = process_video(video_data, chosen_model)

    if base64_video:
        print(base64_video)
    else:
        print("Error: Failed to process the video.")

if __name__ == '__main__':
    main()
