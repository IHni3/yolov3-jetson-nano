# imports
import cv2
import logging_utils as logging
import stopwatch
import numpy as np
from yolo_od_utils import *
import os
from PIL import Image

# constants
OUTPUT_VIDEO_FILENAME = "output_video.avi"
OUTPUT_IMAGE_FILENAME = "output_image.jpg"

# variables
enable_detection_recording = False

# functions
def process_images(file, output_dir, net, confidence, threshold, labels, colors):
    """ Apply YOLO object detection on a image file.
        file : Input image
        output_dir : Output directory
        net : YOLO v3 network object
        confidence : Confidence threshold (specified in command line)
        threshold : IoU threshold for NMS (specified in command line)
        labels : Class labels specified in coco.names
        colors : Colors assigned to the classes
    """
    # init stopwatch for time measurement
    sw = stopwatch.Stopwatch()

    # create csv file for object logging
    if enable_detection_recording:
        csv_file = create_csv(output_dir)


    # load the image
    logging.verbose("Loading image: " + file)
    sw.start()
    image = cv2.imread(file)    
    logging.verbose(sw.message(message="Loading image time"))

    # check if image is loaded
    if(image is None):
        logging.error("Image not found: " + file)
        return

    # inference
    logging.verbose("Running inference")
    sw.start()
    (result_image, datas) = yolo_object_detection(image, net, confidence, threshold, labels, colors)
    logging.verbose(sw.message(message="Inference time"))

    # save the image
    output_file = os.path.join(output_dir, OUTPUT_IMAGE_FILENAME)

    # save the image
    logging.verbose("Saving image: " + output_file)
    sw.start()
    cv2.imwrite(output_file, image)
    logging.verbose(sw.message(message="Saving image time"))

    if enable_detection_recording:
        # log to csv file
        logging.verbose("Logging to csv file")
        for data in datas:
            csv_logging(csv_file, "", data.class_name, data.score, data.x, data.y, data.width, data.height)

def process_video(file, output_dir, batch_size, net, confidence, threshold, labels, colors, framerate):
    """ Apply YOLO object detection on a video file.
        file : Input image
        output_dir : Output directory
        batch_size : Batch size for inference
        net : YOLO v3 network object
        confidence : Confidence threshold (specified in command line)
        threshold : IoU threshold for NMS (specified in command line)
        labels : Class labels specified in coco.names
        colors : Colors assigned to the classes
        framerate : Framerate of the output video
    """

    if enable_detection_recording:
        # create csv file for object logging
        csv_file = create_csv(output_dir)

    # load the video
    vidcap = cv2.VideoCapture(file)

    # get the video framerate
    given_framerate = int(vidcap.get(cv2.CAP_PROP_FPS))

    # given framerate is smaller then output framerate
    if(given_framerate < framerate):
        logging.error("Given video framerate is smaller then output framerate")
        return

    logging.verbose("Framerate: " + str(framerate))

    # get the video dimensions
    width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # width and height to tuple
    frameSize = (width, height)
    logging.verbose("Frame size: " + str(frameSize))

    # create output_dir if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # create the video writer
    output_file = os.path.join(output_dir, OUTPUT_VIDEO_FILENAME)
    out = cv2.VideoWriter(output_file,cv2.VideoWriter_fourcc(*'DIVX'), framerate, frameSize)
    logging.verbose("Output video: " + output_file)

    # counts the number of frames in the video
    count = 0

    #init stopwatch for time measurement
    sw = stopwatch.Stopwatch()

    # loop over the frames of the video
    while vidcap.isOpened():

        # allocate memory for images (len = batch_size)
        sw.start()
        images = np.zeros(shape=(batch_size,height,width,3), dtype=np.uint8)
        logging.verbose(sw.message(message="Allocation time"))

        # collect batch_size images
        sw.start()

        process_n_image = round(given_framerate / framerate)
        logging.verbose("Processing " + str(process_n_image) + " images")
        
        image_added_count = 0
        total_count = 0
        while image_added_count < batch_size:
            success, image = vidcap.read()
            if success:
                if total_count % process_n_image == 0:
                    images[image_added_count] = image
                    image_added_count += 1
                    logging.verbose("Added image " + str(image_added_count) + " of " + str(batch_size))
                else:
                    logging.verbose("Skipping image")
            else:
                break
            total_count += 1

        logging.verbose(sw.message(message="Collecting time"))

        # run inference on the batch
        sw.start()
        processed = yolo_object_detection_blob(images, net, confidence, threshold, labels, colors)
        logging.verbose(sw.message(message="Inference time"))        
        
        # write the processed images to the output video
        logging.verbose("Writing to video")
        sw.start()
        processed_count = 0
        for (image, datas) in processed:
            # write the image to the output video
            out.write(image)
            
            if enable_detection_recording:
                # calculate time of image in video
                time = round((count + processed_count) / framerate, 2)

                # log to csv file
                for data in datas:
                    csv_logging(csv_file, time, data.class_name, data.score, data.x, data.y, data.width, data.height)
                
                # increase processed_count to calculate time of next image
                processed_count += 1

        logging.verbose(sw.message(message="Write time"))

    # cleanup
    sw.start()
    cv2.destroyAllWindows()
    vidcap.release()
    out.release()
    logging.verbose(sw.message(message="Cleanup time"))

def generateCsvFilename():
    """ Generates a csv filename.
    returns the filename
    """
    filename = time.strftime("detection-data-%Y%m%d-%H%M%S.csv")
    return filename


def create_csv(directory):
    """ Creates a csv file in the specified directory.
        directory : Directory to create the csv file
    """
    filename = os.path.join(directory, generateCsvFilename())
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['time (s)', 'class name', 'score (%)', 'x', 'y', 'width', 'height'])
    return filename

def csv_logging(filepath, time,  class_name, score, x, y, width, height):
    """ Logs the detection results to a csv file.
        filepath : Name of the csv file
        class_name : Name of the class
        score : Confidence score
        x : x-coordinate of the top left corner of the bounding box
        y : y-coordinate of the top left corner of the bounding box
        width : Width of the bounding box
        height : Height of the bounding box
    """
    with open(filepath, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([time, class_name, score, x, y, width, height])