import cv2
import os
import requests
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')
OCR_URL = 'https://api.ocr.space/parse/image'

# --- SETTINGS ---
VIDEO_PATH = os.environ.get('VIDEO_PATH')
FRAMES_DIR = os.environ.get('FRAMES_DIR')
OUTPUT_TEXT_FILE = os.environ.get('OUTPUT_TEXT_FILE ')
FRAME_RATE = 2                     # Frames per second to extract (adjust if needed)
BLACKNESS_TRASHOLD = 97.5         # Similarity to detect duplicate pages

# --- PREPARE ---
os.makedirs(FRAMES_DIR, exist_ok=True)

# --- STEP 1: Extract Frames ---
print("Extracting frames...")
cap = cv2.VideoCapture(VIDEO_PATH)
fps = cap.get(cv2.CAP_PROP_FPS)
interval = int(fps // FRAME_RATE)

def blackness_score(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Normalize pixel values to [0, 1] where 0 = black, 1 = white
    norm = gray / 255.0
    # Invert to get "blackness" where 1 = black
    blackness = 1.0 - norm
    # Compute average blackness and scale to 0–100
    score = np.mean(blackness) * 100
    return round(score, 2)


def is_duplicate(frameA, frameB):
    diff = cv2.bitwise_xor(frameA, frameB)
    return blackness_score(diff) > BLACKNESS_TRASHOLD

frame_idx = 0
saved_idx = 0
duplicates_removed = 0
success, frame = cap.read()
prev_frame = 'none'

while success:
    if frame_idx % interval == 0:
        frame_path = os.path.join(FRAMES_DIR, f"frame_{saved_idx:03d}.png")
        frame = cv2.resize(frame, (1400, 700))  # Normalize size
        if (frame_idx == 0) or (not is_duplicate(frame, prev_frame)):
            cv2.imwrite(frame_path, frame)
            saved_idx += 1
            print(f"{saved_idx} frame is saved")
        else:
            duplicates_removed += 1
            print(f"duplicated frame ignored")
        prev_frame = frame
    success, frame = cap.read()
    frame_idx += 1

cap.release()
print(f"{saved_idx} frames extracted.")
print(f"{duplicates_removed} duplicated frames ignored")

