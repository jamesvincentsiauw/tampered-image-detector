# Tampered Image Detector with Python

## How to Run
``` bash
# Clone the Repository
$ git clone https://github.com/jamesvincentsiauw/tampered-image-detector.git

# Change to Server Directory
$ cd server

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