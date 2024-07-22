import streamlit as st
import tensorflow as tf
import numpy as np
import time

# Load the model and labels
model = tf.keras.models.load_model("trained_model2.h5")
with open("label.txt") as f:
    labels = f.readlines()

def model_prediction(test_image):
    image = tf.keras.preprocessing.image.load_img(test_image, target_size=(64, 64))
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])  # Convert single image to batch
    predictions = model.predict(input_arr)
    return np.argmax(predictions)  # Return index of max element

# Sidebar
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Prediction"])

# Main Page
if app_mode == "Home":
    st.header("FRUITS CLASSIFICATION SYSTEM (Fruty)")
    image_path = 'home_img.jpg'
    st.image(image_path)

# About Project
elif app_mode == "About Project":
    st.header("About Project")
    st.text("Welcome to Fruit Classification Project named Fruty, where passion meets purpose, and learning\ntranscends boundaries. Our project is not just a culmination of academic endeavors,\nit is a celebration of creativity, collaboration, and the pursuit of knowledge.")
    st.text("We strive to create an atmosphere where curiosity is not just welcomed but celebrated,\nand where students can transform challenges into opportunities for growth.")
    st.text("This is a machine learning model created as an class project to learn the basic\nconcept of machine learning that can accurately classify whether the given image\nis of fruits or not. The model will be trained on a dataset containing labelled\nimages of various fruits, and its performance will be evaluated on a test set to \nassess its classification accuracy.")
    st.text(" The model architecture is Convolutional Neural Network(CNN).\nThis model is using a deep learning framework TensorFlow")
    st.subheader("About Us")
    st.text("This project is made by:")
    st.code("Avinash Verma, 2K22/SE/36\nDeepak Kumar, 2K22/SE/54")
    st.text("Under The Supervision Of:")
    st.code("M/s Shweta Meena Mam\nM/s Anjali Bansal Mam")
    st.subheader("About Dataset")
    st.text("This dataset contains images of the following food items:")
    st.code("Fruits- Banana, Apple, Pear, Grapes, Orange, Kiwi, Watermelon, Pomegranate, Pineapple, Mango, Cucumber, Bell Pepper, Corn, Eggplant, Tomato.")
    st.code("Vegetables- Carrot, Capsicum, Onion, Potato, Lemon, Raddish, Beetroot, Cabbage, Lettuce, Spinach, Soybean, Cauliflower, Chilli Pepper, Turnip, Sweetcorn, Sweet Potato, Paprika, Jalepeño, Ginger, Garlic, Peas.")
    st.subheader("Content")
    st.text("Dataset contains three folders:")
    st.text("1. train (100 images each)")
    st.text("2. test (10 images each)")
    st.text("3. validation (10 images each)")

# Prediction Page
elif app_mode == "Prediction":
    st.header("Model Prediction")
    test_image = st.file_uploader("Choose an Image:")
    
    if test_image is not None:
        if(st.button("Show Image")):
            st.image(test_image,width=4,use_column_width=True)
        
        # Predict button
        if st.button("Predict"):
            with st.spinner("Predicting..."):
                time.sleep(2)
            st.balloons()
            st.write("Model Prediction")
            result_index = model_prediction(test_image)
            predicted_label = labels[result_index].strip()
            
            # Determine if it's a fruit or not
            is_fruit = predicted_label in ["banana", "apple", "pear", "grapes", "orange", "kiwi", "watermelon", "pomegranate", "pineapple", "mango", "eggplant", "cucumber", "corn", "bell pepper", "tomato"]
            if is_fruit:
                st.success(f"Model Prediction: It's a Fruit ({predicted_label})")
            else:
                st.success("Model Prediction: It's not a Fruit")