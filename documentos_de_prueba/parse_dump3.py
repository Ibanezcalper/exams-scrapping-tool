from bs4 import BeautifulSoup

with open('post_check_dump_q1.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

qp = soup.find(id="question-prompt")
if qp:
    for i, sibling in enumerate(qp.find_next_siblings()):
        print(f"Sibling {i}: name={sibling.name}, class={sibling.get('class')}")
        print(f"Content: {sibling.prettify()[:300]}")

