# Notizen

## Interessante Links

- youtube.com/watch?v=MdF6x6ZmLAY
- github.com/ultralytics/yolov5/wiki/Train-Custom-Data

# Aufsetzen des Nvidia Jetson Boards

1.  Betriebssystem herunterladen von https://developer.nvidea.com/embedded/downloads
    oder direkt diesen Befehl ausführen:

         wget https://developer.nvidia.com/jetson-nano-sd-card-image-441

2.  Validieren des Downloard

        md5sum jetson-nano-sd-card-image-441

    Die erzeugte Checksumme sollte `a6853252de77324c4786e81cddb64182` entsprechen.

3.  Entpacken des Zip-Archivs (Das kann einige Zeit in Anspruch nehmen, da das Image über 10GB groß ist)

        unzip jetson-nano-sd-card-image-441

    Darin enthalten ist das Image mit dem Namen sd-blob-b01.img

4.  SD-Karte einführen
5.  Gerät lokalisieren

        sudo fdisk -l

6.  Verbindung zum Gerät entfernen (unmount)

        sudo unmount /dev/<insert-devicename>*

7.  Das Image auf die SD-Karte kopieren (Beachte die korrekte Partition auszuwählen)

        sudo dd bs=1M if=sd-blob-b01.img of=/dev/<insert-devicename>

8.  Entfernen der SD-Karte
9.  Einstecken der Micro-SD in das Jetson Nano Board
10. Stromkabel verbinden

## Aufsetzen des Docker Containers

1.  In dem Ordner des beigefügten Dockerfiles folgenden Befehl ausführen. Damit wird der Docker Container gebaut:

        sudo docker build . -t <container-name>

2.  Im zweiten Schritte kann der Docker Container ausgeführt werden. Über `-v` wird ein Volume erzeugt um die Daten die im Docker Container erstellt werden auf den Host zurück zu schreiben.

        sudo docker run -v $PWD:/data ros01

3.  Als Ergebnis sollte im aktuellen Ordner ein neues Bild zu sehen sein. Darin wurde eine Detektion durchgeführt.
