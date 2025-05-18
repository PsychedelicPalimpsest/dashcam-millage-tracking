import cv2
import pytesseract
import numpy as np
import time
import json
from concurrent.futures import ThreadPoolExecutor
import os


from CONFIG import Y_START, Y_END, X_LOC_END, TIME_START, INTERVAL

# Optimize Tesseract configuration
custom_config = r'--oem 1 --psm 7 -c tessedit_char_whitelist=0123456789WN.:/ '

def process_frame(frame_data):
    """Process a single frame and extract text"""
    frame_number, timestamp, frame = frame_data
    
    # Process image for OCR
    cropped = frame[Y_START:Y_END, :]
    contrasted = cv2.convertScaleAbs(cropped, alpha=2, beta=-400)
    gray = cv2.cvtColor(contrasted, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
    
    # Extract regions
    location_img = bw[:, :X_LOC_END]
    time_img = bw[:, TIME_START:]
    
    
    # Perform OCR
    location = pytesseract.image_to_string(location_img, lang='eng', 
                                          config=custom_config).strip()
    time = pytesseract.image_to_string(time_img, lang='eng', 
                                      config=custom_config).strip()
    
    return {
        "frame": frame_number,
        "timestamp": timestamp,
        "location": location.replace("W", " ").replace("N", " ").replace("  ", " ").split(" "),
        "time": time
    }


def process_video(vid):
    cap = cv2.VideoCapture(vid)
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    frame_interval = int(fps * INTERVAL)
    
    print(f"Video FPS: {fps}, Duration: {duration:.2f}s")
    print(f"Processing one frame every {frame_interval} frames ({INTERVAL} seconds)")
    
    # Prepare frames for processing
    frames_to_process = []
    
    for frame_number in range(0, total_frames, frame_interval):
        # Set frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        
        if not ret:
            break
            
        # Calculate timestamp
        timestamp = frame_number / fps
        frames_to_process.append((frame_number, timestamp, frame))
    
    cap.release()
    
    # Process frames using ThreadPoolExecutor with 10 workers
    results = []
    start_time = time.time()
    
    print("Starting bulk ocr")

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(process_frame, frame_data) 
                  for frame_data in frames_to_process]
        
        # Collect results as they complete
        for future in futures:
            try:
                result = future.result()
                results.append(result)
                print(f"Processed frame {result['frame']} - {result['location']} {result['date']}")
            except Exception as e:
                print(f"Error processing frame: {e}")
    
    # Sort results by frame number
    results.sort(key=lambda x: x['frame'])
    
    return results