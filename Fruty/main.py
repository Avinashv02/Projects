import streamlit as st
import tensorflow as tf
import numpy as np
import time
import os

# Load the model and labels with error handling
@st.cache_resource
def load_model_and_labels():
    try:
        model = tf.keras.models.load_model("Fruty/fruits.h5")
        with open("label.txt", "r") as f:
            labels = [label.strip().lower() for label in f.readlines()]
        return model, labels
    except Exception as e:
        st.error(f"Error loading model or labels: {e}")
        return None, None

model, labels = load_model_and_labels()

def model_prediction(test_image):
    if model is None:
        return None
    try:
        image = tf.keras.preprocessing.image.load_img(test_image, target_size=(64, 64))
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([input_arr])  # Convert single image to batch
        predictions = model.predict(input_arr)
        return np.argmax(predictions)  # Return index of max element
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None

# Sidebar
st.sidebar.title("Dashboard")
app_mode = st.sidebar.selectbox("Select Page", ["Home", "About Project", "Prediction"])

# Main Page
if app_mode == "Home":
    st.header("FRUITS CLASSIFICATION SYSTEM (Fruty)")
    image_path = 'home_img.jpg'
    
    # Check if image exists before displaying
    if os.path.exists(image_path):
        st.image(image_path)
    else:
        st.warning("Home image not found. Please add 'home_img.jpg' to your directory.")

# About Project
elif app_mode == "About Project":
    st.header("About Project")
    st.text("Welcome to Fruit Classification Project named Fruty, where passion meets purpose, and learning\ntranscends boundaries. Our project is not just a culmination of academic endeavors,\nit is a celebration of creativity, collaboration, and the pursuit of knowledge.")
    st.text("We strive to create an atmosphere where curiosity is not just welcomed but celebrated,\nand where students can transform challenges into opportunities for growth.")
    st.text("This is a machine learning model created as a class project to learn the basic\nconcept of machine learning that can accurately classify whether the given image\nis of fruits or not. The model will be trained on a dataset containing labelled\nimages of various fruits, and its performance will be evaluated on a test set to \nassess its classification accuracy.")
    st.text("The model architecture is Convolutional Neural Network(CNN).\nThis model is using a deep learning framework TensorFlow")
    st.subheader("About Us")
    st.text("This project is made by:")
    st.code("Avinash Verma, 2K22/SE/36\nDeepak Kumar, 2K22/SE/54")
    st.text("Under The Supervision Of:")
    st.code("M/s Shweta Meena Mam\nM/s Anjali Bansal Mam")
    st.subheader("About Dataset")
    st.text("This dataset contains images of the following food items:")
    st.code("Fruits- Banana, Apple, Pear, Grapes, Orange, Kiwi, Watermelon, Pomegranate, Pineapple, Mango")
    st.code("Vegetables- Cucumber, Bell Pepper, Corn, Eggplant, Tomato, Carrot, Capsicum, Onion, Potato, Lemon, Radish, Beetroot, Cabbage, Lettuce, Spinach, Soybean, Cauliflower, Chilli Pepper, Turnip, Sweetcorn, Sweet Potato, Paprika, Jalapeño, Ginger, Garlic, Peas")
    st.subheader("Content")
    st.text("Dataset contains three folders:")
    st.text("1. train (100 images each)")
    st.text("2. test (10 images each)")
    st.text("3. validation (10 images each)")

# Prediction Page
elif app_mode == "Prediction":
    st.header("Model Prediction")
    
    if model is None or labels is None:
        st.error("Model or labels failed to load. Please check your files.")
    else:
        test_image = st.file_uploader("Choose an Image:", type=['jpg', 'jpeg', 'png'])
        
        if test_image is not None:
            if st.button("Show Image"):
                st.image(test_image, use_column_width=True)
            
            # Predict button
            if st.button("Predict"):
                with st.spinner("Predicting..."):
                    time.sleep(2)
                st.balloons()
                st.write("Model Prediction")
                result_index = model_prediction(test_image)
                
                if result_index is not None and result_index < len(labels):
                    predicted_label = labels[result_index]
                    
                    # Define fruits correctly (botanically accurate)
                    fruits = ["banana", "apple", "pear", "grapes", "orange", "kiwi", 
                             "watermelon", "pomegranate", "pineapple", "mango", "kiwi", "tomato"]
                    
                    if predicted_label in fruits:
                        st.success(f"Model Prediction: It's a Fruit ({predicted_label.title()})")
                    else:
                        st.success(f"Model Prediction: It's not a Fruit (It's {predicted_label.title()})")
                else:
                    st.error("Prediction failed. Please try again.")
