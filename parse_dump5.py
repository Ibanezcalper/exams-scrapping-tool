from bs4 import BeautifulSoup
import json

with open('post_check_dump_q1.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

qp = soup.find(id="question-prompt")
if qp:
    for sibling in qp.find_next_siblings():
        answers = sibling.select("div[data-purpose='answer']")
        if answers:
            for i, ans in enumerate(answers):
                body = ans.select_one("div[data-purpose='answer-body']")
                # inside body, there's the text div.
                text_div = body.select_one("div[class*='rt-scaffolding']") if body else ans
                text = text_div.get_text(separator="\n", strip=True) if text_div else ans.get_text(separator="\n", strip=True)
                print(f"Opt {i+1}: {text}")
                
                # is it correct?
                is_correct = "Correct answer" in ans.get_text()
                print(f"  Correct? {is_correct}")
