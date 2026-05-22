from bs4 import BeautifulSoup

with open('page_dump.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

print("UL count:", len(soup.select("ul[aria-labelledby='question-prompt'] > li")))
print("Label count:", len(soup.select("label[class*='mc-quiz-answer--answer']")))
