import streamlit as st
from PIL import Image
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np
from keras.models import load_model
import requests
from bs4 import BeautifulSoup

model = load_model('models.h5')
labels = {0: 'champagne', 1: 'cotton candy', 2: 'crimson seedless', 3: 'gewurztraminer', 4: 'glenora', 5: 'kyoho'
          }





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


def run():
    st.set_page_config(
    page_title="Nhận Dạng Các Loại Nho",
    page_icon=":grapes:",
    layout="wide",)
    c1,c2 = st.columns([1,8])
    with c2:
        image = Image.open('logo2.png')    
        st.image(image,width=1000)

    col1,col2 = st.columns([1, 3])
    with col2:
         st.title("NHẬN DẠNG CÁC LOẠI NHO :grapes:")
    st.text("""
    - Phan Đại Đăng Khoa
    - Nguyễn Trường Phúc
    """)
    
    img_file = st.file_uploader("Choose an Image", type=["jpg", "png"])
    if img_file is not None:
        img = Image.open(img_file).resize((250, 250))
        st.image(img, use_column_width=False)
        save_image_path = './upload_images/' + img_file.name
        with open(save_image_path, "wb") as f:
            f.write(img_file.getbuffer())

        # if st.button("Predict"):
        if img_file is not None:
            result = processed_img(save_image_path)
            print(result)
            st.success("**Predicted : " + result + '**')
            
        


run()