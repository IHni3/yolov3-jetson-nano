FROM officinerobotiche/ros:foxy-ros-base-l4t-r32.4.4-cv-4.4.0

ENV DEBIAN_FRONTEND=noninteractive 

# install python modules
RUN pip3 install Pillow
RUN pip3 install termcolor
RUN pip3 install numpy

#copy current directory to docker container
COPY . .

#add entrypoint
COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
