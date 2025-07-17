import os
import shutil

def move_lambda_to_lambdas():
    lambda_name = os.environ["COOKIECUTTER_lambda_name"]
    project_dir = os.getcwd()
    src_path = os.path.join(project_dir, lambda_name)
    dest_dir = os.path.join(project_dir, "lambdas")
    dest_path = os.path.join(dest_dir, lambda_name)

    os.makedirs(dest_dir, exist_ok=True)

    # Move the folder into lambdas/
    shutil.move(src_path, dest_path)

if __name__ == "__main__":
    move_lambda_to_lambdas()
