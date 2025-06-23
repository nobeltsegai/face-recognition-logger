import os
import face_recognition
from PIL import Image
import numpy as np
import cv2
#from pathlib import Path 
#   [to be used when working with multiple folder of faces, pick and choose case]

class FaceRecognition: 
    #taken in path to folder associeted to the faces to compare to
    def __init__(self, known_face_list: str) -> None: 
        # 3 components, encoding, names, and loading known faces
        self.known_encoding = []
        self.known_names = []
        self._load_known_faces(known_face_list)

    
    def _load_known_faces(self, dir: str) -> None:    
        accepted_types = (".png", ".jpeg", ".jpg") #can expand later, strict check for now 
        
        for filename in os.listdir(dir): 
            if filename.lower().endswith(accepted_types): 
                file_path = os.path.join(dir, filename)
                image = face_recognition.load_image_file(file_path)
                
                # Convert image to RGB to avoid issues with transparency or palette
                try:
                    with Image.open(file_path) as img:
                        rgb_image = img.convert("RGB")
                        # Save to a temporary NumPy array for face_recognition
                        image_np = np.array(rgb_image)
                except Exception as e:
                    print(f"[WARN] Could not open {file_path}: {e}")
                    continue

                print(f"Image shape: {image_np.shape}, dtype: {image_np.dtype}")
                locations = face_recognition.face_locations(image_np)
                image_encodings = face_recognition.face_encodings(image_np, locations)


                if image_encodings: 
                    self.known_encoding.append(image_encodings[0])
                    file_name = os.path.splitext(filename)[0]
                    self.known_names.append(file_name)
                else: 
                    print([f"[INFO] No face found in {file_path}"])

    # # returns list with a tuples of name and pixel coordinate of the face
    def recognition_of_faces(self, frame) -> list[tuple[str, tuple[int, int, int, int]]]: 
        
        
        rgb_frame = frame[:, :, ::-1]
        print(f"[DEBUG] rgb_frame shape: {rgb_frame.shape}, dtype: {rgb_frame.dtype}")
        
        
        
        try: #make sure encoding goes through
            locations = face_recognition.face_locations(rgb_frame)
            if not locations:
                return []
            
            print(f"[DEBUG] Face locations: {locations}")
            #encodings = face_recognition.face_encodings(rgb_frame, locations)
            small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
            locations = face_recognition.face_locations(small_frame)
            encodings = face_recognition.face_encodings(small_frame, locations)

            scaled_locations = [(top*4, right*4, bottom*4, left*4) for top, right, bottom, left in locations]
            #shrink and unshrink for speed 

        except Exception as e:
            print(f"[ERROR] Face encoding failed: {e}")
            return []

        result = [] #can be multiple faces

        #given there is a face in frame, match to a known face and label their name were the face is
        #unknown if its unfamiliar face 
        for encoding, location in zip(encodings, scaled_locations): 
            matches = face_recognition.compare_faces(self.known_encoding, encoding)
            name = "unfamiliar"
            
            if True in matches: 
                match_index = matches.index(True)
                name = self.known_names[match_index]
            
            result.append((name, location))
        return result 


# def recognition_of_faces(self, frame):
#     # Convert BGR (OpenCV) to RGB (face_recognition expects RGB)
#     rgb_frame = frame[:, :, ::-1]

#     # Resize for faster processing
#     small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)

#     # Detect faces in the resized frame
#     small_locations = face_recognition.face_locations(small_frame, model="hog")

#     # Scale locations back to original frame size
#     face_locations = []
#     for top, right, bottom, left in small_locations:
#         face_locations.append((top * 4, right * 4, bottom * 4, left * 4))

#     # (Optional) Use these locations to encode and identify faces
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#     names = []
#     for face_encoding in face_encodings:
#         # Add your logic here to compare against known encodings
#         name = self.identify_face(face_encoding)  # assuming you have this
#         names.append(name)

#     return zip(names, face_locations)
