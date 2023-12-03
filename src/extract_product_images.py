from dotenv import load_dotenv
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
from utils import get_files_in_folder
from PIL import Image

import click
import base64
import os

load_dotenv()

def extract_product_images(input_path, output_path):
    if not os.path.exists(output_path):
        raise f'Folder {output_path} does not exist'

    image_files = get_files_in_folder(input_path)

    counter = 0
    for image_file in image_files:
        predictions = detect_products(image=image_file)
        
        _, tail = os.path.split(image_file)
        image_name, _ = tail.split('.')

        prediction = predictions[0]
        bboxes = prediction["bboxes"]

        print(f'Extracting {len(bboxes)} product image(s) from {image_file}')

        for idx, bbox in enumerate(bboxes):
            cropped = crop_image(image=image_file, bbox=bbox)
            cropped_file_name = os.path.join(output_path, image_name + '-' + str(idx) + '.jpeg')
            cropped.save(cropped_file_name, format="jpeg")
            counter = counter + 1
        
    print(f'Cropped {counter} product image(s) from {image_file}')


def detect_products(*, image, max_predictions = 10, confidence_threshold = 0.8):
    with open(image, "rb") as f:
        file_content = f.read()

    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageObjectDetectionPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]

    parameters = predict.params.ImageObjectDetectionPredictionParams(
        confidence_threshold=confidence_threshold,
        max_predictions=max_predictions,
    ).to_value()

    PBBD_PROJECT_ID = os.getenv('PBBD_PROJECT_ID')
    PBBD_ENDPOINT_ID = os.getenv('PBBD_ENDPOINT_ID')
    PBBD_LOCATION = os.getenv('PBBD_LOCATION')
    PBBD_API_ENDPOINT = os.getenv('PBBD_API_ENDPOINT')

    client = aiplatform.gapic.PredictionServiceClient(client_options= {"api_endpoint": PBBD_API_ENDPOINT})
    endpoint = client.endpoint_path(
        project=PBBD_PROJECT_ID, location=PBBD_LOCATION, endpoint=PBBD_ENDPOINT_ID
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    return response.predictions


def crop_image(*, image, bbox):
    image = Image.open(image)
    # latitude and longitude are on a scale from 0 to 1
    # 
    #                 longMin
    #         (0,0)-------------(1,0)
    #           |                 |
    #           |                 |
    #    latMin |      image      | latMax
    #           |                 |
    #           |                 |
    #           |                 |
    #         (0,1)-------------(1,1)
    #                 longMax 
    # 
    (latMin, latMax, longMin, longMax) = bbox
    (width, height) = image.size
    # convert the bounding box to pixels
    left = latMin * width
    upper = longMin * height
    right = latMax * width
    lower = longMax * height
    return image.crop(box=(left, upper, right, lower))


@click.command()
@click.option("--input_path", prompt="Path to the folder containing your brochure images", help="Specifies the location of the brochure images", required=True)
@click.option("--output_path", prompt="Path to folder to save the cropped images", help="Specifies where the cropped images will be saved", required=True)
def main(input_path, output_path):
    """
    Crops products in brochure images found in the input_path into individual images.
    """
    extract_product_images(input_path, output_path)

if __name__ == '__main__':
    main()