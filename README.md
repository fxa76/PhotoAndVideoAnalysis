# PhotoAndVideoAnalysis

##Working principles
1. original file is never modified (batch load will move from load folder to storage folder keeping the same directory hierarchy)
2. analysis are queued per analysis type using Rabbitmq

##Load in DB
Batch load from a source folder
1. prevent duplicate photo or video insertion using sha 512
2. extract exif from photo or video (camera type, gps data, date and time)
3. thumbnail creation

##Analysis
###Photos:
1. object detection
2. face detection
3. text detection and OCR

###Video:
1. speech to text

##Web Interface:
1. search criteria using date, gps coordinates (thru map area selection), object detected, face similarity
2. open street map pins for each photo video with GPS coordinate
3. add comments to video or photo in db
4. add gps coordinates to video or photo in db
5. group photos or videos in albums
6. timeline for photos
7. layer on top of picture to highlight detected objects
8. Find similar faces across the database
