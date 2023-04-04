import cv2
import dlib # type: ignore
import numpy as np


class BlinkDetector:
    def __init__(self):
        # Initialize face detector and eye tracker
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        # Define constants
        self.EYE_AR_THRESH = 0.3
        self.EYE_AR_CONSEC_FRAMES = 3

    def detect_blinks(self, frame):
        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        rects = self.detector(gray, 0)

        # For each detected face, detect eyes and calculate blink rate
        blink_count = 0
        for rect in rects:
            # Extract region of interest (ROI) containing eyes
            landmarks = self.predictor(gray, rect)
            left_eye = self.extract_eye(landmarks, 36, 42)
            right_eye = self.extract_eye(landmarks, 42, 48)

            # Calculate eye aspect ratio (EAR)
            left_eye_ratio = self.eye_aspect_ratio(left_eye)
            right_eye_ratio = self.eye_aspect_ratio(right_eye)

            ear = (left_eye_ratio + right_eye_ratio) / 2.0

            # Increment blink count if eye is closed
            if ear < self.EYE_AR_THRESH:
                blink_count += 1

        # Calculate blink rate (blinks per minute)
        blink_rate = blink_count * (60.0 / self.EYE_AR_CONSEC_FRAMES)

        return blink_rate

    def extract_eye(self, landmarks, start_index, end_index):
        # Extract eye landmarks from full set of facial landmarks
        eye_landmarks = [landmarks.part(idx=i) for i in range(start_index, end_index)]

        # Convert eye landmarks to numpy array
        eye_landmarks = np.array([(p.x, p.y) for p in eye_landmarks])

        return eye_landmarks

    def eye_aspect_ratio(self, eye):
        # Calculate euclidean distance between horizontal eye landmarks
        a = np.linalg.norm(eye[1] - eye[5])
        b = np.linalg.norm(eye[2] - eye[4])

        # Calculate euclidean distance between vertical eye landmarks
        c = np.linalg.norm(eye[0] - eye[3])

        # Calculate eye aspect ratio (EAR)
        ear = (a + b) / (2.0 * c)

        return ear
