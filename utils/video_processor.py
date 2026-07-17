import cv2
import os


class VideoProcessor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise ValueError(f"Unable to open video: {video_path}")

    def get_video_info(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        duration = total_frames / fps if fps > 0 else 0

        return {
            "FPS": round(fps, 2),
            "Total Frames": total_frames,
            "Width": width,
            "Height": height,
            "Duration (seconds)": round(duration, 2)
        }

    def extract_frames(self, output_folder):
        os.makedirs(output_folder, exist_ok=True)

        frame_count = 0

        while True:
            success, frame = self.cap.read()

            if not success:
                break

            filename = os.path.join(
                output_folder,
                f"frame_{frame_count:05d}.jpg"
            )

            cv2.imwrite(filename, frame)
            frame_count += 1

        self.cap.release()

        return frame_count