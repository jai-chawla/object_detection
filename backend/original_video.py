import sys
import cv2
import base64
from ultralytics import YOLO
import os

# Suppress YOLO library logs
import logging
logging.getLogger('ultralytics').setLevel(logging.CRITICAL)

# Load YOLO model
chosen_model = YOLO("yolov8s.pt", verbose=False)

def process_video(video_path, chosen_model, conf=0.3):
    """
    Process the video file, perform object detection, annotate the frames, and return the annotated video as base64.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}", file=sys.stderr)
        sys.exit(1)

    # Open the video file
    video_stream = cv2.VideoCapture(video_path)

    if not video_stream.isOpened():
        print("Error: Could not open video stream", file=sys.stderr)
        sys.exit(1)

    # Prepare output video
    frame_width = int(video_stream.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video_stream.get(cv2.CAP_PROP_FPS))
    temp_output_path = "annotated_output.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (frame_width, frame_height))

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

        out.write(frame)

    video_stream.release()
    out.release()

    # Convert annotated video to base64
    with open(temp_output_path, "rb") as f:
        base64_video = base64.b64encode(f.read()).decode("utf-8")

    # Clean up temporary output file
    os.remove(temp_output_path)

    return base64_video

def main():
    if len(sys.argv) != 2:
        print("Usage: python video_detection.py <video_path>", file=sys.stderr)
        sys.exit(1)

    video_path = sys.argv[1]

    # Process video and get the base64-encoded video
    base64_video = process_video(video_path, chosen_model)

    # Output the base64 string
    print(base64_video)

if __name__ == '__main__':
    main()
