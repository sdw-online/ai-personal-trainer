from fileinput import filename
import cv2
import time
import streamlit as st
import numpy as np
import json
import requests
from streamlit_lottie import st_lottie
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils  # for mp models to draw on images
mp_pose = mp.solutions.pose  # for importing pose estimation models e.g. face detection, face mesh, hand detections etc


# ----Config Section-----

# Set up title
st.set_page_config(page_title="My AI Trainer", 
                   layout="wide", 
                   page_icon="🧊", 
                   menu_items= 
         {'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!" }    
)

st.title("Live AI Personal Trainer")





# Load animations via Lottie website
def load_animation_via_link(web_link):
    r = requests.get(web_link)
    if r.status_code != 200:
        return None
    return r.json()


# Load animations via local environment
def load_animation_via_desktop(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


# Style your contact form
def style_contact_doc(file_name):
    with open(file=file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)




# -------Header Section------
with st.container():
    columnL, columnR = st.columns(2)
    with columnL:
        st.subheader("Welcome to my AI Personal Trainer v1.0! :movie_camera: ")
        st.markdown("Where artificial intelligence tracks your workout techniques in real-time to get the most out of your workout :camera: ")
        # lottie_animation = load_animation_via_link("https://assets5.lottiefiles.com/packages/lf20_v4isjbj5.json")
        lottie_animation = load_animation_via_link("https://assets7.lottiefiles.com/packages/lf20_zrqthn6o.json")
        st_lottie(lottie_animation, height=400, width=700, key="ai_robot1")
    with columnR:
        
        lottie_animation = load_animation_via_link("https://assets10.lottiefiles.com/packages/lf20_kq6zs04j.json")
        st_lottie(lottie_animation, height=400, width=700, key="github")
        st.subheader(" How to use this app ")
        st.markdown("""     
        
        The AI personal trainer is designed to monitor your workout movement and technique during each exercise rep. **Good workout technique** is rewarded with one rep count and **bad workout technique** is not recorded at all. 

        1. Select on a workout on the left 
        2. Click **Start Workout** to begin workout session
        3. Press 'q' on your keyboard to exit session once completed


        """)



# --------------Workout Selection -----------------------
with st.container():
    columnL, columnR = st.columns(2)
    with columnL:
        st.write('---------------')
        workout = st.selectbox('Select your exercise:', ('None', 'Bicep Curls', 'Push-ups', 'Squats', 'High-Knees'))
        st.write('Your selection:', workout)
        st.text("")
        run = st.checkbox('Start Workout', value=False, key=1)
        st.text("")
        st.text("")
    with columnR:
        pass

# Prompt user if  "Run Workout" is selected without an exercise picked
if workout == 'None' and run is True:
    st.markdown("You need to select a workout before you can begin session")




# Bicep Curls
if workout == "Bicep Curls":
    with st.container():
        columnL, columnR = st.columns(2)
        with columnL:
            lottie_animation = load_animation_via_link("https://assets1.lottiefiles.com/packages/lf20_l0u0rf4r.json")
            st_lottie(lottie_animation, height=400, width=600, key="push_ups")
        with columnR:
            st.header("Bicep Curls")
            st.subheader("Preparation")
            st.markdown("""
                * Warm up your arms by performing light stretches before beginning workout 
                

            """)
            # st.markdown("""""")

            st.subheader("Tips")
            st.markdown("""
            
            - Curl dumbbell towards the region between your chest and bicep
            - Curl back down to starting position and repeat motion 
            - Keep shoulder and elbow locked to your side through out the exercise
            - Squeeze biceps tight through out the exercise
              

            """)
            st.subheader("Notes")
            st.markdown("""
                * Make sure your streaming device (camera/webcam) is on 
                * Face your camera during your workout for the algorithm to successfully detect your body joints during your workout

            """)
            if run:
                st.markdown(""" 
                **Remember to prioritize good technique when performing your exercise to get the best 
                out of your sessions - enjoy your workout!**  
                """)
                def calculate_bicep_angle(a, b, c):
                    a = np.array(a)  # First endpoint
                    b = np.array(b)  # Middle endpoint
                    c = np.array(c)  # Last endpoint
                
                    # Calculate radians to convert to angles
                    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                    angle = np.abs(radians * 180.0 / np.pi)
                
                    # Convert angle between 0 and 180 
                    if angle > 180.0:
                        angle = 360 - angle
                
                    return angle


                cap = cv2.VideoCapture(0)
                
                # Establish your counter variables
                counter = 0  # number of curls to start with
                arm_position = None  # top or bottom part of your curl
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                with mp_pose.Pose(min_detection_confidence=0.5,
                                min_tracking_confidence=0.5) as pose:  # level of detection & tracking accuracy
                    while cap.isOpened():
                        success, frame = cap.read()
                
                        # Recolour image from BGR to RGB 
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False  # make pixel arrays read-only to detect image (saves disk memory)
                
                        # Detect image 
                        results = pose.process(image)
                
                        # Recolour image from RGB to BGR again
                        image.flags.writeable = True    # Make pixel arrays writable (editable) to revert from RGB to BGR
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        image = cv2.resize(image, (1280, 720))
                
                        # Extract landmarks by collecting x,y coordinates for useful body joints
                        try:
                            landmarks = results.pose_landmarks.landmark
                
                            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
                            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
                            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]
                
                            angle = calculate_bicep_angle(shoulder, elbow, wrist)
                
                            # Display angles in images 
                            cv2.putText(image, str(angle),
                                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                                        font, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                
                            # Count the number of bicep curls 
                            if angle > 160:  # if angle is greater than 160...
                                arm_position = "down"  # ... then arm position is down
                
                            if angle < 30 and arm_position == "down":  # if angle is less than 30 and arm position is down...
                                arm_position = "up"  # ...record arm position as up...
                                counter += 1  # ...and add one rep to the total reps ...
                                print(counter)  # ... and display total counts
                
                        except:
                            pass
                
                        # Create progress tracking box at the top left of the screen  
                        # '''Rectangle 1 '''
                
                        rect1_starting_point = (0, 0)
                        rect1_ending_point = (370, 82)
                        rect1_colour = (245, 117, 16)
                        rect1_thickness = -1
                
                        cv2.rectangle(image,
                                    rect1_starting_point,  # starting point
                                    rect1_ending_point,  # ending point
                                    rect1_colour,  # box colour
                                    rect1_thickness)  # thickness
                
                        # Add 'WORKOUT' title to rectangle
                
                        rect1_title = 'WORKOUT'
                        rect1_title_text_org = (15, 12)
                        rect1_title_font = font
                        rect1_title_font_scale = 0.5
                        rect1_title_colour = (0, 0, 0)
                        rect1_title_text_thickness = 1
                        rect1_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect1_title,
                                    rect1_title_text_org,
                                    rect1_title_font,
                                    rect1_title_font_scale,
                                    rect1_title_colour,
                                    rect1_title_text_thickness,
                                    rect1_title_line_type)
                
                        # Add workout type
                
                        rect1_body = 'Bicep Curls'
                        rect1_body_text_org = (10, 65)
                        rect1_body_font = font
                        rect1_body_font_scale = 2
                        rect1_body_colour = (255, 255, 255)
                        rect1_body_text_thickness = 2
                        rect1_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect1_body,
                                    rect1_body_text_org,
                                    rect1_body_font,
                                    rect1_body_font_scale,
                                    rect1_body_colour,
                                    rect1_body_text_thickness,
                                    rect1_body_line_type)
                
                        # '''Rectangle 2 '''
                
                        rect2_starting_point = (1000, 82)
                        rect2_ending_point = (1400, 0)
                        rect2_colour = (100, 255, 50)
                        rect2_thickness = -1
                
                        cv2.rectangle(image,
                                    rect2_starting_point,  # starting point (top left corner)
                                    rect2_ending_point,  # ending point (bottom right corner)
                                    rect2_colour,
                                    rect2_thickness
                                    )
                
                        # Add reps total  
                
                        rect2a_title = 'REPS'
                        rect2a_title_text_org = (1016, 12)
                        rect2a_title_font = font
                        rect2a_title_font_scale = 0.5
                        rect2a_title_colour = (0, 0, 0)
                        rect2a_title_text_thickness = 1
                        rect2a_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2a_title,
                                    rect2a_title_text_org,
                                    rect2a_title_font,
                                    rect2a_title_font_scale,
                                    rect2a_title_colour,
                                    rect2a_title_text_thickness,
                                    rect2a_title_line_type)
                
                        rect2a_body = str(counter)
                        rect2a_body_text_org = (1016, 64)
                        rect2a_body_font = font
                        rect2a_body_font_scale = 2
                        rect2a_body_colour = (255, 255, 255)
                        rect2a_body_text_thickness = 2
                        rect2a_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2a_body,
                                    rect2a_body_text_org,
                                    rect2a_body_font,
                                    rect2a_body_font_scale,
                                    rect2a_body_colour,
                                    rect2a_body_text_thickness,
                                    rect2a_body_line_type)
                
                        # Add arm position     
                
                        rect2b_title = 'ARM POSITION'
                        rect2b_title_text_org = (1122, 12)
                        rect2b_title_font = font
                        rect2b_title_font_scale = 0.5
                        rect2b_title_colour = (0, 0, 0)
                        rect2b_title_text_thickness = 1
                        rect2b_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2b_title,
                                    rect2b_title_text_org,
                                    rect2b_title_font,
                                    rect2b_title_font_scale,
                                    rect2b_title_colour,
                                    rect2b_title_text_thickness,
                                    rect2b_title_line_type)
                
                        rect2b_body = str(arm_position)
                        rect2b_body_text_org = (1122, 64)
                        rect2b_body_font = font
                        rect2b_body_font_scale = 2
                        rect2b_body_colour = (255, 255, 255)
                        rect2b_body_text_thickness = 2
                        rect2b_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2b_body,
                                    rect2b_body_text_org,
                                    rect2b_body_font,
                                    rect2b_body_font_scale,
                                    rect2b_body_colour,
                                    rect2b_body_text_thickness,
                                    rect2b_body_line_type)
                
                        # Use model to identify landmarks in the image 
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                                mp_drawing.DrawingSpec(color=(164, 66, 22), thickness=6, circle_radius=7)
                                                )
                
                        cv2.imread('AI Personal Trainer', image)
                
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                
                cap.release()
                cv2.destroyAllWindows()
                
                



