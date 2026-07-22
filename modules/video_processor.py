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

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(
            self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )

        if self.fps <= 0:
            self.fps = 1

    def get_video_info(self):
        """
        Returns FPS, total frames and duration.
        """

        duration = self.total_frames / self.fps

        return self.fps, self.total_frames, duration

    def get_video_duration(self):
        """
        Returns formatted video duration.
        """

        duration = self.total_frames / self.fps

        minutes = int(duration // 60)

        seconds = int(duration % 60)

        return f"{minutes} min {seconds} sec"


    def extract_frames(self):

        frames = []

        sample_rate = max(
            1,
            int(self.fps)
        )

        frame_number = 0

        while True:

            success, frame = self.cap.read()

            if not success:
                break

            if frame_number % sample_rate == 0:
                frames.append(frame)

            frame_number += 1

        self.cap.release()

        return frames
