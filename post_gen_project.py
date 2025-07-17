import os

lambda_path = os.path.join("lambdas", "{{ cookiecutter.lambda_name }}")
os.makedirs(lambda_path, exist_ok=True)
