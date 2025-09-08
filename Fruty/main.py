import tensorflow as tf
import numpy as np
import time
import os
import streamlit as st
from PIL import Image
import io

# Load Model and Labels
model = tf.keras.models.load_model("Fruty/trained_model2.h5")
with open("Fruty/label.txt") as f:
    labels = f.readlines()
    
# ---------------------------
# Prediction Function
# ---------------------------
def model_prediction(test_image):
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(64, 64))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # Return index of max element


# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Prediction"])

# ---------------------------
# Home Page
# ---------------------------
if app_mode == "Home":
    st.header("🍎 Fruits Classification System (Fruty)")
    st.image("Fruty/home_img.jpg", width=True)
    st.markdown(
        """
        ### Welcome to **Fruty** 🍌🍇🍊  
        This app can classify an uploaded image into **fruit** or **not a fruit**  
        using a Convolutional Neural Network (CNN) trained on fruit & vegetable datasets.
        """
    )

# ---------------------------
# About Project Page
# ---------------------------
elif app_mode == "About Project":
    st.header("📜 About Project")
    st.write(
        """
        **Fruty** is a Machine Learning project developed to classify images  
        as fruits or vegetables using a Convolutional Neural Network (CNN) built with TensorFlow.
        
        - **Purpose:** Learn ML concepts and image classification basics.  
        - **Dataset:** Contains labeled images of various fruits and vegetables.  
        - **Framework:** TensorFlow/Keras  
        - **Model:** CNN architecture
        """
    )

    st.subheader("👨‍💻 Team Members")
    st.code("Avinash Verma, 2K22/SE/36\nDeepak Kumar, 2K22/SE/54")
    st.subheader("👩‍🏫 Supervisors")
    st.code("M/s Shweta Meena Mam\nM/s Anjali Bansal Mam")

    st.subheader("📦 Dataset Details")
    st.markdown(
        """
        **Fruits:** Banana, Apple, Pear, Grapes, Orange, Kiwi, Watermelon,  
        Pomegranate, Pineapple, Mango, Cucumber, Bell Pepper, Corn, Eggplant, Tomato.  

        **Vegetables:** Carrot, Capsicum, Onion, Potato, Lemon, Raddish, Beetroot,  
        Cabbage, Lettuce, Spinach, Soybean, Cauliflower, Chilli Pepper, Turnip,  
        Sweetcorn, Sweet Potato, Paprika, Jalepeño, Ginger, Garlic, Peas.  

        **Dataset Structure:**
        - `train` (100 images each)
        - `test` (10 images each)
        - `validation` (10 images each)
        """
    )

# ---------------------------
# Prediction Page
# ---------------------------
elif app_mode == "Prediction":
    st.header("🔍 Model Prediction")
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

        if st.button("Predict"):
            with st.spinner("Analyzing Image..."):
                time.sleep(1.5)
                result_index = model_prediction(uploaded_file)
                predicted_label = labels[result_index]

                # Fruits list for classification
                fruits_list = [
                    "banana", "apple", "pear", "grapes", "orange", "kiwi", "watermelon",
                    "pomegranate", "pineapple", "mango", "eggplant", "cucumber", "corn",
                    "bell pepper", "tomato"
                ]

                if predicted_label in fruits_list:
                    st.success(f"🍎 It's a Fruit! **({predicted_label.capitalize()})**")
                else:
                    st.warning(f"🥦 It's NOT a Fruit! Detected: **{predicted_label.capitalize()}**")

            st.balloons()







