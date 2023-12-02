## Prerequisites

Access to Google Cloud with Vision AI enabled.

Follow the instructions [https://cloud.google.com/sdk/docs/install](here) to install gcloud locally. Make sure to follow the instructions to add gcloud to your PATH.

Create and initialize the virtual environment.

brew install poppler
brew install pyenv

```
pip install virtualenv
// cd into project directory
cd eppy-data
// activate the virtual env
source bin/activate
python -m pip install -r requirements.txt
```

Auth against google cloud by following the instructions [here](https://googleapis.dev/python/google-api-core/latest/auth.html).

```
$ gcloud auth application-default login

```

## Adding new dependencies

```
python -m pip freeze > requirements.txt
```