# Pushups
if workout == "Push-ups":
    with st.container():
        columnL, columnR = st.columns(2)
        with columnL:
            lottie_animation = load_animation_via_link("https://assets1.lottiefiles.com/packages/lf20_fyj5ox9g.json")
            st_lottie(lottie_animation, height=400, width=600, key="push_ups")
        with columnR:
            st.header("Push-ups")
            st.subheader("Preparation")
            st.markdown("""
                * Ensure you have performed light cardio and stretches before performing push ups to get your blood flow running 

            """)
            # st.markdown("""""")

            st.subheader("Tips")
            st.markdown("""
            
            Tips on good push-up technique:
            - Keep a straight spine from start to finish
            - Slowly dip your body towards the ground then push the ground away from you
            - Clench your core as tight as if you're about to get punched in the stomach through out the workout
              

            """)
            st.subheader("Notes")
            st.markdown("""
                * Make sure your streaming device (camera/webcam) is on 
                * Face your camera during your workout for the algorithm to successfully detect your body joints during your workout

            """)
            if run:
                st.markdown("""
                **Remember to prioritize good technique when performing your exercise to get the best 
                out of your sessions - enjoy your workout!**

                """)

                # Create function that forms angles at 3 end-points - the return of trigonometry :)
                def calculate_pushup_angle(a, b, c):
                    a = np.array(a)  # First endpoint
                    b = np.array(b)  # Middle endpoint
                    c = np.array(c)  # Last endpoint

                    # Calculate radians to convert to angles
                    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
                    angle = np.abs(radians * 180.0 / np.pi)
                    angle = abs(angle)

                    # Convert angle between 0 and 180 
                    if angle > 180.0:
                        angle = 360 - angle

                    return abs(angle)




                # Establish your counter variables
                cap = cv2.VideoCapture(0)
                if not cap.isOpened():
                    print("Cannot open camera")
                    exit()

                counter = 0  # number of curls to start with
                pushup_position = None  # top or bottom part of your curl
                font = cv2.FONT_HERSHEY_SIMPLEX

                with mp_pose.Pose(min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5) as pose:  # level of detection & tracking accuracy
                    while cap.isOpened():
                        ret, frame = cap.read()

                        if ret:
                            assert not isinstance(frame, type(None))
                        
                        if not ret:
                            print(" Ignoring empty webcam frame ")
                            continue
                        frame = cv2.flip(frame, 0)
                        frame = cv2.flip(frame, 0)

                        if frame is not None:

                            # Recolour image from BGR to RGB 
                            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            image.flags.writeable = False  # make pixel arrays read-only to detect image (saves disk memory)

                            # Detect image
                            results = pose.process(image)

                            # Recolour image from RGB to BGR again
                            image.flags.writeable = True  # Make pixel arrays writable (editable) to revert from RGB to BGR
                            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                            image = cv2.resize(image, (1280, 720))

                            try:
                                # Extract landmarks by collecting x,y coordinates for useful body joints
                                # if results.pose_landmarks.landmark:
                                landmarks = results.pose_landmarks.landmark

                                shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
                                elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
                                wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]

                                angle = calculate_pushup_angle(shoulder, elbow, wrist)

                                # Display angles in images 
                                cv2.putText(image, str(angle),
                                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
                                            font, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                            )

                                # Count the number of pushups
                                if angle > 170:  # if angle is greater than 160...
                                    pushup_position = "up"  # ... then arm position is down

                                if angle < 45 and pushup_position == "up":  # if angle is less than 30 and arm position is down...
                                    pushup_position = "down"  # ...record arm position as up...
                                    counter += 1  # ...and add one rep to the total reps ...
                                    print(counter)  # ... and display total counts

                            except AttributeError as ae:
                                # print(" Camera unable to capture landmarks in specific frames properly ")
                                continue

                            # Create progress tracking box at the top left of the screen  
                            # '''Rectangle 1 '''

                            rect1_starting_point = (0, 0)
                            rect1_ending_point = (370, 82)
                            rect1_colour = (245, 117, 16)
                            rect1_thickness = -1

                            cv2.rectangle(image,
                                          rect1_starting_point,  # starting point
                                          rect1_ending_point,  # ending point
                                          rect1_colour,  # box colour
                                          rect1_thickness)  # thickness

                            # Add 'WORKOUT' title to rectangle

                            rect1_title = 'WORKOUT'
                            rect1_title_text_org = (15, 12)
                            rect1_title_font = font
                            rect1_title_font_scale = 0.5
                            rect1_title_colour = (0, 0, 0)
                            rect1_title_text_thickness = 1
                            rect1_title_line_type = cv2.LINE_AA

                            cv2.putText(image,
                                        rect1_title,
                                        rect1_title_text_org,
                                        rect1_title_font,
                                        rect1_title_font_scale,
                                        rect1_title_colour,
                                        rect1_title_text_thickness,
                                        rect1_title_line_type)

                            # Add workout type

                            rect1_body = 'Pushups'
                            rect1_body_text_org = (10, 65)
                            rect1_body_font = font
                            rect1_body_font_scale = 2
                            rect1_body_colour = (255, 255, 255)
                            rect1_body_text_thickness = 2
                            rect1_body_line_type = cv2.LINE_AA

                            cv2.putText(image,
                                        rect1_body,
                                        rect1_body_text_org,
                                        rect1_body_font,
                                        rect1_body_font_scale,
                                        rect1_body_colour,
                                        rect1_body_text_thickness,
                                        rect1_body_line_type)

                            # '''Rectangle 2 '''

                            rect2_starting_point = (1000, 82)
                            rect2_ending_point = (1400, 0)
                            rect2_colour = (100, 255, 50)
                            rect2_thickness = -1

                            cv2.rectangle(image,
                                          rect2_starting_point,  # starting point (top left corner)
                                          rect2_ending_point,  # ending point (bottom right corner)
                                          rect2_colour,
                                          rect2_thickness
                                          )

                            # Add reps total  

                            rect2a_title = 'REPS'
                            rect2a_title_text_org = (1016, 12)
                            rect2a_title_font = font
                            rect2a_title_font_scale = 0.5
                            rect2a_title_colour = (0, 0, 0)
                            rect2a_title_text_thickness = 1
                            rect2a_title_line_type = cv2.LINE_AA

                            cv2.putText(image,
                                        rect2a_title,
                                        rect2a_title_text_org,
                                        rect2a_title_font,
                                        rect2a_title_font_scale,
                                        rect2a_title_colour,
                                        rect2a_title_text_thickness,
                                        rect2a_title_line_type)

                            rect2a_body = str(counter)
                            rect2a_body_text_org = (1016, 64)
                            rect2a_body_font = font
                            rect2a_body_font_scale = 2
                            rect2a_body_colour = (255, 255, 255)
                            rect2a_body_text_thickness = 2
                            rect2a_body_line_type = cv2.LINE_AA

                            cv2.putText(image,
                                        rect2a_body,
                                        rect2a_body_text_org,
                                        rect2a_body_font,
                                        rect2a_body_font_scale,
                                        rect2a_body_colour,
                                        rect2a_body_text_thickness,
                                        rect2a_body_line_type)

                            # Add arm position     

                            rect2b_title = 'PUSHUP POSITION'
                            rect2b_title_text_org = (1122, 12)
                            rect2b_title_font = font
                            rect2b_title_font_scale = 0.5
                            rect2b_title_colour = (0, 0, 0)
                            rect2b_title_text_thickness = 1
                            rect2b_title_line_type = cv2.LINE_AA

                            cv2.putText(image,
                                        rect2b_title,
                                        rect2b_title_text_org,
                                        rect2b_title_font,
                                        rect2b_title_font_scale,
                                        rect2b_title_colour,
                                        rect2b_title_text_thickness,
                                        rect2b_title_line_type)

                            rect2b_body = str(pushup_position)
                            rect2b_body_text_org = (1122, 64)
                            rect2b_body_font = font
                            rect2b_body_font_scale = 2
                            rect2b_body_colour = (255, 255, 255)
                            rect2b_body_text_thickness = 2
                            rect2b_body_line_type = cv2.LINE_AA

                            cv2.putText(image,
                                        rect2b_body,
                                        rect2b_body_text_org,
                                        rect2b_body_font,
                                        rect2b_body_font_scale,
                                        rect2b_body_colour,
                                        rect2b_body_text_thickness,
                                        rect2b_body_line_type)

                            # Use model to identify landmarks in the image 
                            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                      mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2,
                                                                             circle_radius=2),
                                                      mp_drawing.DrawingSpec(color=(164, 66, 22), thickness=6,
                                                                             circle_radius=7)
                                                      )

                            cv2.imread('AI Personal Trainer', image)
                            if cv2.waitKey(1) & 0xFF == ord('q'):
                                break
                cap.release()
                cv2.destroyAllWindows()


