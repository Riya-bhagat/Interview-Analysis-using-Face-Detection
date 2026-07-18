from modules.video_processor import VideoProcessor
from modules.face_detector import FaceDetector
from modules.emotion_detector import EmotionDetector

video = VideoProcessor("uploads/interview.mp4")
frames = video.extract_frames()

face_detector = FaceDetector()
emotion_detector = EmotionDetector()

for i, frame in enumerate(frames):

    result = face_detector.detect(frame)
    if result["face_found"]:

        emotion = emotion_detector.detect(result["blendshapes"])

        print("-------------------------------")
        print("Emotion :", emotion["emotion"])
        print("Confidence :", emotion["confidence"])
        print(emotion["scores"])

    else:
        print(f"Frame {i+1}: No Face")

face_detector.close()