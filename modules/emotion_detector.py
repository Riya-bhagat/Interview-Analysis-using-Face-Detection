class EmotionDetector:
    """
    Emotion Detection using MediaPipe Blendshapes
    """

    def __init__(self):
        pass

    def get_score(self, blendshapes):
        """
        Convert blendshapes into a dictionary
        """
        scores = {}

        for shape in blendshapes:
            scores[shape.category_name] = shape.score

        return scores

    def detect(self, blendshapes):

        b = self.get_score(blendshapes)

        # ---------- Feature Scores ----------

        smile = (
            b.get("mouthSmileLeft", 0) +
            b.get("mouthSmileRight", 0)
        ) / 2

        frown = (
            b.get("mouthFrownLeft", 0) +
            b.get("mouthFrownRight", 0)
        ) / 2

        brow_down = (
            b.get("browDownLeft", 0) +
            b.get("browDownRight", 0)
        ) / 2

        brow_up = b.get("browInnerUp", 0)

        jaw_open = b.get("jawOpen", 0)

        eye_wide = (
            b.get("eyeWideLeft", 0) +
            b.get("eyeWideRight", 0)
        ) / 2

        cheek = (
            b.get("cheekSquintLeft", 0) +
            b.get("cheekSquintRight", 0)
        ) / 2

        nose = (
            b.get("noseSneerLeft", 0) +
            b.get("noseSneerRight", 0)
        ) / 2

        upper_lip = (
            b.get("mouthUpperUpLeft", 0) +
            b.get("mouthUpperUpRight", 0)
        ) / 2

        # ---------- Emotion Scores ----------

        happy = (
            smile * 4 +
            cheek
        )

        sad = (
            frown * 3 +
            brow_up +
            (0.2 - smile)
        )

        angry = (
            brow_down * 3 +
            nose
        )

        fear = (
            eye_wide * 3 +
            jaw_open +
            brow_up
        )

        surprise = (
            jaw_open * 3 +
            eye_wide * 2 +
            brow_up
        )

        disgust = (
            nose * 3 +
            upper_lip * 2
        )

        # Neutral becomes smaller if expressions become stronger
        neutral = max(
            0,
            1 - (
                smile +
                frown +
                jaw_open +
                brow_down +
                eye_wide
            )
        )

        emotion_scores = {
            "Happy": round(happy, 3),
            "Neutral": round(neutral, 3),
            "Sad": round(sad, 3),
            "Angry": round(angry, 3),
            "Fear": round(fear, 3),
            "Surprise": round(surprise, 3),
            "Disgust": round(disgust, 3)
        }

        emotion = max(emotion_scores, key=emotion_scores.get)

        confidence = emotion_scores[emotion]

        return {
            "emotion": emotion,
            "confidence": confidence,
            "scores": emotion_scores
        }