# Squats
if workout == "Squats":
    with st.container():
        columnL, columnR = st.columns(2)
        with columnL:
            lottie_animation = load_animation_via_link("https://assets8.lottiefiles.com/packages/lf20_Pkg2zS.json")
            st_lottie(lottie_animation, height=400, width=600, key="push_ups")
        with columnR:
            st.header("Squats")
            st.subheader("Preparation")
            st.markdown("""
                * Perform warm up exercises like jogging/skipping on the spot to prepare your legs for squats 

            """)
            # st.markdown("""""")

            st.subheader("Tips")
            st.markdown("""
            
            - Keep your feet shoulder-width apart
            - Keep your back straight through out exercise
            - Focus on dipping until your hip joint is lower than your knee joint
            - Drive back up with your chest
              
            """)
            st.subheader("Notes")
            st.markdown("""
                * Make sure your streaming device (camera/webcam) is on 
                * Face your camera during your workout for the algorithm to successfully detect your body joints during your workout

            """)
            if run:
                st.markdown(""" **Remember to prioritize good technique when performing your exercise to get the best 
                out of your sessions - enjoy your workout!** """)
                def calculate_squat_angle(a,b,c):
                    a = np.array(a) # First endpoint
                    b = np.array(b) # Middle endpoint
                    c = np.array(c) # Last endpoint
                    
                    # Calculate radians to convert to angles
                    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                    angle = np.abs(radians * 180.0/np.pi) 
                    angle = abs(angle)
                    
                    # Convert angle between 0 and 180 
                    if angle > 180.0:
                        angle=360-angle
                        
                    return abs(angle)
                    
                cap = cv2.VideoCapture(0)
                
                # Establish your counter variables
                counter = 0  # number of curls to start with
                squat_position = None  # top or bottom part of your curl
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                with mp_pose.Pose(min_detection_confidence=0.5,
                                min_tracking_confidence=0.5) as pose:  # level of detection & tracking accuracy
                    while cap.isOpened():
                        success, frame = cap.read()
                
                        # Recolour image from BGR to RGB 
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False  # make pixel arrays read-only to detect image (saves disk memory)
                
                        # Detect image 
                        results = pose.process(image)
                
                        # Recolour image from RGB to BGR again
                        image.flags.writeable = True    # Make pixel arrays writable (editable) to revert from RGB to BGR
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        image = cv2.resize(image, (1280, 720))
                
                        # Extract landmarks by collecting x,y coordinates for useful body joints
                        try:
                            landmarks = results.pose_landmarks.landmark
                            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
                            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
                            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
                            
                            angle = calculate_squat_angle(hip, knee, ankle)
                
                            # Display angles in images 
                            cv2.putText(image, str(angle),
                                        tuple(np.multiply(knee, [640, 480]).astype(int)),
                                        font, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                
                            # Count the number of squats
                            if angle > 170:  # if angle is greater than 160...
                                squat_position = "up"  # ... then arm position is down
                
                            if angle < 60 and squat_position == "up":  # if angle is less than 30 and arm position is down...
                                squat_position = "down"  # ...record arm position as up...
                                counter += 1  # ...and add one rep to the total reps ...
                                print(counter)  # ... and display total counts
                
                        except:
                            pass
                
                        # Create progress tracking box at the top left of the screen  
                        # '''Rectangle 1 '''
                
                        rect1_starting_point = (0, 0)
                        rect1_ending_point = (370, 82)
                        rect1_colour = (245, 117, 16)
                        rect1_thickness = -1
                
                        cv2.rectangle(image,
                                    rect1_starting_point,  # starting point
                                    rect1_ending_point,  # ending point
                                    rect1_colour,  # box colour
                                    rect1_thickness)  # thickness
                
                        # Add 'WORKOUT' title to rectangle
                
                        rect1_title = 'WORKOUT'
                        rect1_title_text_org = (15, 12)
                        rect1_title_font = font
                        rect1_title_font_scale = 0.5
                        rect1_title_colour = (0, 0, 0)
                        rect1_title_text_thickness = 1
                        rect1_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect1_title,
                                    rect1_title_text_org,
                                    rect1_title_font,
                                    rect1_title_font_scale,
                                    rect1_title_colour,
                                    rect1_title_text_thickness,
                                    rect1_title_line_type)
                
                        # Add workout type
                
                        rect1_body = 'Squats'
                        rect1_body_text_org = (10, 65)
                        rect1_body_font = font
                        rect1_body_font_scale = 2
                        rect1_body_colour = (255, 255, 255)
                        rect1_body_text_thickness = 2
                        rect1_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect1_body,
                                    rect1_body_text_org,
                                    rect1_body_font,
                                    rect1_body_font_scale,
                                    rect1_body_colour,
                                    rect1_body_text_thickness,
                                    rect1_body_line_type)
                
                        # '''Rectangle 2 '''
                
                        rect2_starting_point = (1000, 82)
                        rect2_ending_point = (1400, 0)
                        rect2_colour = (100, 255, 50)
                        rect2_thickness = -1
                
                        cv2.rectangle(image,
                                    rect2_starting_point,  # starting point (top left corner)
                                    rect2_ending_point,  # ending point (bottom right corner)
                                    rect2_colour,
                                    rect2_thickness
                                    )
                
                        # Add reps total  
                
                        rect2a_title = 'REPS'
                        rect2a_title_text_org = (1016, 12)
                        rect2a_title_font = font
                        rect2a_title_font_scale = 0.5
                        rect2a_title_colour = (0, 0, 0)
                        rect2a_title_text_thickness = 1
                        rect2a_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2a_title,
                                    rect2a_title_text_org,
                                    rect2a_title_font,
                                    rect2a_title_font_scale,
                                    rect2a_title_colour,
                                    rect2a_title_text_thickness,
                                    rect2a_title_line_type)
                
                        rect2a_body = str(counter)
                        rect2a_body_text_org = (1016, 64)
                        rect2a_body_font = font
                        rect2a_body_font_scale = 2
                        rect2a_body_colour = (255, 255, 255)
                        rect2a_body_text_thickness = 2
                        rect2a_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2a_body,
                                    rect2a_body_text_org,
                                    rect2a_body_font,
                                    rect2a_body_font_scale,
                                    rect2a_body_colour,
                                    rect2a_body_text_thickness,
                                    rect2a_body_line_type)
                
                        # Add arm position     
                
                        rect2b_title = 'LEG POSITION'
                        rect2b_title_text_org = (1122, 12)
                        rect2b_title_font = font
                        rect2b_title_font_scale = 0.5
                        rect2b_title_colour = (0, 0, 0)
                        rect2b_title_text_thickness = 1
                        rect2b_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2b_title,
                                    rect2b_title_text_org,
                                    rect2b_title_font,
                                    rect2b_title_font_scale,
                                    rect2b_title_colour,
                                    rect2b_title_text_thickness,
                                    rect2b_title_line_type)
                
                        rect2b_body = str(squat_position)
                        rect2b_body_text_org = (1122, 64)
                        rect2b_body_font = font
                        rect2b_body_font_scale = 2
                        rect2b_body_colour = (255, 255, 255)
                        rect2b_body_text_thickness = 2
                        rect2b_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2b_body,
                                    rect2b_body_text_org,
                                    rect2b_body_font,
                                    rect2b_body_font_scale,
                                    rect2b_body_colour,
                                    rect2b_body_text_thickness,
                                    rect2b_body_line_type)
                
                        # Use model to identify landmarks in the image 
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                                mp_drawing.DrawingSpec(color=(164, 66, 22), thickness=6, circle_radius=7)
                                                )
                
                        cv2.imread('AI Personal Trainer', image)
                
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                
                
                cap.release()
                cv2.destroyAllWindows()



