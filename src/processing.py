# imports
import cv2
import logging_utils as logging
import stopwatch
import numpy as np
from yolo_utils import *
import os
from PIL import Image

# constants
OUTPUT_VIDEO_EXTENSION = ".avi"
OUTPUT_IMAGE_EXTENSION = ".jpg"

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
    (result_image, datas) = yolo_object_detection(image, net, confidence, threshold, labels, colors)

    # get input filename without extension
    filename_no_ext = file.rsplit("." , 1)[0]

    print(filename_no_ext)

    # generate output filename
    output_file = filename_no_ext + "_processed" + OUTPUT_IMAGE_EXTENSION

    # save the image
    output_file = os.path.join(output_dir, output_file)

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

    #check file exists
    if not os.path.exists(file):
        logging.error("file not found: " + file)
        return

    # load the video
    vidcap = cv2.VideoCapture(file)

    # check if open
    if not vidcap.isOpened():
        logging.error("could not open video: " + file)
        return

    # get the video framerate
    given_framerate = int(vidcap.get(cv2.CAP_PROP_FPS))

    #if param framerate 0 use given framerate
    if(framerate <= 0):
        framerate = given_framerate

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

    # get input filename without extension
    filename_no_ext = file.split("." , 1)[0]

    # generate output filename
    output_file = filename_no_ext + "_processed" + OUTPUT_VIDEO_EXTENSION

    # create the video writer
    output_file = os.path.join(output_dir, output_file)
    out = cv2.VideoWriter(output_file,cv2.VideoWriter_fourcc(*'DIVX'), framerate, frameSize)
    logging.verbose("Output video: " + output_file)

    # get number of images from video
    number_of_images = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    # counts the number of frames in the video
    image_count = 0

    #init stopwatch for time measurement
    sw = stopwatch.Stopwatch()

    # loop over the frames of the video
    while image_count < number_of_images:

        # allocate memory for images (len = batch_size)
        sw.start()
        images = np.zeros(shape=(batch_size,height,width,3), dtype=np.uint8)
        logging.verbose(sw.message(message="Allocation time"))

        # collect batch_size images
        sw.start()

        process_n_image = round(given_framerate / framerate)
        logging.verbose("Processing every " + str(process_n_image) + " image")
        
        image_added_count = 0
        while image_added_count < batch_size and image_count < number_of_images:
            success, image = vidcap.read()
            if success:
                if image_count % process_n_image == 0:
                    images[image_added_count] = image
                    image_added_count += 1
                    logging.verbose("Added image " + str(image_added_count) + " of " + str(batch_size))
                else:
                    logging.verbose("Skipping image")
            else:
		
                break
            image_count += 1

        logging.verbose(sw.message(message="Collecting time"))

        # run inference
        if batch_size > 1:
            processed = yolo_object_detection_blob(images, net, confidence, threshold, labels, colors)
        else:
            processed = yolo_object_detection(images[0], net, confidence, threshold, labels, colors)
            processed = [processed]
        
        # write the processed images to the output video
        logging.verbose("Writing to video")
        sw.start()
        processed_count = 0
        for (image, datas) in processed:
            # write the image to the output video
            out.write(image)
            
            if enable_detection_recording:
                # calculate time of image in video
                time = round((image_count + processed_count) / framerate, 2)

                # log to csv file
                for data in datas:
                    csv_logging(csv_file, time, data.class_name, data.score, data.x, data.y, data.width, data.height)
                
                # increase processed_count to calculate time of next image
                processed_count += 1

        logging.verbose(sw.message(message="Write time"))

        # print progress
        progress = round(image_count / number_of_images * 100, 2)
        logging.info("Progress: " + str(progress) + "%")

    # cleanup
    sw.start()
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
