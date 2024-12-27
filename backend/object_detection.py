import sys
import cv2
from ultralytics import YOLO  # YOLOv8 library for object detection
import os
import base64
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("Python script triggered")

# Load your object detection model
# MODEL_PATH = "C:\\Users\\JAI CHAWLA\\Downloads\\best.pt"  # Replace with the correct path to your YOLO model

try:
    logging.info("Loading YOLO model...")
    chosen_model = YOLO("yolov8n.pt", verbose=False)  # Load the YOLO model
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading YOLO model: {e}")
    sys.exit(1)

def predict(chosen_model, img, classes=[], conf=0.3):
    """Predict bounding boxes and classes."""
    try:
        if classes:
            results = chosen_model.predict(img, classes=classes, conf=conf)
        else:
            results = chosen_model.predict(img, conf=conf)
        logging.info("Prediction completed successfully.")
        return results
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return None

def predict_and_detect(chosen_model, img, classes=[], conf=0.3, rectangle_thickness=2, fontScale=2, text_thickness=3):
    """Run predictions and annotate the image with bounding boxes and labels."""
    results = predict(chosen_model, img, classes, conf=conf)
    if not results:
        logging.error("No results returned from prediction.")
        return img, None
    
    for result in results:
        for box in result.boxes:
            try:
                # Draw the bounding box
                cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                              (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)

                # Put the label text
                label = result.names.get(int(box.cls[0]), "Unknown")
                confidence = box.conf[0] if hasattr(box, 'conf') else "N/A"
                cv2.putText(img, f"{label} ({confidence:.2f})",
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_PLAIN, fontScale, (255, 0, 0), text_thickness)
            except Exception as e:
                logging.warning(f"Error annotating box: {e}")
    return img, results

def image_to_base64(image):
    """Convert image to base64 string."""
    try:
        _, buffer = cv2.imencode('.jpg', image)  # Convert image to JPG format
        image_bytes = buffer.tobytes()  # Convert the buffer to bytes
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')  # Encode the image bytes to base64 string
        logging.info("Image successfully converted to base64.")
        return image_base64
    except Exception as e:
        logging.error(f"Error converting image to base64: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        logging.error("Usage: python object_detection.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        logging.error(f"Image path does not exist: {image_path}")
        sys.exit(1)

    # Load the image
    img = cv2.imread(image_path)
    if img is None or img.size == 0:
        logging.error(f"Error: The image at {image_path} could not be loaded or is empty.")
        sys.exit(1)

    logging.info(f"Image loaded successfully: {image_path}")

    # Perform detection
    annotated_img, results = predict_and_detect(chosen_model, img)
    if results is None:
        logging.warning("No detections made.")
    else:
        logging.info(f"Number of detections: {len(results)}")

    # Convert annotated image to base64
    image_base64 = image_to_base64(annotated_img)
    if image_base64:
        logging.info("Annotated image ready to be sent as base64.")

if __name__ == '__main__':
    main()
