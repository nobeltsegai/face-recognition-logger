import cv2

class CameraManager:
    def __init__(self, camera_index: int = 0) -> None:
        self.capture = cv2.VideoCapture(camera_index)

    def get_frame(self):
        ret, frame = self.capture.read()
        return frame if ret else None

    def release(self) -> None:
        self.capture.release()