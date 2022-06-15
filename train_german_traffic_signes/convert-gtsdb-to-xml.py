from lxml.etree import Element, SubElement, tostring
import pprint
from xml.dom.minidom import parseString
import numpy as np
import cv2


CLASSES = [ 'speed limit 20', 'speed limit 30', 'speed limit 50', 'speed limit 60',
	'speed limit 70', 'speed limit 80', 'restriction ends 80', 'speed limit 100', 'speed limit 120',
	'no overtaking', 'no overtaking (trucks)', 'priority at next intersection', 'priority road',
	'give way', 'stop', 'no traffic both ways',
	'no trucks', 'no entry', 'danger', 'bend left','bend right', 'bend', 'uneven road',
	'slippery road ', 'slippery road', 'road narrows', 'construction','traffic signal', 'pedestrian crossing', 'school crossing',
	'cycles crossing', 'snow', 'animals', 'restriction ends',
	'go right', 'go left', 'go straight', 'go right or straight','keep right',
	'keep left ', 'roundabout', 'restriction ends', 'restriction ends']


DEPTH = 3
FOLDER = "TrainIJCNN2013"

PATH = "GTSRB_Final_Training_Images/GTSRB/Final_Training/Images/"

def create_folders(where):
    import os
    os.makedirs(name=where + "/train", exist_ok=True)
    os.makedirs(name=where + "/train/annotations", exist_ok=True)
    os.makedirs(name=where + "/train/images", exist_ok=True)
    os.makedirs(name=where + "/validation", exist_ok=True)
    os.makedirs(name=where + "/validation/annotations", exist_ok=True)
    os.makedirs(name=where + "/validation/images", exist_ok=True)


def generate_pascal_voc(folder, filename, width, height, depth, classname, xmin, ymin, xmax, ymax):
    return """
    <annotation>
        <folder>%s</folder>
        <filename>%s</filename>
        <size>
            <width>%d</width>
            <height>%d</height>
            <depth>%d</depth>
        </size>
        <object>
            <name>%s</name>
            <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
            </bndbox>
        </object>
    </annotation>""" % (folder, filename, width, height, depth, classname, xmin, ymin, xmax, ymax)

def copy_image(image_path, target_folder, target_name):
    import shutil
    shutil.copy(image_path, target_folder + "/" + target_name)



create_folders("dataset-training")

classes = []

#num f classes (folders)
for i in range(43):

    indexStr = str(i).zfill(5)
    path = PATH + "/" + indexStr + "/" + "GT-" + indexStr + ".csv"

    with open(path,"r") as f:
        lines = f.readlines()

        validationImages = len(lines) / 10 #10% validation

        count = 0
        for lineRaw in lines[1:]:
            line=lineRaw.split(';')

            (filename, width, height, roiX1, roiY1, roiX2, roiY2, classId) = line

            width = int(width)
            height = int(height)
            classId = int(classId)
            roiX1 = int(roiX1)
            roiY1 = int(roiY1)
            roiX2 = int(roiX2)
            roiY2 = int(roiY2)

            if(CLASSES[classId] not in classes):
                classes.append(CLASSES[classId])

            newImageFilename = indexStr + "_" + filename

            pascal_voc_str = generate_pascal_voc(FOLDER, newImageFilename, width, height, DEPTH, CLASSES[classId], roiX1, roiY1, roiX2, roiY2)

            filename_pascal_voc = indexStr + "_" + filename.replace(".ppm", ".xml")

            subfolder = ""
            if(count < validationImages):
                subfolder = "validation"
            else:
                subfolder = "train"

            
                
            with open("dataset-training/"+subfolder+"/annotations/"+filename_pascal_voc,"w") as f:
                f.write(pascal_voc_str) 

            image_path = PATH + "/" + indexStr + "/" + filename

            img = cv2.imread(image_path)

            copy_image(image_path, "dataset-training/"+subfolder+"/images", newImageFilename)

            count += 1


print(classes)