# High Knees
if workout == "High-Knees":
    with st.container():
        columnL, columnR = st.columns(2)
        with columnL:
            lottie_animation = load_animation_via_link("https://assets7.lottiefiles.com/packages/lf20_mzbdc0qk.json")
            st_lottie(lottie_animation, height=400, width=600, key="push_ups")
        with columnR:
            st.header("High Knees")
            st.subheader("Preparation")
            st.markdown("""
                * Perform warm up exercises like jogging/skipping on the spot to prepare your legs for squats

            """)
            # st.markdown("""""")

            st.subheader("Tips")
            st.markdown("""
            
            
            - Align your feet the same distance apart as your hips
            - Maintain a straight back through out workout
            - Raise each knee above your hip joint 
            - Pump your arms with each knee raise to get the heart rate high  
              

            """)
            st.subheader("Notes")
            st.markdown("""
                * Make sure your streaming device (camera/webcam) is on 
                * Face your camera during your workout for the algorithm to successfully detect your body joints during your workout

            """)
            if run:
                st.markdown(""" **Remember to prioritize good technique when performing your exercise to get the best 
                out of your sessions - enjoy your workout!** """)
                def calculate_high_knee_angle(a,b,c):
                    a = np.array(a) # First endpoint
                    b = np.array(b) # Middle endpoint
                    c = np.array(c) # Last endpoint
                    
                    # Calculate radians to convert to angles
                    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                    angle = np.abs(radians * 180.0/np.pi) 
                    angle = abs(angle)
                    
                    # Convert angle between 0 and 180 
                    if angle > 180.0:
                        angle=360-angle
                        
                    return abs(angle) 
                    
                
                cap = cv2.VideoCapture(0)
                
                # Establish your counter variables
                counter = 0  # number of curls to start with
                high_knee_position = None  # top or bottom part of your curl
                font = cv2.FONT_HERSHEY_SIMPLEX
                
                with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:  # level of detection & tracking accuracy
                    while cap.isOpened():
                        success, frame = cap.read()
                
                        # Recolour image from BGR to RGB 
                        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        image.flags.writeable = False  # make pixel arrays read-only to detect image (saves disk memory)
                
                        # Detect image 
                        results = pose.process(image)
                
                        # Recolour image from RGB to BGR again
                        image.flags.writeable = True    # Make pixel arrays writable (editable) to revert from RGB to BGR
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        image = cv2.resize(image, (1280, 720))
                
                        # Extract landmarks by collecting x,y coordinates for useful body joints
                        try:
                            landmarks = results.pose_landmarks.landmark
                
                            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
                            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
                            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
                            
                            angle = calculate_high_knee_angle(shoulder, hip, knee)
                
                            # Display angles in images 
                            cv2.putText(image, str(angle),
                                        tuple(np.multiply(hip, [640, 480]).astype(int)),
                                        font, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                        )
                
                            # Count the number of high_knees
                            if angle > 120:  # if angle is greater than 160...
                                high_knee_position = "down"  # ... then arm position is down
                
                            if angle < 70 and high_knee_position == "down":  # if angle is less than 30 and arm position is down...
                                high_knee_position = "up"  # ...record arm position as up...
                                counter += 1  # ...and add one rep to the total reps ...
                                print(counter)  # ... and display total counts
                
                        except:
                            pass
                
                        # Create progress tracking box at the top left of the screen  
                        # '''Rectangle 1 '''
                
                        rect1_starting_point = (0, 0)
                        rect1_ending_point = (370, 82)
                        rect1_colour = (245, 117, 16)
                        rect1_thickness = -1
                
                        cv2.rectangle(image,
                                    rect1_starting_point,  # starting point
                                    rect1_ending_point,  # ending point
                                    rect1_colour,  # box colour
                                    rect1_thickness)  # thickness
                
                        # Add 'WORKOUT' title to rectangle
                
                        rect1_title = 'WORKOUT'
                        rect1_title_text_org = (15, 12)
                        rect1_title_font = font
                        rect1_title_font_scale = 0.5
                        rect1_title_colour = (0, 0, 0)
                        rect1_title_text_thickness = 1
                        rect1_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect1_title,
                                    rect1_title_text_org,
                                    rect1_title_font,
                                    rect1_title_font_scale,
                                    rect1_title_colour,
                                    rect1_title_text_thickness,
                                    rect1_title_line_type)
                
                        # Add workout type
                
                        rect1_body = 'High Knees'
                        rect1_body_text_org = (10, 65)
                        rect1_body_font = font
                        rect1_body_font_scale = 2
                        rect1_body_colour = (255, 255, 255)
                        rect1_body_text_thickness = 2
                        rect1_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect1_body,
                                    rect1_body_text_org,
                                    rect1_body_font,
                                    rect1_body_font_scale,
                                    rect1_body_colour,
                                    rect1_body_text_thickness,
                                    rect1_body_line_type)
                
                        # '''Rectangle 2 '''
                
                        rect2_starting_point = (1000, 82)
                        rect2_ending_point = (1400, 0)
                        rect2_colour = (100, 255, 50)
                        rect2_thickness = -1
                
                        cv2.rectangle(image,
                                    rect2_starting_point,  # starting point (top left corner)
                                    rect2_ending_point,  # ending point (bottom right corner)
                                    rect2_colour,
                                    rect2_thickness
                                    )
                
                        # Add reps total  
                
                        rect2a_title = 'REPS'
                        rect2a_title_text_org = (1016, 12)
                        rect2a_title_font = font
                        rect2a_title_font_scale = 0.5
                        rect2a_title_colour = (0, 0, 0)
                        rect2a_title_text_thickness = 1
                        rect2a_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2a_title,
                                    rect2a_title_text_org,
                                    rect2a_title_font,
                                    rect2a_title_font_scale,
                                    rect2a_title_colour,
                                    rect2a_title_text_thickness,
                                    rect2a_title_line_type)
                
                        rect2a_body = str(counter)
                        rect2a_body_text_org = (1016, 64)
                        rect2a_body_font = font
                        rect2a_body_font_scale = 2
                        rect2a_body_colour = (255, 255, 255)
                        rect2a_body_text_thickness = 2
                        rect2a_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2a_body,
                                    rect2a_body_text_org,
                                    rect2a_body_font,
                                    rect2a_body_font_scale,
                                    rect2a_body_colour,
                                    rect2a_body_text_thickness,
                                    rect2a_body_line_type)
                
                        # Add arm position     
                
                        rect2b_title = 'LEG POSITION'
                        rect2b_title_text_org = (1122, 12)
                        rect2b_title_font = font
                        rect2b_title_font_scale = 0.5
                        rect2b_title_colour = (0, 0, 0)
                        rect2b_title_text_thickness = 1
                        rect2b_title_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2b_title,
                                    rect2b_title_text_org,
                                    rect2b_title_font,
                                    rect2b_title_font_scale,
                                    rect2b_title_colour,
                                    rect2b_title_text_thickness,
                                    rect2b_title_line_type)
                
                        rect2b_body = str(high_knee_position)
                        rect2b_body_text_org = (1122, 64)
                        rect2b_body_font = font
                        rect2b_body_font_scale = 2
                        rect2b_body_colour = (255, 255, 255)
                        rect2b_body_text_thickness = 2
                        rect2b_body_line_type = cv2.LINE_AA
                
                        cv2.putText(image,
                                    rect2b_body,
                                    rect2b_body_text_org,
                                    rect2b_body_font,
                                    rect2b_body_font_scale,
                                    rect2b_body_colour,
                                    rect2b_body_text_thickness,
                                    rect2b_body_line_type)
                
                        # Use model to identify landmarks in the image 
                        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                                mp_drawing.DrawingSpec(color=(164, 66, 22), thickness=6, circle_radius=7)
                                                )
                
                        cv2.imread('AI Personal Trainer', image)                
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                        # run == False

                
                cap.release()
                cv2.destroyAllWindows()
                





