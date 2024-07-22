import streamlit as st
import streamlit.components.v1 as components
from functions import *
import base64
from PIL import Image
import io

st.set_page_config(layout="wide")

html_code = f"""
<head>
    <title>ORGANIC GRIDS</title>
    <style>@import url('https://fonts.googleapis.com/css2?family=Raleway:ital,wght@0,100..900;1,100..900&display=swap')</style>
</head>
<body>
    <div style="text-align: center">
        <h1 style="font-family: Raleway;">ORGANIC GRIDS</h1>
    </div>
"""
components.html(html_code, height=60)

# Create widgets to specify grid attributes by user input
with st.container():
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col2: rows = st.number_input(label="Number of rows", min_value=1, max_value=10, value=4, step=1)
    with col2: transition_size = st.slider(label="Transition size", min_value=0.1, max_value=5.0, value=2.5, step=0.1)

    with col3: cols = st.number_input(label="Number of columns", min_value=1, max_value=10, value=6, step=1)
    with col3: transition_speed = st.slider(label="Transition speed", min_value=0.1, max_value=5.0, value=2.5, step=0.1)
    transition_speed = 1 / transition_speed

# Upload image file
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Disply image in grid
with st.container():

        if uploaded_file is not None:
            # Read uploaded file as bytes
            bytes_data = uploaded_file.read()
            img_type = uploaded_file.name.split('.')[1]

            # Convert bytes to image
            img = Image.open(io.BytesIO(bytes_data))
            img_width, img_height = img.size

            style = create_stylesheet(transition_speed, transition_size)

            html_output = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <style>{style}</style>
            </head>
            <body>
            <div class="container">
            """

            # Split image and create html output
            piece_width = img_width // cols    # Calculate size of pieces
            piece_height = img_height // rows

            for row in range(rows):
                html_output += '<div class="row">'
                for col in range(cols):

                    # Split image
                    left = col * piece_width
                    top = row * piece_height
                    right = (col + 1) * piece_width
                    bottom = (row + 1) * piece_height
                    box = (left, top, right, bottom)
                    piece = img.crop(box)

                    image_bytes_io = io.BytesIO()

                    # Convert RGBA image to RGB
                    if img_type == 'png':
                        piece = piece.convert("RGB")

                    piece.save(image_bytes_io, format="JPEG")
                    base64_image = base64.b64encode(image_bytes_io.getvalue()).decode('utf-8')

                    html_output += '<div class="grid-element", '
                    html_output += 'style="background-image:'
                    html_output += f"url('data:image/jpeg;base64,{base64_image}')"
                    html_output += '"></div>'
                html_output += '</div>'

            html_output += '</div></body></html>'

            components.html("", height=30)
            components.html(html_output, height=600)