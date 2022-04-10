# Statusbericht Studienarbeit 27.11.21

## Aktueller Stand

- Grundsätzliche Funktionalität der Beispielimplementierung aus dem Github Repository https://github.com/ChiekoN/yolov3_opencv geprüft
- Tests mit den beigefügten Beispielbildern aus dem Repository durchgeführt
- Kleinere Anpassungen durchgeführt, da der Sourcecode zu Beginn nicht lauffähig war
- Aufsetzen des Nvidia Jetson Nano Boards
- Setup des YOLO (ROS) Docker Containers auf dem Embedded-Board
- Erstellung eines Dockerfiles mit allen Dependencies der Anwendung

## Nächste Schritte

- Adaption des Algorithmus zur Verarbeitung von Videos
- Aufzeichung des Ergebnis-Videostreams

## Fragen

- Soll ein update von ROSv1 auf ROSv2 durchgeführt werden?
- Mit dem Standard Datensatz von COCO werden 80 Klassen erkannt, darunter sind die geforderten Klassen. Nach aktuellem Kenntnissstand müsste das Netz neu trainiert werden, um nur die geforderten Klassen zu erkennen und keine anderen. Ist das von Nöten oder reich eine Filterung im Postprocessing aus?

## Benötigte Materialien

- Leider war das Video von der Fahrt durch Mosbach nicht auf dem Beigefügten USB Sticks. Ich benötige dieses noch um Videos zu verarbeiten.