#import readTrafficSigns as rts
#import cv2

#(images, labels) = rts.readTrafficSigns(rootpath='/home/tho/studienarbeit_mueller/train-gtsrb/GTSRB_Final_Training_Images/GTSRB/Final_Training/Images')



#print(labels)



from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="dataset-training")


trainer.setTrainConfig(object_names_array=['speed limit 20', 'speed limit 30', 'speed limit 50', 'speed limit 60',
'speed limit 70', 'speed limit 80', 'restriction ends 80', 'speed limit 100', 'speed limit 120', 'no overtaking',
'no overtaking (trucks)', 'priority at next intersection', 'priority road', 'give way', 'stop', 'no traffic both ways',
'no trucks', 'no entry', 'danger', 'bend left', 'bend right', 'bend', 'uneven road', 'slippery road ', 'slippery road',
'road narrows', 'construction', 'traffic signal', 'pedestrian crossing', 'school crossing', 'cycles crossing', 'snow',
'animals', 'restriction ends', 'go right', 'go left', 'go straight', 'go right or straight', 'keep right', 'keep left ', 'roundabout'],
batch_size=4, num_experiments=3, train_from_pretrained_model="pretrained-yolov3.h5")
trainer.trainModel()