import requests
from bs4 import BeautifulSoup


# ----------------------- 1. Stackoverflow 시작 --------------------------------
# 마지막 페이지 번호를 return하는 함수
# 페이지 번호를 찾아서 이걸 url에 이용
def stack_last_page(search_word):
    url = f"https://stackoverflow.com/jobs?r=true&q={search_word}"
    stack_result = requests.get(url)
    soup = BeautifulSoup(stack_result.text, "html.parser")
    pagination = soup.find("div", {"class": "s-pagination"}).find_all("a")
    page_num = []
    for data in pagination:
        page = data.get_text(strip=True)
        try:
            page = int(page)
            page_num.append(page)
        except:
            continue

    return page_num[-2]  # [-2]  # 맨 마지막 요소는 next라서 그 앞의 요소를 가져옴


# 마지막 페이지 번호를 찾았으니
# url마다 내가 원하는 자료를 찾아오는 함수
def get_stack_info(last_page_num, search_word):
    stack_job_list = []

    for page in range(last_page_num):
        url = f"https://stackoverflow.com/jobs?q={search_word}&r=true&pg={page+1}"
        stack_result = requests.get(url)
        soup = BeautifulSoup(stack_result.text, "html.parser")
        job_box = soup.find_all("div", {"class": "-job"})

        for data in job_box:
            try:
                base = data.find("a", {"class": "s-link stretched-link"})
                title = base['title'].strip()
                link = base['href'].strip()
                link = "https://stackoverflow.com" + link
                company = data.find(
                    "h3", {"class": "fc-black-700"}).find("span").get_text(strip=True)
            except:
                continue
            info = {
                'title': title,
                'company': company,
                'link': link
            }
            stack_job_list.append(info)
    return stack_job_list


def stackoverflow_scrapper(search_word):
    last_page = stack_last_page(search_word)
    stack_result = get_stack_info(last_page, search_word)
    return stack_result

# ----------------------- 1. Stackoverflow 끝--------------------------------

# ----------------------- 2. wework 시작 --------------------------------


def wework_scrapper(search_word):
    url = f"https://weworkremotely.com/remote-jobs/search?term={search_word}"
    wework_result = requests.get(url)
    soup = BeautifulSoup(wework_result.text, "html.parser")
    job_box = soup.find_all("li", {"class": "feature"})
    wework_job_list = []

    for data in job_box:
        try:
            company = data.find("span", {"class": "company"}).string.strip()
            title = data.find("span", {"class": "title"}).string.strip()
            link = data.select_one('span.company').parent
            link = link['href']
            link = "https://weworkremotely.com" + link
        except:
            continue

        info = {
            'title': title,
            'company': company,
            'link': link
        }

        wework_job_list.append(info)
    return wework_job_list
# ----------------------- 2. wework 끝 ----------------------------------

# ----------------------- 3. remoteok 시작 --------------------------------


def remoteok_scrapper(search_word):
    url = f"https://remoteok.io/remote-dev+{search_word}-jobs"
    remoteok_result = requests.get(url)
    remoteok_soup = BeautifulSoup(remoteok_result.text, "html.parser")
    job_box = remoteok_soup.find_all("tr", {"class": "job"})
    remoteok_job_list = []

    for data in job_box:
        title = data.find("h2", {"itemprop": "title"}).string.strip()
        company = data['data-company'].strip()
        link = data['data-url']
        link = "https://remoteok.io" + link

        info = {
            'title': title,
            'company': company,
            'link': link
        }
        remoteok_job_list.append(info)
    return remoteok_job_list
# ----------------------- 3. remoteok 끝 ----------------------------------
