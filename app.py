import streamlit as st
import streamlit.components.v1 as components
from functions import *
from PIL import Image
import base64
import io
import requests
import os

st.set_page_config(page_title='Organic Grids Generator', layout="wide")

html_code = """
<head>
    <style>@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');
    body {
        font-family: Raleway;
    }
    a:link, a:visited {
        color: #FF4B4B;
        text-decoration: None;
    }

    a:link:active, a:visited:active {
        color: black;
    }
    </style>
</head>
<body>
    <div style="text-align: center">
        <h1 style="margin-bottom: 0;">ORGANIC GRIDS GENERATOR</h1>
        <p style="margin-top: 5px; margin-bottom: 0px">based on an experiment by digital artist <a href="https://nahuelgerth.de/" target="_blank" rel="noopener noreferrer">Nahuel Gerth</a></p>
    </div>
</body>
"""
components.html(html_code, height=85)



css_streamlit = '''
<style>
    [data-testid='stFileUploader'] {
        width: max-content;
    }
    [data-testid='stFileUploader'] section {
        padding: 0;
        float: right;
    }
    [data-testid='stFileUploader'] section > input + div {
        display: none;
    }
    [data-testid='stFileUploader'] section + div {
        float: right;
        padding-top: 0;
    }
    .block-container {
        padding-top: 5vh;
        padding-bottom: 0rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
</style>
'''

st.markdown(css_streamlit, unsafe_allow_html=True)

st.markdown("""
        <style>

        </style>
        """, unsafe_allow_html=True)



# Create widgets to specify grid properties by user input
with st.container():
    col1, col2, col3 = st.columns([1, 4, 1])

    with col1: rows = st.number_input(label="Number of rows", min_value=1, max_value=15, value=5, step=1)
    with col1: cols = st.number_input(label="Number of columns", min_value=1, max_value=15, value=8, step=1)
    with col1: grid_gap_width = st.number_input(label="Grid gap width", min_value=0, max_value=10, value=2, step=1)
    with col1: components.html("", height=0)
    with col1: transition_size = st.slider(label="Transition size", min_value=0.1, max_value=10.0, value=2.5, step=0.1)
    with col1: transition_speed_in = st.slider(label="Transition speed in", min_value=0.1, max_value=3.0, value=1.5, step=0.1)
    transition_speed_in = 1 / (transition_speed_in)**2
    with col1: transition_speed_out = st.slider(label="Transition speed out", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
    transition_speed_out = 1 / (transition_speed_out)**2


    with col3: uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key='image_uploaded')
    with col3:
        if st.button('New random photo'):
            if 'image_fetched' in st.session_state:
                del st.session_state['image_fetched']
            if "image_uploaded" in st.session_state:
                del st.session_state['image_uploaded']
            st.rerun()


    with col2:

        # Set grid properties if no user input
        if rows is None:
            rows = 4
            cols = 6
            transition_size = 2.5
            transition_speed = 1 / 2.5

        # Disply image in grid
        if uploaded_image is None:
            #url = "https://images.unsplash.com/photo-1573147367786-a5a227916f0c?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
            
            if 'image_fetched' not in st.session_state:
                url = "https://picsum.photos/800/600"
                img_bytes, img_type = fetch_image_from_url(url)
                bytes_data = img_bytes.read()
                st.session_state['image_fetched'] = True
                st.session_state['image_bytes_data'] = bytes_data
                st.session_state['image_type'] = img_type
            else:
                bytes_data = st.session_state['image_bytes_data']
                img_type = st.session_state['image_type']
            
        else:
            bytes_data = uploaded_image.read()
            img_type = uploaded_image.name.split('.')[1]

        # Convert bytes to image
        img = Image.open(io.BytesIO(bytes_data))
        img_width, img_height = img.size

        html_output = split_image_and_create_html_output(img, img_type, rows, cols, transition_speed_in, transition_speed_out, transition_size, grid_gap_width)

        display_height = 800 * img_height / img_width
        components.html(html_output, height=display_height)


with st.container():

    footer_html="""
    <head>
    <style>@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap');
    body {
        font-family: Raleway;
    }
    a:link, a:visited {
        color: #FF4B4B;
        text-decoration: None;
    }
    a:link:active, a:visited:active {
        color: black;
    }
    </style>
    </head>
    <body>
        <div style="text-align: center">
            <br>
            <br>
            <p>Random photos fetched from <a href="https://unsplash.com/" target="_blank" rel="noopener noreferrer">Unsplash</a> via <a href="https://picsum.photos/" target="_blank" rel="noopener noreferrer">Lorem Picsum</a>.</p>
        </div>
    </body>
    """

    components.html(footer_html, height=150)