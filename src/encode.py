import json
import numpy as np
from PIL import Image
import cv2
import os
import base64

frame_width = 1920
frame_height = 1080
pixels_per_frame = frame_width * frame_height
fps = 8

with open('data/data.json', 'r') as json_file:
    json_data = json.load(json_file)

json_string = json.dumps(json_data)
bytes_data = json_string.encode('utf-8')
base64_encoded = base64.b64encode(bytes_data)

bit_string = ''.join(format(byte, '08b') for byte in base64_encoded)

total_bits = len(bit_string)
total_frames = (total_bits + pixels_per_frame - 1) // pixels_per_frame

output_folder = 'frames'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

frames = 0
while frames < total_frames:
    image_matrix = np.zeros((frame_height, frame_width), dtype=np.uint8)

    for y in range(frame_height):
        for x in range(frame_width):
            bit_index = frames * pixels_per_frame + y * frame_width + x
            if bit_index < total_bits:
                pixel_value = int(bit_string[bit_index])
                image_matrix[y, x] = pixel_value * 255

    image = Image.fromarray(image_matrix)
    image.save(f'{output_folder}/frame_{frames:04d}.png')

    frames += 1

image_files = sorted([f for f in os.listdir(output_folder) if f.startswith("frame_")])

# Create the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('output/output_video.mp4', fourcc, fps, (frame_width, frame_height), isColor=False)

for image_file in image_files:
    frame = cv2.imread(os.path.join(output_folder, image_file), cv2.IMREAD_GRAYSCALE)
    video.write(frame)

for i in image_files:
    os.remove(os.path.join(output_folder, i))

video.release()