else:
    st.write('*So...have you decided on what workout you want or?????*')

st.write('---------------')
# st.text(" How do you grow muscles?")

# st.text(" 1. Avoid ego lifting - master technique using lighter weights ")
# st.text("2. Focus on time over tension/resistance")
# st.text("3. ")


with st.container():
    st.markdown(
        """ **Disclaimer: The information provided on this app should not be considered as professional, medical or health advice (these are strictly the opinions of the developer) - please seek your doctor's recommendations for professional advice on your health situation or read at your own discretion.** """)
    column1, column2, column3 = st.columns(3)
    with column1:
        st.subheader("1. What are your fitness goals?")
        fitness_goal = st.radio("Pick one ",
                                ("None", "Increasing muscle mass",
                                 "Losing body fat/weight", "Maintaining my current shape or physique"))
        st.text("")
        st.text("")
        st.text("")
        st.subheader("2. How is your current diet? ")
        meal_plan = st.radio("Pick one ",
                             ("None", "Great! Most of my meals contain the nutrients that meet my fitness goals",
                              "Alright - my meals are relatively healthy but I could improve",
                              "Not good - most of my meals are not rich in nutritional content..."))
    with column2:
        if fitness_goal == "None":
            lottie_animation = load_animation_via_link("https://assets3.lottiefiles.com/packages/lf20_wGsXfA.json")
            st_lottie(lottie_animation, height=300, width=300, key="muscle_growth")
        if fitness_goal == "Increasing muscle mass":
            lottie_animation = load_animation_via_link("https://assets10.lottiefiles.com/packages/lf20_kmj1m9xh.json")
            st_lottie(lottie_animation, height=300, width=300, key="muscle_growth")
        if fitness_goal == "Losing body fat/weight":
            lottie_animation = load_animation_via_link("https://assets10.lottiefiles.com/packages/lf20_xfhjdjbn.json")
            st_lottie(lottie_animation, height=300, width=300, key="lose_fat")
        if fitness_goal == "Maintaining my current shape or physique":
            lottie_animation = load_animation_via_link(
                "https://assets1.lottiefiles.com/private_files/lf30_zumhi5up.json")
            st_lottie(lottie_animation, height=300, width=300, key="maintain_physique")

        if meal_plan == "None":
            pass
        if meal_plan == "Great! Most of my meals contain the nutrients that meet my fitness goals":
            st.markdown(""" 
            Excellent! Keep it up!
            """)
            st.markdown(""" 
             Staying consistent is the hardest part - aim to turn your diet into a way of life - that's where the results show up :raised_hands: :100: 
            """)

        if meal_plan == "Alright - my meals are relatively healthy but I could improve":
            st.markdown(""" 
            
            Eating the right meals occassionally is a good start :white_check_mark:- 

            * Try some options recommended under "Increasing body mass" or "Losing body fat/weight" options under question 1
            * Start the food selections you've picked slow and small to form a habit e.g. fish and rice for lunch daily for two weeks 
            * Gradually increase your range of selection after you've formed a meal prep routine e.g. add fruit salad to compliment your fish and rice lunch meals after week 3
             
            """)

        if meal_plan == "Not good - most of my meals are not rich in nutritional content...":
            st.markdown(""" 
            As the old Chinese proverb says, 

            " :palm_tree: The best time to plant a tree was 20 years ago. The second best time is now! :palm_tree:"
            
            Here are a few suggestions to kick-start a better meal plan: 
            * Try increasing your protein and fibre intake gradually
            * Consider food supplements 
            * Have a calories intake goal you'd like to reach
            """)
    with column3:

        if fitness_goal == "Increasing muscle mass":
            st.header("Maximizing Muscle Growth ")
            st.subheader("*How do you stimulate healthy growth in muscle mass?* ")
            st.markdown("""                



            * Workouts: Prioritize free weights and machine workouts more 
            * Workout ratio: 60% weights, 20% stretching, 20% cardio  
            * Food: 
            * Meal plans: Eat carbs after workout, include protein with vegetables in all your meals (40% fruit & vegs, 30% protein, 20% healthy fats, 10% fibre)
            * Science: Consume lots of carbs to fuel your workouts and plenty of protein + healthy fats to fuel muscle development 




             """)
            st.subheader("*Top muscle-development tips* ")
            st.markdown("""                
            * Technique first, weights after - avoid ego lifting by respecting your current limits - focus on mastering workout form with lighter weights first and increase weight size once you're comfortable 
            * Focus on time over tension/resistance
            * Rest between sets for at least 2-3 mins - don't set yourself up for failure for the next set
            * Don't skip leg day - no seriously...work on your legs more - you release testosterone & growth hormones the more you work them out
            * Use free weights when you're full of energy and machines when you're fatigue
            * If you're low on motivation, focus on doing a little - a little is better than nothing

             """)

            st.text("")
            st.text("")
            st.text("")

        if fitness_goal == "Losing body fat/weight":
            st.header("Burning fat ")
            # st.write("##")

            st.subheader("*How do you lose fat?* ")
            st.markdown("""                
            * Workouts: Focus on HIIT workouts more e.g. 100m sprints, shadow boxing
            * Workout ratio: (40% HIITs, 30% weights, 20% stretching, 10% machines)
            * Food: Salmon, avocado, nuts, chicken, almonds, sardines, eggs, greek yoghurt, and more
            * Meal plans: Eat more protein than carbs (70% protein, 20% fibre, 10% carbs) e.g. consider keto-diet 
            * Science: Burn more than you eat e.g. consider intermittent fasting, 36-hours water fast

             """)

            st.subheader("*Top fat-burning workouts* ")
            st.markdown("""                
            Start with these for 30-45 secs per rep:

            * Skipping/jogging on the spot 
            * Jumping jacks
            * Hill sprints

             """)
            st.subheader("Conclusion?")
            st.markdown("""                
            
            Stay in calorie deficit as long as possible (in a sustainably healthy manner) - this is when you are burning more calories than you are digesting. 

            As long as you are burning more calories than you digest, you will always lose fat. 
            
             """)
        if fitness_goal == "Maintaining my current shape or physique":
            st.header("Maintaining current physique ")
            # st.write("##")

            st.subheader("*How do you keep what you're happy with already?* ")
            st.markdown("""                
            * Workouts: A regular workout routine on moderate pace should be enough 
            * Workout ratio: (30% cardio, 20% weights, 30% stretching, 10% machines)
            * Food: Meals and snacks that contain fruit, veg, protein, fibre, healthy fats, 
            * Meal plans: Explore new dishes that touch on each of the regular nutrient intake you require   
            * Science: Enjoy the exploration process! Life is about expanding your horizons 

             """)

            # st.subheader("*Top fat-burning workouts* ")
            # st.markdown("""                
            # Start with these for 30-45 secs per rep:

            # * Skipping/jogging on the spot 
            # * Jumping jacks
            # * Hill sprints

            #  """)
            # st.subheader("Conclusion?")
            # st.markdown("""                

            # Stay in calorie deficit as long as possible (in a sustainably healthy manner) - this is when you are burning more calories than you are digesting. 

            # As long as you are burning more calories than you digest, you will always lose fat. 

            #  """)

