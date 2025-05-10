
import cv2
import os
import requests
import numpy as np
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('API_KEY')
OCR_URL = 'https://api.ocr.space/parse/image'
FRAMES_DIR = os.environ.get('FRAMES_DIR')
OUTPUT_TEXT_FILE = os.environ.get('OUTPUT_TEXT_FILE')
LANG=os.environ.get('LANG_OCR')

# --- STEP 3: OCR Frames and Save Text ---
print("Running OCR...")
print(f"Lang {LANG}")

def ocr_space_image(image_path, lang='eng'):
    with open(image_path, 'rb') as f:
        r = requests.post(
            OCR_URL,
            files={'filename': f},
            data={'apikey': API_KEY, 'language': lang},
        )
    print(r)
    result = r.json()
    if result.get("IsErroredOnProcessing"):
        print(f"Error processing {image_path}: {result.get('ErrorMessage')}")
        return ""
    return result['ParsedResults'][0]['ParsedText']

# --- STEP 3: OCR Frames and Save Text (using OCR.Space) ---
print("Running OCR (OCR.Space API)...")
previous_text = None

frames = sorted(os.listdir(FRAMES_DIR))
for (i, frame_path) in enumerate(tqdm(frames)):
    text = ocr_space_image(os.path.join(FRAMES_DIR, frame_path), lang=LANG)  # use 'spa' for Spanish
    with open(OUTPUT_TEXT_FILE, 'a', encoding='utf-8') as f:
        f.write(text)

    print(f"✅ Frame {i} processed")




