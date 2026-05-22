from bs4 import BeautifulSoup
import json

with open('post_check_dump_q1.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

options_soup = soup.select("ul[aria-labelledby='question-prompt'] > li")
if not options_soup:
    options_soup = soup.select("label[class*='mc-quiz-answer--answer']")
if not options_soup:
    qp = soup.find(id="question-prompt")
    if qp:
        for sibling in qp.find_next_siblings():
            options_soup = sibling.select("div[data-purpose='answer']")
            if options_soup:
                break

for o_idx, opt in enumerate(options_soup):
    body_div = opt.select_one("div[class*='mc-quiz-answer--answer-body'], div[data-purpose='answer-body']")
    opt_text = ""
    if body_div:
        text_div = body_div.select_one("div[class*='rt-scaffolding']") if "answer-body" in body_div.get("data-purpose", "") else None
        opt_text = text_div.get_text(separator="\n", strip=True) if text_div else body_div.get_text(separator="\n", strip=True)
    else:
        opt_text = opt.get_text(separator="\n", strip=True)
    
    inner_html = str(opt)
    is_correct = "Correct" in inner_html or "Correct selection" in inner_html or "ud-text-success" in inner_html
    print(f"Opt {o_idx+1}: {opt_text[:60]}... Correct? {is_correct}")

