import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class FaceDetector:
    """
    Detects face landmarks, blendshapes and head transformation matrix.
    """

    def __init__(self):

        model_path = "model/face_landmarker.task"

        base_options = python.BaseOptions(
            model_asset_path=model_path
        )

        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces=1
        )

        self.detector = vision.FaceLandmarker.create_from_options(options)

    def detect(self, frame):

        # Convert BGR → RGB
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Convert to MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        # Detect
        result = self.detector.detect(mp_image)

        # No face detected
        if len(result.face_landmarks) == 0:
            return {
                "face_found": False,
                "landmarks": None,
                "blendshapes": None,
                "head_matrix": None
            }

        return {
            "face_found": True,
            "landmarks": result.face_landmarks[0],
            "blendshapes": result.face_blendshapes[0],
            "head_matrix": result.facial_transformation_matrixes[0]
        }

    def close(self):
        self.detector.close()