import json
import cv2
import os
import base64

frame_width = 1920
frame_height = 1080
pixels_per_frame = frame_width * frame_height
fps = 8

output_folder = 'frames'

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoCapture('output/output_video.mp4')

bit_string = ''

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    bit_values = (frame_gray.flatten() > 128).astype(int)
    bit_string += ''.join(map(str, bit_values))

video.release()

# Remove padding bits
padding = len(bit_string) % 8
if padding > 0:
    bit_string = bit_string[:-padding]

# Convert bit string to bytes
byte_array = bytearray([int(bit_string[i:i + 8], 2) for i in range(0, len(bit_string), 8)])
base64_decoded = base64.b64decode(byte_array)

# Convert bytes to JSON
decoded_json = base64_decoded.decode('utf-8')
decoded_data = json.loads(decoded_json)

# Write the decoded data to results.json
with open('output/results.json', 'w') as json_file:
    json.dump(decoded_data, json_file, indent=4)
