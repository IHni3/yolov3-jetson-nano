FROM officinerobotiche/ros:foxy-ros-base-l4t-r32.4.4-cv-4.4.0

ENV DEBIAN_FRONTEND=noninteractive 

# update apps on the base image
#RUN apt-get -y update && apt-get install 

# install dependencies
#RUN apt-get -y install python3 pip software-properties-common apt-utils 
#python3-opencv

# install opencv python module
# RUN pip3 install opencv-python
RUN pip3 install Pillow
RUN pip3 install termcolor
RUN pip3 install numpy

#copy current directory to docker container
COPY . .

# build opencv
# RUN /build_open_cv.sh

#add entrypoint
COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
