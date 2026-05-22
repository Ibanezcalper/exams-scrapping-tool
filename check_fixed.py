import json

with open('examen_completo_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

q1 = data['examen_1']['preguntas'][0]
print("Q1 Correct options:")
for i, opt in enumerate(q1['opciones']):
    if opt['es_correcta']:
        print(f"  [{i}] {opt['texto'][:30]}... | Imgs: {opt.get('imagenes', [])}")
print("Q1 Explanation images:", q1.get('imagenes_explicacion', []))
