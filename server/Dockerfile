# Use an official Python runtime as a parent image
FROM python:latest

# build tools required for dlib
RUN apt-get update -y && \
    apt-get install build-essential cmake pkg-config -y

# tools required for cv2
RUN apt-get install libsm6 libxext6 libxrender-dev -y
RUN apt-get libxext6  -y

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -U pip wheel cmake
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /app
COPY . /app

