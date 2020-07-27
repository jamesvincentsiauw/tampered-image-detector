# Tampered Image Detector with Python

## How to Run
``` bash
# Clone the Repository
$ git clone https://github.com/jamesvincentsiauw/tampered-image-detector.git

# Change to Server Directory
$ cd server

# Copy .env.example to .env
$ cp .env.example .env

# Change KAFKA_IP_SERVER in .env file with your IP
KAFKA_IP_SERVER = YOUR_IP_ADDRESS

# Build the App Image
$ docker build -t tampered-image-detector:latest .

# Run the Container
$ docker run -p 5000:5000 -d tampered-image-detector

# See Your Container Status
$ docker ps

# Your Container is Live
http://localhost:5000/

# Test the API
$ curl -F 'model=v2' -F 'img=@real-1-custom.jpg' http://localhost:5000/api/predictor
```

## How to Run Unit Testing
``` bash
# Clone the Repository
$ git clone https://github.com/jamesvincentsiauw/tampered-image-detector.git

# Install Dependencies
$ pip install -r requirements.txt

# Change to test Directory
$ cd server/test

# Run the Script
$ python test_controller.py

Note: if you fail to run the script via command line, please run via IDE
```

### Additional Notes
API Documentation: https://docs.google.com/document/d/1QTPX-UJeraMyPCkQgoGfW7LYLl80uboxd3x-PBdJPTg/edit?usp=sharing

Project Documentation: https://docs.google.com/document/d/1844Wf_I-7o62gJUkZlqM5xkFdGI9dpqIzkXdf2HuHdM/edit?usp=sharing
