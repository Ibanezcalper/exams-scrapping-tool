import json
import os

with open('examen_completo.json', 'r') as f:
    data = json.load(f)

for exam, exam_data in data.items():
    for q in exam_data.get('preguntas', []):
        if q.get('imagenes_pregunta'):
            print(f"Pregunta img: {q['imagenes_pregunta']}")
            break
    break

print("Checking imagenes_examen folder:")
print(os.listdir('imagenes_examen')[:5])
