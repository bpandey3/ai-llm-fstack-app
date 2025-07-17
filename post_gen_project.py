import os
import shutil
import json

def move_lambda_to_lambdas():
    # Read cookiecutter context from cookiecutter.json in current directory
    context_file = os.path.join(os.getcwd(), 'cookiecutter.json')
    with open(context_file, 'r') as f:
        context = json.load(f)

    lambda_name = context['lambda_name']
    project_dir = os.getcwd()
    src_path = os.path.join(project_dir, lambda_name)
    dest_dir = os.path.join(project_dir, 'lambdas')
    dest_path = os.path.join(dest_dir, lambda_name)

    os.makedirs(dest_dir, exist_ok=True)

    # Move lambda folder into lambdas/
    shutil.move(src_path, dest_path)

    # Optional: remove cookiecutter.json if you don’t want it left behind
    os.remove(context_file)

if __name__ == "__main__":
    move_lambda_to_lambdas()
