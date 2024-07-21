from PIL import Image
import os
import base64

def create_html_file(img_name, rows, cols):
    # specify name of output html-file
    html_file_name = img_name

    # write top lines of html code
    html_output = ''
    html_output += '<!DOCTYPE html>'
    html_output += '<html>'
    html_output += '<head>'
    html_output += f'<title>{img_name}</title>'
    html_output += '<link rel="stylesheet" href="style.css" />'
    html_output += '</head>'
    html_output += '<body>' 
    html_output += '<div class="container">'

    # create <div>-elements for each image-'cell'
    # and write elements to html code
    for row in range(rows):
        html_output += '<div class="row">'
        for col in range(cols):
            img_path = f"'img_split/piece_{row}_{col}.jpg'"
            html_output += '<div class="grid-element", '
            html_output += f'style="background-image: url({img_path})"'
            html_output += '></div>'
        html_output += '</div>'

    # write bottom lines of html code
    html_output += '</div>'
    html_output += '</body>'
    html_output += '</html>'

    # define folder and file name for output html-file
    output_folder = f'../files/{img_name}'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # create output html-file and write the code to the file
    with open(f"{output_folder}/{html_file_name}.html", "w") as text_file:
        text_file.write(f"{html_output}")

    return html_output

def split_image(img_name, rows, cols):
    # Open the input image
    input_path = f'../img/{img_name}.jpeg'
    img = Image.open(input_path)
    img_width, img_height = img.size

    # Calculate the size of each piece
    piece_width = img_width // cols
    piece_height = img_height // rows

    # Create the output folder if it doesn't exist
    output_folder = f'../files/{img_name}/img_split'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Split the image and save each piece
    for row in range(rows):
        for col in range(cols):
            left = col * piece_width
            top = row * piece_height
            right = (col + 1) * piece_width
            bottom = (row + 1) * piece_height
            box = (left, top, right, bottom)
            piece = img.crop(box)
            piece_filename = f"piece_{row}_{col}.jpg"
            piece_path = os.path.join(output_folder, piece_filename)
            piece.save(piece_path)

def split_uploaded_image(img, rows, cols):

    img_name = img.split('.')[0]
    img_type = img.split('.')[1]

    # Open the input image
    input_path = f'../files/{img_name}-{rows}-{cols}/{img}'
    img = Image.open(input_path)
    img_width, img_height = img.size

    # Calculate the size of each piece
    piece_width = img_width // cols
    piece_height = img_height // rows

    # Create the output folder if it doesn't exist
    output_folder = f'../files/{img_name}-{rows}-{cols}/img_split'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Split the image and save each piece
    for row in range(rows):
        for col in range(cols):
            left = col * piece_width
            top = row * piece_height
            right = (col + 1) * piece_width
            bottom = (row + 1) * piece_height
            box = (left, top, right, bottom)
            piece = img.crop(box)
            piece_filename = f"piece_{row}_{col}.jpg"
            piece_path = os.path.join(output_folder, piece_filename)
            piece.save(piece_path)

def create_stylesheet(img_name, rows, cols, transition_speed, transition_size):
    style_content = f"body {{ display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: Arial, sans-serif; }} .container {{ width: 900px; height: 600px; display: flex; flex-direction: column; gap: 2px; }} .row {{ display: flex; flex-direction: row; gap: 2px; }} .grid-element {{ background-color: pink; opacity: 1; border-radius: 0px; background-size: cover; }} .row, .grid-element {{ flex: 1; -webkit-transition: flex {transition_speed}s ease-out; -moz-transition: flex {transition_speed}s ease-out; -ms-transition: flex {transition_speed}s ease-out; -o-transition: flex {transition_speed}s ease-out; transition: flex {transition_speed}s ease-out; }} .row:hover {{ flex: {transition_size}; opacity: 1; }} .grid-element:hover {{ flex: {transition_size}; opacity: 1; }}"

    # define folder and file name for output html-file
    output_folder = f'../files/{img_name}-{rows}-{cols}'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # create output html-file and write the code to the file
    with open(f"{output_folder}/style.css", "w") as text_file:
        text_file.write(style_content)

    return style_content

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def create_html_with_style(img, rows, cols, transition_speed, transition_size):

    img_name = img.split('.')[0]
    img_type = img.split('.')[1]

    style = create_stylesheet(img_name, rows, cols, transition_speed, transition_size)

    html_output = f"""
    <!DOCTYPE html>
    <html>
    <title>{img_name}</title>
    <style>{style}</style>
    </head>
    <body>
    <div class="container">
    """

    for row in range(rows):
        html_output += '<div class="row">'
        for col in range(cols):
            img_path = f"../files/{img_name}-{rows}-{cols}/img_split/piece_{row}_{col}.jpg"
            base64_image = get_base64_encoded_image(img_path)
            html_output += '<div class="grid-element", '
            html_output += 'style="background-image:'
            html_output += f"url('data:image/jpeg;base64,{base64_image}')"
            html_output += '"></div>'
        html_output += '</div>'

    html_output += '</div>'
    html_output += '</body>'
    html_output += '</html>'

    return html_output

    