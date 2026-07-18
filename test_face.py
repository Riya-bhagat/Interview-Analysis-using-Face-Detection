from modules.video_processor import VideoProcessor
from modules.face_detector import FaceDetector

video = VideoProcessor("uploads/interview.mp4")
frames = video.extract_frames()

detector = FaceDetector()

for i, frame in enumerate(frames):

    result = detector.detect(frame)

    print("\n----------------------")
    print("Frame:", i + 1)
    print("Face Found:", result["face_found"])

    if result["face_found"]:
        print("Landmarks :", len(result["landmarks"]))
        print("Blendshapes :", len(result["blendshapes"]))
        print("Head Matrix Shape :", result["head_matrix"].shape)

        break

detector.close()