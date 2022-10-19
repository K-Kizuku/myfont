FROM python:3.10.6

RUN mkdir -p /code
COPY . /code/
WORKDIR /code

RUN apt update
RUN apt install -y libpq-dev build-essential
RUN pip install --upgrade pip setuptools wheel

RUN pip install pillow
RUN pip install scipy
RUN pip install imageio
RUN pip install opencv-python
RUN pip install cloudinary
RUN pip install python-dotenv
RUN pip install google
RUN pip install google-cloud 
RUN pip install google-cloud-storage
RUN pip install google-cloud-aiplatform
RUN pip install pipenv
RUN pipenv install

RUN apt update -y\
    && apt upgrade -y

RUN apt-get install ffmpeg  -y
RUN apt-get install libsm6   -y
RUN apt-get install libxext6 -y
RUN apt install fontforge -y   
RUN apt install potrace -y

ENTRYPOINT []
CMD pipenv run uvicorn main:app --host 0.0.0.0 --reload