from PIL import Image
import os
import base64
import io
import requests

def create_stylesheet(transition_speed, transition_size):
    
    style_content = f"body {{ display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: Arial, sans-serif; }} .container {{ width: 900px; height: 600px; display: flex; flex-direction: column; gap: 2px; }} .row {{ display: flex; flex-direction: row; gap: 2px; }} .grid-element {{ background-color: pink; opacity: 1; border-radius: 0px; background-size: cover; }} .row, .grid-element {{ flex: 1; -webkit-transition: flex {transition_speed}s ease-out; -moz-transition: flex {transition_speed}s ease-out; -ms-transition: flex {transition_speed}s ease-out; -o-transition: flex {transition_speed}s ease-out; transition: flex {transition_speed}s ease-out; }} .row:hover {{ flex: {transition_size}; opacity: 1; }} .grid-element:hover {{ flex: {transition_size}; opacity: 1; }}"
    
    return style_content

def get_base64_encoded_image(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def split_image_and_create_html_output(img, img_type, rows, cols, transition_speed, transition_size):

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
    return html_output


def fetch_image_from_url(url):
    # Download the image
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors
    
    # Convert the image to a BytesIO object
    image_bytes = io.BytesIO(response.content)
    
    # Optionally open it with PIL to ensure it's a valid image
    img = Image.open(image_bytes)
    
    # Reset the BytesIO pointer to the beginning
    image_bytes.seek(0)
    
    return image_bytes, img.format

    