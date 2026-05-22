from bs4 import BeautifulSoup

with open('post_check_dump_q1.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

qp = soup.find(id="question-prompt")
if qp:
    print("Found question-prompt. Siblings:")
    for sibling in qp.find_next_siblings():
        if sibling.name == 'ul':
            print("Found a UL sibling!")
            print(sibling.prettify()[:500])
        else:
            print("Sibling class:", sibling.get('class'))
            
    print("\nLooking for any ul inside question-result:")
    qr = soup.select_one("div[class*='question-result--question-result']")
    if qr:
        for ul in qr.find_all('ul'):
            print("UL class:", ul.get('class'))
            li_list = ul.find_all('li')
            print("List items:", len(li_list))
            if li_list:
                print("First list item:", li_list[0].text[:100])

