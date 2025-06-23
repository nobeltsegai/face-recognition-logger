from face_recognition_mod import FaceRecognition
from ui_labeling import UILabeler
from camera_manager import CameraManager
from attendance_track import AttendanceTracker
import os


def main(): 
    face_recognitions = FaceRecognition(os.path.join(os.path.dirname(__file__), "familiar_faces"))
    attendance = AttendanceTracker()
    ui_label = UILabeler()
    camera = CameraManager()

    while True: 
        frame = camera.get_frame()
        if frame is None: 
            break 

        faces = face_recognitions.recognition_of_faces(frame)
        
        for name, location in faces: 
            attendance.mark_attendance(name)
        ui_label.frame_face(frame, faces)
        ui_label.show_frame(frame)

        if ui_label.wait_for_quit():
            break

    attendance.save_attendance()
    camera.release()
    ui_label.close()

if __name__ == "__main__": #only run in main, no auto-compile in testing 
    main()