from collections import Counter


class ReportGenerator:


    def __init__(self):

        self.emotions = []


    def add_emotion(self, emotion):

        """
        Store detected emotion
        from every frame.
        """

        self.emotions.append(emotion)



    def calculate_emotion_percentage(self):

        if len(self.emotions) == 0:
            return {}


        total = len(self.emotions)


        count = Counter(
            self.emotions
        )


        result = {}


        for emotion, value in count.items():

            percentage = (
                value / total
            ) * 100


            result[emotion] = round(
                percentage,
                2
            )


        return result



    def confidence_level(self, engagement):

        if engagement >= 80:
            return "Excellent"

        elif engagement >= 60:
            return "Good"

        elif engagement >= 40:
            return "Average"

        else:
            return "Low"



    def engagement_level(self, score):

        if score >= 80:
            return "High"

        elif score >= 60:
            return "Medium"

        else:
            return "Low"



    def generate_report(
            self,
            engagement_report,
            duration
    ):


        emotion_percentage = (
            self.calculate_emotion_percentage()
        )


        engagement_score = (
            engagement_report["engagement_score"]
        )


        confidence = self.confidence_level(
            engagement_score
        )


        engagement = self.engagement_level(
            engagement_score
        )



        recommendation = self.generate_recommendation(
            engagement,
            confidence
        )



        return {


            "Interview Duration":
                duration,


            "Detected Emotions":
                emotion_percentage,


            "Eye Contact Score":
                engagement_report[
                    "eye_contact_score"
                ],


            "Attention Score":
                engagement_report[
                    "attention_score"
                ],


            "Face Visibility":
                engagement_report[
                    "face_visibility"
                ],


            "Overall Engagement":
                engagement,


            "Confidence Level":
                confidence,


            "Final Recommendation":
                recommendation

        }



    def generate_recommendation(
            self,
            engagement,
            confidence
    ):


        if engagement == "High":

            return (
                "Candidate appeared attentive, "
                "maintained good eye contact, "
                "showed positive expressions, "
                "and remained engaged throughout "
                "the interview."
            )


        elif engagement == "Medium":

            return (
                "Candidate showed moderate "
                "engagement with acceptable "
                "attention during the interview."
            )


        else:

            return (
                "Candidate showed low engagement "
                "and inconsistent attention "
                "during the interview."
            )