from modules.report_generator import ReportGenerator



report = ReportGenerator()


# simulate emotions detected from frames

emotions = [

    "Neutral",
    "Neutral",
    "Happy",
    "Neutral",
    "Happy",
    "Surprise"

]


for emotion in emotions:

    report.add_emotion(
        emotion
    )



engagement_data = {

    "eye_contact_score":87,

    "attention_score":91,

    "face_visibility":96,

    "engagement_score":90

}



final_report = report.generate_report(

    engagement_data,

    "12 min 35 sec"

)



print(final_report)