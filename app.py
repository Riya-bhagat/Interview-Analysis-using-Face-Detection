from utils.video_processor import VideoProcessor

VIDEO_PATH = "uploads/interview.mp4"

processor = VideoProcessor(VIDEO_PATH)

video_info = processor.get_video_info()

print("=" * 40)
print("VIDEO INFORMATION")
print("=" * 40)

for key, value in video_info.items():
    print(f"{key}: {value}")

frames = processor.extract_frames("outputs/frames")

print("\nFrame Extraction Completed")
print(f"Total Frames Saved: {frames}")