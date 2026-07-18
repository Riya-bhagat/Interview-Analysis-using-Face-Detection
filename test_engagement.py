from modules.video_processor import VideoProcessor
from modules.face_detector import FaceDetector
from modules.engagement import EngagementAnalyzer


video = VideoProcessor(
    "uploads/interview.mp4"
)


frames = video.extract_frames()


face_detector = FaceDetector()

engagement = EngagementAnalyzer()



for frame in frames:

    result = face_detector.detect(frame)

    engagement.process_frame(result)



report = engagement.get_report()


print(report)


face_detector.close()
