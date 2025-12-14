from camera_stream import CameraStream
from yolo_detector import YoloDetector
from object_tracker import ObjectTracker
from manipulator_controller import ManipulatorController
from diff_drive import DiffDrive
from navigation_core import NavigationCore

class RobotBrain:
    def __init__(self):
        self.camera = CameraStream()
        self.detector = YoloDetector()
        self.tracker = ObjectTracker()
        self.arm = ManipulatorController()
        self.drive = DiffDrive()
        self.nav = NavigationCore()

    def step(self):
        frame = self.camera.read()
        if frame is None:
            return

        detections = self.detector.detect_objects(frame)
        tracks = self.tracker.update(detections)

        if self.detector.has_obstacle(frame):
            self.drive.stop()
            self.arm.remove_obstacle()
        else:
            self.drive.forward(0.5)

        target = self.nav.update()
        return tracks, target
