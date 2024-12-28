import sys
import cv2
import os
from ultralytics import YOLO
import logging
import time


logging.getLogger('ultralytics').setLevel(logging.CRITICAL)

# Load YOLO model
chosen_model = YOLO("yolov8n.pt", verbose=False)

def process_video(video_path, chosen_model, conf=0.3):
    # Open the video file
    video_stream = cv2.VideoCapture(video_path)

    if not video_stream.isOpened():
        print("Error: Could not open video stream", file=sys.stderr)
        sys.exit(1)

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
                              (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (0, 255, 255), 2)
                cv2.putText(frame, f"{result.names[int(box.cls[0])]}",
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 3)

        output_frames.append(frame)

    video_stream.release()

    # Create a 'processed' directory if it doesn't exist
    processed_dir = 'processed'
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    # Generate a unique filename using the current timestamp
    timestamp = int(time.time())  # Current Unix timestamp
    unique_filename = f"annotated_video_{timestamp}.mp4"
    output_video_path = os.path.join(processed_dir, unique_filename)

    # Write the annotated frames to the output video file
    # Using libx264 for H.264 video codec and AAC for audio codec
    fourcc = cv2.VideoWriter_fourcc(*'X264')  # This is usually for H.264 codec
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    for frame in output_frames:
        out.write(frame)
    out.release()

    # Return the path to the processed video
    return output_video_path

def main():
    # Read video path from argument
    video_path = sys.argv[1]

    # Process video and get the path to the annotated video
    output_video_path = process_video(video_path, chosen_model)

    # Output the path to the processed video
    print(output_video_path)

if __name__ == '__main__':
    main()
