import streamlit as st
import streamlit.components.v1 as components
from functions import *
import base64
from PIL import Image
import io

st.set_page_config(layout="wide")

html_code = f"""
<head>
    <style>@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap')</style>
</head>
<body>
    <div style="text-align: center">
        <h1 style="font-family: Raleway;">ORGANIC GRIDS</h1>
    </div>
"""
components.html(html_code, height=60)



with st.container():

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col2: rows = st.number_input(label="Number of rows", min_value=1, max_value=10, value=4)

    with col2: transition_size = st.slider(label="Transition size", min_value=0.1, max_value=10.0, value=2.0, step=0.1)

    with col3: cols = st.number_input(label="Number of columns", min_value=1, max_value=10, value=4, step=1)

    with col3: transition_speed = st.slider(label="Transition speed", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    transition_speed = 1 / transition_speed


with st.container():

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        # Upload image file
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])


with st.container():

        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.read()
            
            # Convert bytes data to an image
            image = Image.open(io.BytesIO(bytes_data))
            img_name = uploaded_file.name.split('.')[0]

            # Create a directory to save the uploaded file
            save_dir = f'../files/{img_name}-{rows}-{cols}'
            os.makedirs(save_dir, exist_ok=True)

            # Save the file
            save_path = os.path.join(save_dir, uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(bytes_data)

            split_uploaded_image(uploaded_file.name, rows, cols)
            html_code = create_html_with_style(uploaded_file.name, rows, cols, transition_speed, transition_size)
            components.html("", height=30)
            components.html(html_code, height=600)