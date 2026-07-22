import threading
import time

import av
import cv2

from modules.emotion_detector import EmotionDetector
from modules.engagement import EngagementAnalyzer
from modules.face_detector import FaceDetector
from modules.report_generator import ReportGenerator


class LiveProcessor:
    """
    Processes browser webcam frames during a live interview session.
    """

    def __init__(self):

        self.face_detector = FaceDetector()
        self.emotion_detector = EmotionDetector()
        self.engagement = EngagementAnalyzer()
        self.report = ReportGenerator()

        self.lock = threading.Lock()

        self.start_time = time.time()
        self.last_analysis_time = 0
        self.latest_emotion = "Waiting"
        self.latest_confidence = 0
        self.face_found = False


    def recv(self, frame):
        """
        Called automatically for every webcam video frame.
        """

        image = frame.to_ndarray(format="bgr24")

        current_time = time.time()

        if current_time - self.last_analysis_time >= 1:

            self.last_analysis_time = current_time

            result = self.face_detector.detect(image)

            emotion_name = "No Face"
            confidence = 0

            self.engagement.process_frame(result)

            if result["face_found"]:

                emotion = self.emotion_detector.detect(
                    result["blendshapes"]
                )

                self.report.add_emotion(
                    emotion["emotion"]
                )

                emotion_name = emotion["emotion"]
                confidence = emotion["confidence"]

            engagement_report = self.engagement.get_report()

            with self.lock:
                self.face_found = result["face_found"]
                self.latest_emotion = emotion_name
                self.latest_confidence = confidence
                self.latest_report = engagement_report

        output = self.draw_overlay(image)

        return av.VideoFrame.from_ndarray(
            output,
            format="bgr24"
        )


    def draw_overlay(self, image):
        """
        Draw simple live status on the camera frame.
        """

        summary = self.get_summary()

        face_text = "Face: Yes" if summary["face_found"] else "Face: No"

        engagement = summary["engagement_score"]

        cv2.rectangle(
            image,
            (0, 0),
            (image.shape[1], 125),
            (20, 20, 20),
            -1
        )

        cv2.putText(
            image,
            face_text,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 120),
            2
        )

        cv2.putText(
            image,
            f"Emotion: {summary['latest_emotion']}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            image,
            f"Engagement: {engagement}%",
            (20, 105),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        return image


    def get_summary(self):
        """
        Returns current live session state.
        """

        with self.lock:

            report = getattr(
                self,
                "latest_report",
                {}
            )

            return {
                "face_found":
                    self.face_found,

                "latest_emotion":
                    self.latest_emotion,

                "latest_confidence":
                    self.latest_confidence,

                "eye_contact_score":
                    report.get("eye_contact_score", 0),

                "attention_score":
                    report.get("attention_score", 0),

                "face_visibility":
                    report.get("face_visibility", 0),

                "engagement_score":
                    report.get("engagement_score", 0),

                "total_frames":
                    report.get("total_frames", 0),

                "face_frames":
                    report.get("face_frames", 0)
            }


    def get_report(self):
        """
        Returns final report for the current live session.
        """

        engagement_report = self.engagement.get_report()

        if not engagement_report:
            return {}

        elapsed_seconds = int(
            time.time() - self.start_time
        )

        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60

        duration = f"{minutes} min {seconds} sec"

        return self.report.generate_report(
            engagement_report,
            duration
        )


    def close(self):

        self.face_detector.close()
