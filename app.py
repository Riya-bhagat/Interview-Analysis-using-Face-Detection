import json
import tempfile

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

from modules.emotion_detector import EmotionDetector
from modules.engagement import EngagementAnalyzer
from modules.face_detector import FaceDetector
from modules.live_processor import LiveProcessor
from modules.report_generator import ReportGenerator
from modules.video_processor import VideoProcessor


st.set_page_config(
    page_title="Interview Analysis",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 Interview Analysis")


def analyze_video(video_path):
    """
    Analyze uploaded interview video and return final report.
    """

    video = VideoProcessor(video_path)

    frames = video.extract_frames()

    if len(frames) == 0:
        return None

    face_detector = FaceDetector()
    emotion_detector = EmotionDetector()
    engagement = EngagementAnalyzer()
    report = ReportGenerator()

    progress = st.progress(0)
    status = st.empty()

    total_frames = len(frames)

    for index, frame in enumerate(frames):

        result = face_detector.detect(frame)

        engagement.process_frame(result)

        if result["face_found"]:

            emotion = emotion_detector.detect(
                result["blendshapes"]
            )

            report.add_emotion(
                emotion["emotion"]
            )

        progress.progress(
            (index + 1) / total_frames
        )

        status.info(
            f"Processing frame {index + 1}/{total_frames}"
        )

    face_detector.close()

    engagement_report = engagement.get_report()

    return report.generate_report(
        engagement_report,
        video.get_video_duration()
    )


def show_dashboard(report):
    """
    Show metrics and emotion charts.
    """

    st.subheader("📊 Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Eye Contact",
            f"{report['Eye Contact Score']}%"
        )

    with col2:
        st.metric(
            "Attention",
            f"{report['Attention Score']}%"
        )

    with col3:
        st.metric(
            "Face Visibility",
            f"{report['Face Visibility']}%"
        )

    with col4:
        st.metric(
            "Engagement",
            f"{report['Overall Engagement Score']}%",
            report["Overall Engagement"]
        )

    st.caption(
        f"Analyzed frames: {report['Analyzed Frames']} | "
        f"Face detected frames: {report['Face Detected Frames']}"
    )

    emotions = [
        "Happy",
        "Neutral",
        "Sad",
        "Angry",
        "Fear",
        "Surprise",
        "Disgust"
    ]

    emotion_data = report["Detected Emotions"]

    df = pd.DataFrame({
        "Emotion": emotions,
        "Percentage": [
            emotion_data.get(emotion, 0)
            for emotion in emotions
        ]
    })

    left, right = st.columns(2)

    with left:
        bar = px.bar(
            df,
            x="Emotion",
            y="Percentage",
            text="Percentage",
            color="Emotion"
        )

        bar.update_layout(
            height=420,
            showlegend=False
        )

        st.plotly_chart(
            bar,
            width="stretch"
        )

    with right:
        pie = px.pie(
            df,
            values="Percentage",
            names="Emotion",
            hole=0.45
        )

        pie.update_layout(
            height=420
        )

        st.plotly_chart(
            pie,
            width="stretch"
        )


def show_report(report):
    """
    Show final candidate report and download button.
    """

    st.subheader("📄 Candidate Report")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Duration",
            report["Interview Duration"]
        )

    with col2:
        st.metric(
            "Confidence",
            report["Confidence Level"]
        )

    with col3:
        st.metric(
            "Engagement",
            f"{report['Overall Engagement Score']}%",
            report["Overall Engagement"]
        )

    st.write("Detected Emotions")

    st.json(report["Detected Emotions"])

    st.success(report["Final Recommendation"])

    report_json = json.dumps(
        report,
        indent=4
    )

    st.download_button(
        "Download Report",
        report_json,
        file_name="candidate_report.json",
        mime="application/json",
        width="stretch"
    )


def show_live_interview():
    """
    Shows real-time browser camera analysis.
    """

    st.subheader("🎙️ Live Interview Session")

    st.info(
        "Click START in the camera box, allow camera permission, "
        "answer normally, then click Generate Live Report."
    )

    context = webrtc_streamer(
        key="live-interview",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration={
            "iceServers": [
                {
                    "urls": [
                        "stun:stun.l.google.com:19302"
                    ]
                }
            ]
        },
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        video_processor_factory=LiveProcessor,
        async_processing=False
    )

    processor = context.video_processor

    if processor and hasattr(processor, "get_summary"):

        summary = processor.get_summary()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Current Emotion",
                summary["latest_emotion"]
            )

        with col2:
            st.metric(
                "Eye Contact",
                f"{summary['eye_contact_score']}%"
            )

        with col3:
            st.metric(
                "Attention",
                f"{summary['attention_score']}%"
            )

        with col4:
            st.metric(
                "Frames",
                summary["total_frames"]
            )

        if st.button(
            "Generate Live Report",
            width="stretch"
        ):

            final_report = processor.get_report()

            if not final_report:
                st.error("No live frames analyzed yet. Start the camera first.")
            else:
                st.session_state["candidate_report"] = final_report
                st.success("Live interview report generated.")

    elif context.state.playing:
        st.info("Camera is starting. Please wait a moment.")


st.markdown(
    "Analyze recorded interviews or run a real-time browser camera session. "
    "Dashboard and candidate report are generated on the same page."
)

st.divider()

analysis_tab, dashboard_tab, report_tab = st.tabs(
    [
        "Analyze",
        "Dashboard",
        "Candidate Report"
    ]
)

with analysis_tab:

    analysis_type = st.radio(
        "Choose Analysis Type",
        [
            "Upload Video",
            "Live Interview"
        ],
        horizontal=True
    )

    if st.button(
        "Clear Previous Report",
        width="stretch"
    ):
        st.session_state.pop(
            "candidate_report",
            None
        )

    if analysis_type == "Upload Video":

        uploaded_video = st.file_uploader(
            "Choose Interview Video",
            type=[
                "mp4",
                "avi",
                "mov"
            ]
        )

        if uploaded_video:

            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".mp4"
            )

            temp_file.write(
                uploaded_video.read()
            )

            video_path = temp_file.name

            temp_file.close()

            st.video(video_path)

            if st.button(
                "Analyze Interview",
                width="stretch"
            ):

                final_report = analyze_video(video_path)

                if final_report is None:
                    st.error("No frames could be extracted from this video.")
                else:
                    st.session_state["candidate_report"] = final_report
                    st.success("Interview analysis completed.")

    else:

        show_live_interview()


with dashboard_tab:

    if "candidate_report" in st.session_state:
        show_dashboard(st.session_state["candidate_report"])
    else:
        st.warning("Analyze an interview first.")


with report_tab:

    if "candidate_report" in st.session_state:
        show_report(st.session_state["candidate_report"])
    else:
        st.warning("Analyze an interview first.")
