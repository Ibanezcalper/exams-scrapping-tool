from bs4 import BeautifulSoup

with open('post_check_dump_q1.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

qp = soup.find(id="question-prompt")
if qp:
    for sibling in qp.find_next_siblings():
        # find all answers
        answers = sibling.select("div[data-purpose='answer']")
        if not answers:
            answers = sibling.select("div[class*='answer-result-pane']")
        print(f"Found {len(answers)} answers.")
        for i, ans in enumerate(answers):
            print(f"--- Option {i+1} ---")
            print(ans.prettify()[:500])
