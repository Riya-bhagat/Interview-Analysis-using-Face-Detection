from modules.video_processor import VideoProcessor

video = VideoProcessor("/Users/riyabhagat/Project/Interview analysis/uploads/interview.mp4")

fps, total_frames, duration = video.get_video_info()

print("FPS:", fps)
print("Total Frames:", total_frames)
print("Duration:", duration)

frames = video.extract_frames()

print("Extracted Frames:", len(frames))