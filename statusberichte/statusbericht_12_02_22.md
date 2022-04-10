# Statusbericht Studienarbeit 12.02.22

## Aktueller Stand

- Verarbeitung von Videos über ein Kommandozeilenprogramm
- Verarbeitung von Einzelbildern über ein Kommandozeilenprogramm
- Detailiertes Logging der dedektierten Objekte in ein CSV-File

- Auszug über die Verwendung des Kommandozeilenprogramms:

```
usage: yolo_od.py [-h] [-c CONFIDENCE] [-t THRESHOLD] [-m {video,image}] [-o OUTPUT] [-b BATCH_SIZE] [-v] [--record-detections] file

positional arguments:
  file                  Path to image or video file

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIDENCE, --confidence CONFIDENCE
                        Minimum probability to filter weak detections
  -t THRESHOLD, --threshold THRESHOLD
                        Threshold for Non-Maximum-Surpression (NMS)
  -m {video,image}, --mode {video,image}
                        Mode of operation: video or image
  -o OUTPUT, --output OUTPUT
                        Output folder
  -b BATCH_SIZE, --batch-size BATCH_SIZE
                        Batch size for inference. Only possible for video mode
  -v, --verbose         Enable verbose output
  --record-detections   Enable detection logging
```

## Nächste Schritte

1. Anwendung selbst trainierter Gewichte (Deutsche Verkehrsschilder)
2. Performance-Verbesserung
3. Dokumentation (in den letztn 14-Tagen vor Abgabe)
   - Ausschließlich technische Dokumentation
   - Aufsetzen auf fabrikneuem nano von 0 bis 100
   - Konfiguration und Parameter
   - KEINE THEORIE
   - Von Windows und Linux her Aufsetzung

## Fragen

- Aktuell keine Fragen
- Es soll lediglich der aktuelle Stand besprochen und die nächsten Schritte geplant werden

## Benötigte Materialien

- Aktuell werden keine Materialien benötigt
