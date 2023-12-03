from google.cloud import vision
from utils import get_files_in_folder
import shutil
import os
import click

def extract_text_from_product_images(input_path, output_path, copy_images):
    if not os.path.exists(output_path):
        raise f'Folder {output_path} does not exist'

    image_files = get_files_in_folder(input_path)
    image_files = [im for im in image_files if im.endswith('.jpeg')]

    print(f'Found {len(image_files)} image(s) to extract text from')

    client = vision.ImageAnnotatorClient()

    for image_file in image_files:
        with open(image_file, "rb") as file:
            content = file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image, image_context={"language_hints": ["no"]})
        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )

        json = vision.AnnotateImageResponse.to_json(response)

        _, tail = os.path.split(image_file)
        image_file_name, _ = tail.split('.')

        with open(os.path.join(output_path, image_file_name + '.json'), 'w') as file:
            file.write(json)
            file.close()

        if copy_images:
            with open(os.path.join(output_path, image_file_name + '.jpeg'), 'w') as destination_image:
                shutil.copyfileobj(file, destination_image)

    print(f'Finished extracting text from {len(image_files)} image(s)')


@click.command()
@click.option("--input_path", prompt="Path to the folder containing your product images", help="Specifies the location of the product images", required=True)
@click.option("--output_path", prompt="Path to folder to save the textual data", help="Specifies where the textual data will be saved", required=True)
@click.option("--copy_images", prompt="Do you want to copy the product image to the output file?", help="If true, copies the product image into the output path along with the textual data", is_flag=True)
def main(input_path, output_path, copy_images):
    """
    Extracts text from products in brochure images found in the input_path into individual images.
    Textual data will be saved in the output path.
    """
    extract_text_from_product_images(input_path, output_path, copy_images)

if __name__ == '__main__':
    main()