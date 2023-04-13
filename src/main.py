import streamlit as st
import streamlit.components.v1 as stc
import time
from pathlib import Path

# File Processing Pkgs
import pandas as pd
from io import BytesIO,StringIO
from PIL import Image 



def main():
    st.title("Phần mềm nhận dạng các loại nho")
    col1, col2 = st.columns([3, 1], gap="medium")
    with col2:
        st.image(image = Image.open('logo.png'), width=140)
    with col1:
        st.write(
            """
        Thành viên:
        - Phan Đại Đăng Khoa
        - Nguyễn Trường Phúc
        """)
    file = st.file_uploader("Upload file",type=["png","jpg"])
    show_file = st.empty()

    if not file:
          show_file.info("Please Upload a file: {}".format(' '.join(["png","jpg"])))
          return
    content = file.getvalue()

    if isinstance(file, BytesIO):
        show_file.image(file)
        if st.button('Bắt đầu nhận dạng'):
            progress_text = "Operation in progress. Please wait."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.1)
                my_bar.progress(percent_complete + 1, text=progress_text)
            st.success('Đây là loại nho....')        
    else:
          df = pd.read_csv(file)
          st.dataframe(df.head(2))
    file.close()


if __name__ == '__main__':
	main()