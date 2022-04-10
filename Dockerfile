FROM ros:foxy

ENV DEBIAN_FRONTEND=noninteractive 

# update apps on the base image
RUN apt-get -y update && apt-get install 

# install dependencies
RUN apt-get -y install python3 pip python3-opencv

# install opencv python module
RUN pip3 install opencv-python
RUN pip3 install Pillow

#copy current directory to docker container
COPY . ./data
WORKDIR /data

#add entrypoint
#ENTRYPOINT [ "./entrypoint.sh", "IMG_4570.JPG" ]
COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
