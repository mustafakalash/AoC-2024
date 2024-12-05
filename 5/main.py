class PageRule:
    _page_rules = []

    def __init__(self, page, before):
        self.page = page
        self.before = before
        PageRule._page_rules.append(self)

    @staticmethod
    def get_rules(page):
        rules = []
        for rule in PageRule._page_rules:
            if rule.page == page:
                rules.append(rule)

        return rules

    @staticmethod
    def is_correct(pages):
        for i, page in enumerate(pages):
            rules = PageRule.get_rules(page)
            for rule in rules:
                if rule.before in pages[:i]:
                    print(f"{pages} breaks rule {page}|{rule.before}")
                    return False, page, rule.before
        
        print(f"{pages} is correct")
        return True, None, None
    
    @staticmethod
    def sort(pages, page, before):
        correct = False
        while not correct:
            pages.remove(page)
            pages.insert(pages.index(before), page)
            correct, page, before = PageRule.is_correct(pages)

        return pages
    
def get_middle(pages):
    return int(pages[len(pages)//2])

with open("5/input") as f:
    lines = f.readlines()

i = lines.index("\n")
rules, page_lists = lines[:i], lines[i+1:]

for rule in rules:
    PageRule(*rule.strip().split("|"))

p1_sum = p2_sum = 0
for page_list in page_lists:
    pages = page_list.strip().split(",")
    correct, page, before = PageRule.is_correct(pages)
    if correct:
        p1_sum += get_middle(pages)
    else:
        p2_sum += get_middle(PageRule.sort(pages, page, before))

print(f"Part 1: {p1_sum}\nPart 2: {p2_sum}")