import os
import shutil

lambda_name = os.environ['COOKIECUTTER_lambda_name']
base_dir = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'genai-lambda-base', 'lambdas'))
target_path = os.path.join(base_dir, lambda_name)

os.makedirs(target_path, exist_ok=True)

# copy rendered files from current dir to the target folder
shutil.copyfile('index.py', os.path.join(target_path, 'index.py'))
