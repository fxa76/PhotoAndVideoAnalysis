from ultralytics import YOLO
import numpy as np

model = YOLO("yolov10x.pt")
results = model("test2.jpg")
cls = results[0].boxes.cls
xywh = results[0].boxes.xywh.numpy()
conf = results[0].boxes.conf
i=0
for c in cls:
    print(c)
    print(model.names[c.item()])
    print(xywh[0][i].item())
    print(conf[i].item())
    i+=1





results[0].show()