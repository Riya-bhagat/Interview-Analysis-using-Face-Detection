import numpy as np


class EngagementAnalyzer:

    def __init__(self):

        self.total_frames = 0
        self.face_frames = 0
        self.eye_contact_frames = 0
        self.attention_frames = 0


    def calculate_eye_contact(self, landmarks):

        """
        Estimate if candidate is looking at camera
        using eye landmarks.
        """

        # MediaPipe eye landmark indexes

        left_eye = [
            33,
            133,
            159,
            145
        ]

        right_eye = [
            362,
            263,
            386,
            374
        ]


        # Get eye center

        left_center_x = np.mean(
            [landmarks[i].x for i in left_eye]
        )

        right_center_x = np.mean(
            [landmarks[i].x for i in right_eye]
        )


        # Eyes are near center

        if (
            0.35 < left_center_x < 0.65
            and
            0.35 < right_center_x < 0.65
        ):
            return True


        return False



    def calculate_attention(self, head_matrix):

        """
        Calculate attention using head rotation.
        """

        matrix = np.array(head_matrix)


        # Rotation values

        yaw = matrix[0][2]

        pitch = matrix[1][2]


        # Facing camera

        if (
            abs(yaw) < 0.35
            and
            abs(pitch) < 0.35
        ):
            return True


        return False



    def process_frame(self, result):

        """
        Process every video frame.
        """

        self.total_frames += 1


        if result["face_found"]:

            self.face_frames += 1


            if self.calculate_eye_contact(
                result["landmarks"]
            ):
                self.eye_contact_frames += 1



            if self.calculate_attention(
                result["head_matrix"]
            ):
                self.attention_frames += 1



    def get_report(self):

        if self.total_frames == 0:
            return {}


        face_visibility = (
            self.face_frames /
            self.total_frames
        ) * 100


        eye_contact = (
            self.eye_contact_frames /
            self.total_frames
        ) * 100


        attention = (
            self.attention_frames /
            self.total_frames
        ) * 100



        engagement = (
            eye_contact * 0.4
            +
            attention * 0.4
            +
            face_visibility * 0.2
        )


        return {

            "eye_contact_score":
                round(eye_contact,2),

            "attention_score":
                round(attention,2),

            "face_visibility":
                round(face_visibility,2),

            "engagement_score":
                round(engagement,2)
        }