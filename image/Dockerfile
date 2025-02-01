FROM public.ecr.aws/lambda/python:3.11

# copy requirements.txt to container root directory
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip3 install -r requirements.txt

COPY . ${LAMBDA_TASK_ROOT}

# setting the CMD to your handler file_name.function_name
ENV PYTHONPATH=/var/task/source:$PYTHONPATH

CMD [ "source.main.real_estate_scraper" ]

