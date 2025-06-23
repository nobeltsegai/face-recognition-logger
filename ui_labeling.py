import cv2

class UILabeler:
    def frame_face(face, frame, faces: list[tuple[str, tuple[int, int, int, int]]]) -> None: 
        for name, (top, right, bottom, left) in faces: 
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame,
                        name, 
                        (left, top - 10), 
                        cv2.FONT_HERSHEY_COMPLEX, 
                        0.5, 
                        (0, 255, 0), 
                        2
                ) 

    def show_frame(self, frame) -> None:
        cv2.imshow("Webcam", frame)

    def wait_for_quit(self) -> bool:
        return cv2.waitKey(1) & 0xFF == ord("q")

    def close(self) -> None:
        cv2.destroyAllWindows()