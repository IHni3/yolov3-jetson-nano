# imports
import numpy as np
import argparse
import cv2
import os.path
import mimetypes

import logging_utils as logging
import processing

### Get options specified in the command line
#############################################################################################
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('file', type=str, help='Path to image or video file')

parser.add_argument('-c', '--confidence',
    type=float,
    default=0.3,
    help='Minimum probability to filter weak detections')

parser.add_argument('-t', '--threshold',
    type=float,
    default=0.5,
    help='Threshold for Non-Maximum-Surpression (NMS)')

parser.add_argument('-m', '--mode',
    type=str,
    default='video',
    choices=['video', 'image'],
    help='Mode of operation: video or image')

parser.add_argument('-o', '--output',
    type=str,
    default='.',
    help='Output folder')

parser.add_argument('-b', '--batch-size',
    type=int,
    default=4,
    help='Batch size for inference. Only possible for video mode')
parser.add_argument('--video-framerate', type=int, default=0, help='Video framerate')

parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

parser.add_argument('--record-detections', action='store_true', help='Enable detection logging')

args = parser.parse_args()
#############################################################################################



# set filenames for the model
coco_names_file = "../yolo/coco.names"
yolov3_weight_file = "../yolo/yolov3.weights"
yolov3_config_file = "../yolo/yolov3.cfg"

# check yolo files existing
if not os.path.isfile(coco_names_file):
    logging.error("File coco.names not found!")
    exit()
if not os.path.isfile(yolov3_weight_file):
    logging.error("File yolov3.weights not found!")
    exit()
if not os.path.isfile(yolov3_config_file):
    logging.error("File yolov3.cfg not found!")
    exit()

# read coco object names
labels = open(coco_names_file).read().strip().split("\n")

# assign random colours to the corresponding class labels
np.random.seed(45)
colors = np.random.randint(0, 255, size=(len(labels), 3), dtype="uint8")

# read YOLO network model
net = cv2.dnn.readNetFromDarknet(yolov3_config_file, yolov3_weight_file)

# set preferred processing mode to gpu	
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# enable or disable verbose printing
logging.enable_verbose_output = args.verbose

# enable or disable detection recording
processing.enable_detection_recording = args.record_detections

# check input file matches given mode (image/video)
mimetypes.init()
mimestart = mimetypes.guess_type(args.file)[0]

if mimestart != None:
    mimestart = mimestart.split('/')[0]
else:
    mimestart = ""

if mimestart == "video":
    # check missmatch of file and given mode
    if args.mode != 'video':
        logging.error("Given file has type video but given mode is image!")
        exit()

elif mimestart == "image":
    # check missmatch of file and given mode
    if args.mode != "image":
        logging.error("Given file has type image but given mode is video!")
        exit()
else:
    logging.error("Given file is not of type video or image!")
    exit() 

# check range of batch-size
if args.batch_size <= 0:
    logging.error("Given batch size is invalid!")
    exit() 

# check range of confidence
if args.confidence > 1.0:
    logging.error("Given confidence value is invalid!")
    exit()
elif args.confidence <= 0:
    logging.error("Given confidence value is invalid!")
    exit()

# check range of threshold
if args.threshold > 1.0:
    logging.error("Given confidence value is invalid!")
    exit()
elif args.threshold <= 0:
    logging.error("Given confidence value is invalid!")
    exit()

### mode is images  
if args.mode == 'image':
    processing.process_images(file=args.file,
        output_dir=args.output,
        net=net,
        confidence=args.confidence,
        threshold=args.threshold,
        labels=labels,
        colors=colors)

elif args.mode == 'video':
    processing.process_video(file=args.file,
        output_dir=args.output,
        batch_size=args.batch_size,
        net=net,
        confidence=args.confidence,
        threshold=args.threshold,
        labels=labels,
        colors=colors,
        framerate=args.video_framerate)
else:
    logging.error("Invalid mode")
