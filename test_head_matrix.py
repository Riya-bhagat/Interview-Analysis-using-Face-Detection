from modules.video_processor import VideoProcessor
from modules.face_detector import FaceDetector

video = VideoProcessor("uploads/interview.mp4")
frames = video.extract_frames()

detector = FaceDetector()

for i, frame in enumerate(frames):

    result = detector.detect(frame)

    if result["face_found"]:

        print("\nFrame:", i + 1)

        print("Head Matrix:")

        for row in result["head_matrix"]:
            print(row)

        break

detector.close()