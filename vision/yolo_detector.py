from ultralytics import YOLO

class YoloDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        return self.model(frame, verbose=False)

    def detect_objects(self, frame):
        results = self.detect(frame)
        detections = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            cls = int(box.cls)
            conf = float(box.conf)
            detections.append((cls, conf, (x1, y1, x2, y2)))
        return detections

    def has_obstacle(self, frame):
        results = self.detect_objects(frame)
        for cls, conf, box in results:
            if cls != 0:
                return True
        return False
