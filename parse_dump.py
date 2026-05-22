from bs4 import BeautifulSoup
import json

with open('post_check_dump_q1.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("ID question-prompt:")
qp = soup.find(id="question-prompt")
if qp:
    print(qp.text.strip())

print("\nOptions:")
# Check possible selectors
print("ul aria-labelledby='question-prompt':", len(soup.select("ul[aria-labelledby='question-prompt'] > li")))
print("div mc-quiz-answer:", len(soup.select("div[class*='mc-quiz-answer']")))
print("label mc-quiz-answer:", len(soup.select("label[class*='mc-quiz-answer']")))

# The options might be listed as correct/incorrect after checking.
# Let's search for the text of one of the options. "Amazon RDS" or similar.
# Let's find any list item that is a multiple choice option.
opts = soup.select("ul > li div[data-purpose*='safely-set-inner-html']")
if not opts:
    opts = soup.select("div[class*='mc-quiz-answer']")
if not opts:
    opts = soup.select("div[data-purpose='answer-content']") # Example data-purpose
for i, o in enumerate(opts):
    print(f"Opt {i+1}: {o.text.strip()[:50]}")

# Maybe just find all 'li' under 'ul' that are inside the 'question-result' div?
q_result = soup.select_one("div[class*='question-result']")
if q_result:
    print("q_result found!")
    for li in q_result.select("li"):
        print("li:", li.text.strip()[:50])

