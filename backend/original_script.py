import sys
import cv2
from ultralytics import YOLO  # YOLOv8 library for object detection
import base64
import numpy as np
import os
import logging


logging.getLogger('ultralytics').setLevel(logging.CRITICAL)
# Load the YOLO model
chosen_model = YOLO("yolov8n.pt", verbose=False)  # Load the YOLO model

def predict(chosen_model, img, classes=[], conf=0.3):
    """Predict bounding boxes and classes."""
    if classes:
        results = chosen_model.predict(img, classes=classes, conf=conf)
    else:
        results = chosen_model.predict(img, conf=conf)
    return results

def predict_and_detect(chosen_model, img, classes=[], conf=0.3, rectangle_thickness=2, fontScale=3, text_thickness=2):
    """Run predictions and annotate the image with bounding boxes and labels."""
    results = predict(chosen_model, img, classes, conf=conf)
    for result in results:
        for box in result.boxes:
            # Draw the bounding box
            cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)

            # Put the label text
            cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN, fontScale, (255, 0, 0), text_thickness)
    return img, results

def image_to_base64(image):
    """Convert image to base64 string."""
    _, buffer = cv2.imencode('.jpg', image)  # Convert image to JPG format
    image_bytes = buffer.tobytes()  # Convert the buffer to bytes
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')  # Encode the image bytes to base64 string
    return image_base64

def main():
    # Get the file path from the argument
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: File not found at {image_path}", file=sys.stderr)
        sys.exit(1)
    
    img = cv2.imread(image_path)  # Read the image from the file path
    
    if img is None:
        print("Error: Could not decode the image", file=sys.stderr)
        sys.exit(1)

    # Perform detection
    annotated_img, results = predict_and_detect(chosen_model, img)

    # Convert annotated image to base64
    image_base64 = image_to_base64(annotated_img)

    # Output the base64 image string
    print(image_base64)

if __name__ == '__main__':
    main()
