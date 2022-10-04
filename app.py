
import streamlit as st
import random
from youtube import get_info
import database as dbs

@st.cache(allow_output_mutation=True)
def get_workouts():
    return dbs.get_all_workouts() #gets workouts and places them in cache

def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s / 60) % 60)
    hours = int((duration_s / (60*60)) % 24)
    text = ''
    if hours > 0:
        text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        text += f'{minutes:02d}:{seconds:02d}'
    return text


st.title("FitGo Scheduling App")

menu_options = ("Today's Workout Routine", "Available Workouts", "Request Workout", "Chat with Trainer")
selection = st.sidebar.selectbox("Menu", menu_options)

if selection == "Available Workouts":
    st.markdown(f"## Available Workouts")

    workouts = get_workouts()
    for wo in workouts: #extracts info
        url = "https://youtu.be/" + wo["video_id"]
        st.text(wo['title'])
        st.text(f"{wo['channel']} - {get_duration_text(wo['duration'])}")

        ok = st.button('Delete Workout', key=wo["video_id"])
        if ok:
            dbs.delete_workout(wo["video_id"])
            st.legacy_caching.clear_cache()
            st.experimental_rerun()

        st.video(url)
    else:
        st.text("No available workouts in the database!")

elif selection == "Today's Workout Routine":
    st.markdown(f"## Today's Workout Routine")

    workouts = get_workouts()
    if not workouts:
        st.text("No workouts in Database!")
    else:
        wo = dbs.get_todays_workout()

        if not wo:
            # not yet defined
            workouts = get_workouts()
            n = len(workouts)
            idx = random.randint(0, n - 1)
            wo = workouts[idx]
            dbs.update_todays_workout(wo, insert=True)
        else:
            # first item in list
            wo = wo[0]

        if st.button("Choose another workout"):
            workouts = get_workouts()
            n = len(workouts)
            if n > 1:
                idx = random.randint(0, n - 1)
                wo_new = workouts[idx]
                while wo_new['video_id'] == wo['video_id']:
                    idx = random.randint(0, n - 1)
                    wo_new = workouts[idx]
                wo = wo_new
                dbs.update_workout_today(wo)

        url = "https://youtu.be/" + wo["video_id"]
        st.text(wo['title'])
        st.text(f"{wo['channel']} - {get_duration_text(wo['duration'])}")
        st.video(url)

elif selection == "Chat with Trainer":
    st.markdown(f"## Contact a Trainer")

    email_sender = st.text_input("Enter user email ")
    password = st.text_input("Enter user password ", type="password")
    email_receiver = st.text_input("Enter trainer's email")
    subject = st.text_input("Your email subject: ")
    body = st.text_area("Your user email")

    if st.button("Send email"):
        try:
            connection = st.SMTP('smtp.gmail.com', 587)
            connection.starttls()
            connection.login(email_sender, password)
            message = "Subject:{}\n\n{}".format(subject, body)
            connection.sendmail(email_sender, email_receiver, message)
            connection.quit()
            st.success("Email sent successfully")

        except Exception as e:
            if email_sender == "":
                st.error("Please fill user email")

            elif password == "":
                st.error("Please fill user email")

            elif email_receiver == "":
                st.error("Please fill email_receiver")

            elif subject == "":
                st.error("Please fill out the subject")

            else:
                st.error("Please fill out body")






else:
    st.markdown(f"## Request Workout")

    url = st.text_input('Please enter the video url')
    if url:
        workout_data = get_info(url)
        if workout_data is None:
            st.text("Could not find video")
        else:
            st.text(workout_data['title'])
            st.text(workout_data['channel'])
            st.video(url)
            if st.button("Add workout"):
                dbs.insert_workout(workout_data)
                st.text("Added workout!")
                st.legacy_caching.clear_cache()


