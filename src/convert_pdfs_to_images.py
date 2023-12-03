from utils import get_files_in_folder
from pdf2image import convert_from_path
import os
import click

def convert_pdfs_to_images(input_path, output_path):
    if not os.path.exists(output_path):
        raise f'Folder {output_path} does not exist'

    pdf_files = get_files_in_folder(input_path)
    pdf_files = [pf for pf in pdf_files if pf.endswith('.pdf')]

    print(f'Found {len(pdf_files)} pdf(s) to convert to images')

    counter = 0
    for pdf_file in pdf_files:
        images = convert_pdf_to_images(pdf_file, output_path)
        counter = counter + len(images)

    print(f'Converted {len(pdf_files)} pdf(s) to convert to {counter} image(s)')


def convert_pdf_to_images(pdf_file, output_path):
    _, tail = os.path.split(pdf_file)
    file_name, _ = tail.split('.')

    images = convert_from_path(pdf_file)

    for i in range(len(images)):
        image_path = os.path.join(output_path, file_name + '-' + str(i) + '.jpeg')
        images[i].save(image_path)

    return images


@click.command()
@click.option("--input_path", prompt="Path to the folder containing your pdfs", help="Specifies the location of the pdfs", required=True)
@click.option("--output_path", prompt="Path to folder to export the images", help="Specifies where the images will be saved", required=True)
def main(input_path, output_path):
    """
    Converts any pdfs found in the input_path to jpegs in the output_path. 
    """
    convert_pdfs_to_images(input_path, output_path)

if __name__ == '__main__':
    main()