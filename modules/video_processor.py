import cv2


class VideoProcessor:

    def __init__(self, video_path):
        # Save the video path
        self.video_path = video_path

        # Open the video
        self.cap = cv2.VideoCapture(video_path)

        # Check whether video opened successfully
        if not self.cap.isOpened():
            raise ValueError("Unable to open video.")


    def get_video_info(self):
        """
        Returns FPS, total frames and duration.
        """

        fps = self.cap.get(cv2.CAP_PROP_FPS)

        total_frames = int(
            self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        duration = total_frames / fps

        return fps, total_frames, duration


    def extract_frames(self):

        frames = []

        fps = int(
            self.cap.get(cv2.CAP_PROP_FPS)
        )

        frame_number = 0

        while True:

            success, frame = self.cap.read()

            if not success:
                break

            if frame_number % fps == 0:
                frames.append(frame)

            frame_number += 1

        self.cap.release()

        return frames