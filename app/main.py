# SPDX-FileCopyrightText: Copyright (C) ARDUINO SRL (http://www.arduino.cc)
#
# SPDX-License-Identifier: MPL-2.0

from arduino.app_utils import App
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection
from datetime import datetime, UTC

# Initialize the Web UI
ui = WebUI()

# Initialize the Object Detection Stream
# By default, this looks for the 'EI_OBJ_DETECTION_MODEL' variable from your YAML
detection_stream = VideoObjectDetection(confidence=0.5, debounce_sec=0.0)

# Allow the UI to adjust the threshold slider
ui.on_message("override_th", lambda sid, threshold: detection_stream.override_threshold(threshold))

# Register a callback for when objects are detected
def send_detections_to_ui(detections: dict):
    for key, value in detections.items():
        entry = {
            "content": key,
            "confidence": value.get("confidence"),
            "timestamp": datetime.now(UTC).isoformat()
        }
        # Send the detection data to the Web Interface
        ui.send_message("detection", message=entry)

# Link the detection event to the callback function
detection_stream.on_detect_all(send_detections_to_ui)

# Run the Application
App.run()
