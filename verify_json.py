import json

with open('examen_completo.json', 'r') as f:
    data = json.load(f)

print(f"Total exams: {len(data)}")
for exam, exam_data in data.items():
    print(f"Exam: {exam}")
    print(f"  Questions: {len(exam_data['preguntas'])}")
    if exam_data['preguntas']:
        q1 = exam_data['preguntas'][0]
        print(f"  Q1 Text: {q1['texto'][:100]}...")
        print(f"  Q1 Options Count: {len(q1['opciones'])}")
        for opt in q1['opciones']:
            print(f"    - {opt['texto'][:50]}... | Correct: {opt['es_correcta']}")
        print(f"  Q1 Explanation: {q1.get('explicacion', '')[:100]}...")
