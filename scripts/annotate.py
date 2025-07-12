import streamlit as st
import os
import json
from PIL import Image
import cv2
import numpy as np

# 🔧 Get absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
SAVE_FOLDER = os.path.join(BASE_DIR, "annotations")

st.title("📌 Image Annotation Tool")

# DEBUG INFO
st.sidebar.title("🛠 Debug Info")
st.sidebar.write(f"Image folder: {IMAGE_FOLDER}")
st.sidebar.write(f"Save folder: {SAVE_FOLDER}")

# CHECK IMAGE FOLDER EXISTS
if not os.path.exists(IMAGE_FOLDER):
    st.error(f"🚫 Folder not found: {IMAGE_FOLDER}")
    st.stop()

images = [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.png', '.jpg', '.jpeg'))]

if not images:
    st.error("⚠️ No images found in the 'images/' folder. Please add some .jpg or .png files.")
    st.stop()

# IMAGE SELECT DROPDOWN
selected_img = st.selectbox("Select an image", images)

if selected_img:
    img_path = os.path.join(IMAGE_FOLDER, selected_img)
    img = Image.open(img_path)
    st.image(img, caption="Selected Image", use_column_width=True)

    st.subheader("🔖 Annotation Input")
    label = st.text_input("Label", "object")
    x = st.number_input("X (top left)", 0)
    y = st.number_input("Y (top left)", 0)
    w = st.number_input("Width", 10)
    h = st.number_input("Height", 10)

    # ✅ Draw bounding box + label on image before saving
    if w > 0 and h > 0 and label:
        img_cv = cv2.imread(img_path)
        if img_cv is not None:
            img_cv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
            start_point = (int(x), int(y))
            end_point = (int(x + w), int(y + h))

            # Draw bounding box
            cv2.rectangle(img_cv, start_point, end_point, (0, 255, 0), 2)

            # Draw label above box
            label_position = (int(x), int(y) - 10)
            cv2.putText(img_cv, label, label_position,
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.8,
                        color=(255, 0, 0),
                        thickness=2)

            # Display image
            st.image(img_cv, caption="With Bounding Box + Label", use_column_width=True)
        else:
            st.error("❌ Could not read the image using OpenCV.")

    if st.button("💾 Save Annotation"):
        os.makedirs(SAVE_FOLDER, exist_ok=True)
        data = {
            "image": selected_img,
            "label": label,
            "bbox": [int(x), int(y), int(w), int(h)]
        }
        save_path = os.path.join(SAVE_FOLDER, f"{selected_img}.json")
        with open(save_path, "w") as f:
            json.dump(data, f, indent=2)

        st.success(f"✅ Annotation saved to {save_path}")
