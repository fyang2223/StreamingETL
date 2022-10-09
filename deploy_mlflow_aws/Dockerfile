FROM public.ecr.aws/lambda/python:3.9

RUN pip install -U pip
RUN pip install pipenv 

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "lambda_function.py", "./" ]

# [Lambda-specific only] 
# Set the CMD to our handler function. This should be <filename>.<functioname> with your respective values.
CMD [ "lambda_function.lambda_handler" ] 