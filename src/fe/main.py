import cv2
from io import BytesIO
import streamlit as st
from PIL import Image
from rembg import remove
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
import requests
from bs4 import BeautifulSoup
import time

model = load_model('models.h5')
labels = {0: 'champagne', 1: 'cotton candy', 2: 'crimson seedless', 3: 'gewurztraminer', 4: 'glenora', 5: 'kyoho'}

def getInfor(prediction):
     # Đường dẫn tới file text
    file_path =  prediction+".txt"

    # Mở file và đọc nội dung của nó
    with open(file_path, "r",encoding="utf-8") as f:
        content = f.read()
    return content


def processed_img(img_path):
    img = load_img(img_path, target_size=(100, 100, 3))
    img = img_to_array(img)
    img = img / 255
    img = np.expand_dims(img, [0])
    answer = model.predict(img)
    answer2 = answer[0]
    y_class = answer.argmax(axis=-1)
    array = np.asarray(answer2)
    idx = (np.abs(array-1)).argmin()
    acc = array[idx]
    print(y_class)
    y = " ".join(str(x) for x in y_class)
    y = int(y)
    res = labels[y]
    print(res)
    print(acc)
    return res.capitalize()



st.set_page_config(
    page_title="Nhận Dạng Các Loại Nho",
    page_icon=":grapes:",
    layout="wide",)


image = Image.open('logo2.png')    
st.image(image,width=900)

st.title("NHẬN DẠNG CÁC LOẠI NHO :grapes::grapes::grapes:")


st.sidebar.write("""
    # Nhóm 6:
    - Phan Đại Đăng Khoa
    - Nguyễn Trường Phúc
    """)
st.sidebar.write("## Choose an Image :gear:")

# Create the columns
col1, col2 = st.columns(2)

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# Package the transform into a function
def fix_image(upload):
    image = Image.open(upload)
    col1.write("Original Image :camera:")
    col1.image(image)

    fixed = remove(image)
    col2.write("Fixed Image :wrench:")
    col2.image(fixed)
    st.sidebar.download_button(
        "Download fixed image", convert_image(fixed), "fixed.png", "image/png"
    )

# Create the file uploader
my_upload = st.sidebar.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if my_upload is not None:
        img_out = fix_image(my_upload)
        save_image_path = './upload_images/' + my_upload.name
        with open(save_image_path, "wb") as f:
            f.write(my_upload.getbuffer())

# Fix the image!
if my_upload is not None:
    result = processed_img(save_image_path)
    print(result)
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
      
    st.success("**Predicted : " + result + '**')
    st.warning(getInfor(result))
