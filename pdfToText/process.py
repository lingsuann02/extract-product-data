from pdf2image import convert_from_path
from google.cloud import vision
from PIL import Image, ImageDraw
from enum import Enum
import os

results_path = './files/results'

class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def get_files_in_folder(path):
    return [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f != '.DS_Store' and not os.path.isdir(f)
    ]


def convert_pdf_to_image(path):
    files = get_files_in_folder(path)

    for file in files:
        _, file_name_including_extension = os.path.split(file)
        file_name, _ = file_name_including_extension.split('.')

        converted_files_path = os.path.join('results', file_name)
        if not os.path.exists(converted_files_path):
            os.makedirs(converted_files_path)

        images = convert_from_path(file)

        for i in range(len(images)):
            images[i].save(converted_files_path + '/page-' + str(i) +'.jpg', 'JPEG')

        os.rename(file, os.path.join('processed', file_name_including_extension))


def extract_text():
    client = vision.ImageAnnotatorClient()
    results_files = get_files_in_folder(results_path)
    for result_path in results_files:
        is_folder = os.path.isdir(result_path)
        if not is_folder:
            continue
        image_files = get_files_in_folder(result_path)
        for image_file in image_files:
            is_folder = os.path.isdir(image_file)
            if is_folder:
                continue
            
            if not image_file.endswith('.jpg'):
                continue

            with open(image_file, "rb") as file:
                content = file.read()
            image = vision.Image(content=content)

            response = client.text_detection(image=image, image_context={"language_hints": ["no"]})
            json = vision.AnnotateImageResponse.to_json(response)

            _, image_file_name_including_extension = os.path.split(image_file)
            image_file_name, _ = image_file_name_including_extension.split('.')

            with open(image_file_name + '.json', 'w') as file:
                file.write(json)
                file.close()

            if response.error.message:
                raise Exception(
                    "{}\nFor more info on error messages, check: "
                    "https://cloud.google.com/apis/design/errors".format(response.error.message)
                )
            

def draw_boxes(image, bounds, color):
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon(
            [
                bound.vertices[0].x,
                bound.vertices[0].y,
                bound.vertices[1].x,
                bound.vertices[1].y,
                bound.vertices[2].x,
                bound.vertices[2].y,
                bound.vertices[3].x,
                bound.vertices[3].y,
            ],
            None,
            color,
            5
        )
    return image


def get_bounds(detected_text_response, feature):
    document = detected_text_response.full_text_annotation
    bounds = []
    # Collect specified feature bounds by enumerating all document features
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if feature == FeatureType.SYMBOL:
                            bounds.append(symbol.bounding_box)

                    if feature == FeatureType.WORD:
                        bounds.append(word.bounding_box)

                if feature == FeatureType.PARA:
                    bounds.append(paragraph.bounding_box)

            if feature == FeatureType.BLOCK:
                bounds.append(block.bounding_box)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds


def annotate_images():
    results_files = get_files_in_folder(results_path)
    for result_path in results_files:
        is_folder = os.path.isdir(result_path)
        if not is_folder:
            continue

        image_to_text_map = []

        image_files = get_files_in_folder(result_path)
        for file in image_files:
            if file.endswith('.jpg'):
                image_to_text_map.append([file, file + '.json'])

        for [image_file, detected_text_file] in image_to_text_map:
            text_file = open(detected_text_file)
            json = text_file.read()

            detected_text_response = vision.AnnotateImageResponse.from_json(json)

            image = Image.open(image_file)
            bounds = get_bounds(detected_text_response, FeatureType.BLOCK)
            draw_boxes(image, bounds, "blue")
            bounds = get_bounds(detected_text_response, FeatureType.PARA)
            draw_boxes(image, bounds, "red")
            bounds = get_bounds(detected_text_response, FeatureType.WORD)
            draw_boxes(image, bounds, "yellow")

            image.save(image_file)


convert_pdf_to_image('./files/unprocessed')
extract_text()
annotate_images()