st.text("")
st.text("")
st.text("")

# with st.container():
#     st.header("Burning fat ")
#     st.write("##")
#     st.subheader("*How do you lose fat?* ")
#     st.markdown("""                

#     * Burn more than you eat 
#     * Eat more protein than carbs
#     * Focus on HIITs more !   

#      """)

st.write("----------")
st.header("Development Plans :wrench:")
with st.container():
    columnL, columnR = st.columns(2)
    with columnL:
        st.markdown(
            """
        This is the 1st version of my AI Personal Trainer so there are inevitable issues you may come across when navigating through this. 

        I'm currently utilizing this to aid my fitness journey when working out from home, but I'm interested in knowing your honest thoughts and opinions on this current release so that I can further enhance the user experience on this. 
         
      
        Any suggestions to improving this app is welcome, so let me know your thoughts - feel free to contact me on:

        * [LinkedIn](https://www.linkedin.com/in/stephen-david-williams-860428123/)
        * [Gmail](mailto:stephenodavidwilliams@gmail.com) 

        
        """)
    with columnR:
        lottie_animation = load_animation_via_link("https://assets7.lottiefiles.com/packages/lf20_xh83pj1c.json")
        st_lottie(lottie_animation, height=400, width=700, key="ai_robot2")

contact_doc = """

<form action="https://formsubmit.co/stephenodavidwilliams@gmail.com" method="POST">
     <input type="hidden" name="_capcha" value="false">
     <input type="text" name ="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here" required></textarea>
     <button type="submit">Send</button>
</form>

"""

columnL, columnR = st.columns(2)
with st.container():
    with columnL:
        st.markdown("""
        Alternatively you can use the contact form below to fast-track your messages to me too 

        """)
        st.header("Contact Me :email:")
        st.markdown(contact_doc, unsafe_allow_html=True)
    with columnR:
        st.empty()

st.markdown("""---------""")
st.markdown("""""")

# st.sidebar.title("Contact Me")
# st.sidebar.info("""
# Feel free to reach out to me on:

# * [LinkedIn](https://www.linkedin.com/in/stephen-david-williams-860428123/)
# * [Gmail](mailto:stephenodavidwilliams@gmail.com)


# """)

style_contact_doc("style.css")
