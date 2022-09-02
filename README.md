# PhotoAndVideoAnalysis
PhotoAndVideoAnalysis is a system to store and analyze images and video files, the goal is to extract as much information as possible from the images using exif data, image recognition techniques and to provide a web interface to easily use the information extrated to retrieve photo, create albums, etc...

Main technologies used are docker, postgres, rabbitmq, ffmpeg, mongodb, opencv
Programming languages are Python and Javascript (Angular)

# Working principles
1. original file is never modified (batch load will move from load folder to storage folder keeping the same directory hierarchy)
2. analysis are queued per analysis type using Rabbitmq

# Load in DB
Batch load from a source folder
1. prevent duplicate photo or video insertion using sha 512
2. extract exif from photo or video (camera type, gps data, date and time)
3. thumbnail creation

# Analysis
## Photos:
1. object detection
2. face detection
3. text detection and OCR

## Video:
1. speech to text

# Web Interface:
1. search criteria using date, gps coordinates (thru map area selection), object detected, face similarity
2. open street map pins for each photo video with GPS coordinate
[![screenshot of map](./docs/screenshot/map_world.png)]
[![screenshot of map](./docs/screenshot/map_corsica.png)]
4. add comments to video or photo in db
5. add gps coordinates to video or photo in db
6. group photos or videos in albums
7. timeline for photos
8. layer on top of picture to highlight detected objects
9. Find similar faces across the database
