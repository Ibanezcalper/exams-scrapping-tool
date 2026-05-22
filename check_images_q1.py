import json
import os
import hashlib

with open('examen_completo.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

q1 = data['examen_1']['preguntas'][0]
images = q1.get('imagenes_explicacion', [])
print(f"Total explanation images in Q1: {len(images)}")

for img in images:
    if os.path.exists(img):
        size = os.path.getsize(img)
        with open(img, "rb") as f:
            h = hashlib.md5(f.read()).hexdigest()
        print(f"{img} - size: {size} - md5: {h}")
    else:
        print(f"{img} - NOT FOUND")
