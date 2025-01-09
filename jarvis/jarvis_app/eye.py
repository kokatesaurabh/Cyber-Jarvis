import cv2
import numpy as np

# Load YOLOv4 model

def detect_objects():
    net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
    layer_names = net.getUnconnectedOutLayersNames()

    # Open a video capture object (0 is typically used for the default camera)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Normalize and preprocess image
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)

        # Run forward pass
        outs = net.forward(layer_names)

        # Get bounding boxes and confidence scores
        class_ids = []
        confidences = []
        boxes = []

        height, width, _ = frame.shape

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:  # Adjust confidence threshold as needed
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        # Draw bounding boxes on the image
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        for i in range(len(boxes)):
            if i in indices:
                x, y, w, h = boxes[i]
                label = str(class_ids[i])
                confidence = confidences[i]
                color = (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Display the resulting frame
        cv2.imshow("YOLOv8 Object Detection", frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# # Call the function to detect objects
# detect_objects()
