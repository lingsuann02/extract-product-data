# Extract product images and text from customer leaflets

WIP

## Prerequisites

At least Python 3.9.6 - we use [pyenv](https://github.com/pyenv/pyenv) to manage python versions

[Poppler](https://poppler.freedesktop.org/) for reading and modifying pdfs.

[Virtualenv](https://github.com/pypa/virtualenv) for creating isolated virtual python environments.

Run the following commands to install poppler, pyenv and virtualenv :)

```bash
brew install poppler
brew install pyenv
pip install virtualenv
```

Once the prerequisites are installed, open up your shell and run the following to set up install dependencies.

```bash
# cd into project directory
cd eppy-data
# activate the virtual env
source bin/activate
# install python reqs
python -m pip install -r requirements.txt
```

We use google cloud to extract textual data from images, so make sure you auth against google cloud by following the instructions [here](https://googleapis.dev/python/google-api-core/latest/auth.html) and have the Vision AI enabled.

```
$ gcloud auth application-default login
```

Copy the contents of `.env-template` to `.env` and set the environment variables to your deployment of your machine learning model.

## Commands

Below, you'll find instructions on how to use the various commands in this library.
Feel free to follow/ignore the naming recommendations for folders.

### Convert pdf to images

From the root directory, run the following to convert pdfs to images.
`python ./src/convert_pdfs_to_images.py`
This command will find any pdfs in the specified folder `input_path` and convert it to an image. The image will be saved in the specified `output_path`.

We recommend naming the input folder `pdfs`.
We recommend naming the output folder `pdfs_as_images`.

```
python ./src/convert_pdfs_to_images.py --input_path="./pdfs" --output_path="./pdfs_as_images"
```

### Extract product images

From the root directory, run the following to convert pdfs to images.
`python ./src/extract_product_images.py`
This command will find any images in the specified folder `input_path`, detect and product images. The cropped images will be saved in the specified `output_path`.

We recommend naming the output folder `product_images`.

```
python ./src/extract_product_images.py --input_path="./pdfs_as_images" --output_path="./product_images"
```

### Extract textual data from images

From the root directory, run the following to convert pdfs to images.
`python ./src/extract_text_from_product_images.py`
This command will find any images in the specified folder `input_path`, detect and product images. The cropped images will be saved in the specified `output_path`.
This command also accepts an additional arg `copy_images` if you want to copy the image to the output path.

We recommend naming the output folder `product_data`.

```
python ./src/extract_text_from_product_images.py --input_path="./product_images" --output_path="./product_data" --copy_images=True
```
