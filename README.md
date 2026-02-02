# smart_helmet

This project is a smart road monitoring and accident detection system to improve rider safety and promote traffic rule compliance on Indian roads. It combines edge AI computer vision with crash detection to address key issues: poor road conditions, helmet non-compliance, and faulty street lighting.

The system has two independent main workflows:

1. **Road Intelligence Workflow (Edge AI Vision)**  
   - Uses a forward-facing webcam to capture real-time road video.  
   - Runs **YOLO** locally on a connected smartphone or laptop (**pure edge AI** — no internet required for detection).  
   - Detects:  
     - **Potholes** (or large road defects/uneven surfaces).  
     - **Helmet violations** — checks if the rider (self) or nearby/oncoming two-wheeler riders are wearing helmets.  
     - **Non-working streetlights** — detects streetlights and checks if they are off/non-functional (no visible glow/illumination, especially useful at night/dusk).  
   - On detection:  
     - Pothole → geo-tags with GPS and queues for cloud upload.  
     - No helmet on detected rider → logs violation (type, GPS, timestamp) to cloud for traffic police/authorities.  
     - Non-working streetlight → logs fault (type: "streetlight_off", GPS, timestamp) to cloud for municipal/electricity board repair teams.  
   - **Key advantage**: All detection (potholes, helmets, streetlights) is **edge AI** — fully functional offline in no-network areas. Uploads are queued locally and sent automatically when connectivity is available.

2. **Crash Detection & Emergency Workflow**  
   - Handled by **Arduino Uno Q** + gyroscope.  
   - Detects sudden impacts or excessive tilts (e.g., fall/crash).  
   - Triggers a 60-second "Golden Minute" grace period: buzzer beeps + LED matrix countdown.  
   - Rider presses cancel button if safe.  
   - If no cancel → assumes unconscious → sends WiFi signal to phone → phone auto-sends email + call to emergency contacts with current GPS.

The system is powered by a portable **power bank** and mounts easily on a two-wheeler.

## Features

- Real-time **edge AI** detection of potholes, helmet violations, and non-working streetlights (100% offline capable).  
- Violation/hazard logging to cloud (Firebase): potholes, no-helmet cases, faulty streetlights — authorities can access a map/dashboard for repairs and enforcement.  
- Crash/fall detection with user-cancelable emergency alert.  
- Automated SOS: email + call with GPS on confirmed crash.  
- Low-cost, portable, two-wheeler optimized.

## Hardware Requirements

- Arduino Uno Q (built-in WiFi + LED matrix)  
- Gyroscope 
- buzzer  
- Push button (SOS cancel)  
- Optional status LED  
- Power bank (5V, ≥10,000 mAh)  
- USB webcam (Logitech or any compatible)  
- Smartphone (Android preferred) or small laptop/tablet with USB-OTG  
- Jumper wires, mounting hardware/enclosure  


## Hardware Connections

- **Gyroscope** → Arduino: VCC → 3.3V/5V, GND → GND, SCL → A5, SDA → A4  
- **Buzzer** → D8 (+) , GND (-)  
- **Cancel Button** → D7 (pull-up enabled), GND  
- **Optional LED** → D9 (with 220Ω resistor) → GND  
- **Power**: Power bank USB → Arduino USB  
- **Webcam** → Phone USB-OTG (not to Arduino)  
- **WiFi**: Arduino → phone hotspot/local network (for SOS only)

Mount webcam forward (road + streetlights view), gyroscope firmly on frame.

## Software Requirements

- **Arduino IDE** → crash sketch  
- **Python 3.8+** → edge AI vision (on phone/laptop)  
- Libraries: `ultralytics` (YOLO), `opencv-python`, `firebase-admin`/`pyrebase`, GPS via `geocoder`/`plyer`  
- **Cloud**: Firebase Realtime Database (free tier)  
- Optional: Termux on Android for running Python script

## Repository Structure (Assumed)

```
smart_helmet/
├─ requirements.txt
├── README.md
├── license.txt
├── model/
│   └── helmet.eim
│   └── model_pothole.eim
│   └── streetlight.eim
├── app/
│   ├── main.py           
│   ├── sketch.ino
│   └── app.yaml
│   └──sketch.yaml                   
```

## Implementation Steps

1. **Hardware Assembly**  
   Follow connections. Test gyro/buzzer/button via Arduino Serial Monitor.

2. **Crash Workflow (Arduino)**  
   - Upload `crash_detection.ino`  
   - Set: tilt/impact thresholds, WiFi (phone hotspot), phone IP/port for SOS POST  
   - Behavior: monitor gyro → trigger → countdown + buzzer → cancel? → else SOS via WiFi

3. **Edge AI Vision Workflow (Python on Phone/Laptop)**  
   - Install: `pip install -r requirements.txt`  
   - Use YOLOv8/YOLOv11 model (fine-tuned or combined):  
     - **Pothole** detection (use public pothole datasets/models)  
     - **Helmet** detection (rider class → helmet / no-helmet subclasses; many open helmet datasets on Roboflow/Kaggle)  
     - **Streetlight** detection + status:  
       - Detect "streetlight" class (use Roboflow streetlight datasets or traffic light models adapted)  
       - For status: simple post-processing — check if detected light has bright glow/region (e.g., high brightness in bounding box at night) or use a secondary classifier/light detection. If no glow → classify as "off/faulty"  
       - Many research papers (2024–2025) show YOLO variants successfully detect streetlight condition/operation via brightness analysis or custom classes (on/off/faulty).  
   - In `edge_detection.py`:  
     - OpenCV webcam capture  
     - YOLO inference (local/edge — no net needed) every few frames  
     - On pothole: queue GPS + upload  
     - On no-helmet rider: queue violation `{ "type": "helmet_violation", "lat": ..., "lon": ..., "ts": ... }`  
     - On streetlight + faulty/off: queue `{ "type": "streetlight_fault", "subtype": "off", "lat": ..., "lon": ..., "ts": ... }`  
   - Run continuously during rides (Termux or laptop)

4. **Cloud & Notifications**  
   - Firebase stores: potholes, helmet violations, streetlight faults (authorities build map/dashboard)  
   - SOS: phone gets Arduino signal → `smtplib` email + call integration (Android intent/Twilio/IFTTT)

5. **Offline Behavior**  
   - Detection (potholes, helmets, streetlights) → fully edge AI → works with **zero network**  
   - Uploads → queued locally → sent when connected

## Testing

- Tilt Arduino → verify countdown/buzzer/SOS  
- Show pothole images → check detection/upload  
- Show riders with/without helmet → check violation log  
- Show streetlights (on vs off, day/night) → check fault logging  
- Disconnect internet → confirm all detections continue

## Future Improvements

- Fine-tune YOLO on Indian roads (potholes + helmets + streetlights night/day)  
- Add number plate recognition for violations  
- Improve streetlight status: use brightness thresholding or dedicated light-on model  
- Build simple web dashboard for authorities  
- Mobile app wrapper for easier phone usage

Safe rides, better roads, and well-lit nights! 🪖🚀🌃
