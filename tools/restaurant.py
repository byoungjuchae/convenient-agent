from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from .utils.admin_state import State
from .utils.util import KAKAO_API_KEY,llm
import psycopg2
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

conn = psycopg2.connect(
    host='postgres',
    dbname='airflow',
    user='airflow',
    password='airflow',
    port=5432
)

cur = conn.cursor()
create_table_sql = """CREATE TABLE IF NOT EXISTS users2(
                    id TEXT,
                    place_category TEXT,
                    place_name TEXT,
                    place_url TEXT,
                    place_id INTEGER,
                    place_phone TEXT,
                    rating TEXT,
                    total_reviewers INTEGER,
                    blogging INTEGER,
                    mobile_site TEXT,
                    time_schedule TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                    );
"""

create_table_accomodation = """CREATE TABLE IF NOT EXISTS accomodation2(
                    id TEXT,
                    place_category TEXT,
                    place_name TEXT,
                    place_url TEXT,
                    place_id INTEGER,
                    place_phone TEXT,
                    rating TEXT,
                    total_reviewers INTEGER,
                    blogging INTEGER,
                    mobile_site TEXT,
                    created_at TIMESTAMPTZ DEFAULT NOW()
                    );
"""
cur.execute(create_table_sql)
cur.execute(create_table_accomodation)
conn.commit()

def selenium_setting():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("no-sandbox")
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu") 
    options.add_argument("lang=ko_KR")    
    options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    
    return options


@tool
async def accomodation_search(keyword: str):
    "if you have to find the accomodation, use this tool. the input keyword is related to the accomodation. keyword must be korean."
    headers = {"Authorization":f"KakaoAK {KAKAO_API_KEY}"}

    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

    response = requests.get(url,headers=headers,params={f"query":{keyword}})


    if response.status_code == 200:
        names = []
        website = []
        documents = []
        information = []
        infor = {}
        address = response.json().get('documents')
    
        for i in range(5):

            options = selenium_setting()
            driver = webdriver.Chrome(options=options)
  
            driver.get(address[i].get('place_url'))
            wait = WebDriverWait(driver, 15)

            time.sleep(3)
            rating = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/a/span/span[2]').text
            total_reviewers = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[2]/a/span[2]').text
            total_blogging = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[3]/a/span[2]').text

            mobile_web = f"https://map.kakao.com/link/map/{address[i].get('id')}"
    
            now = time.localtime()
            cur.execute("""INSERT INTO accomodation2 (id, place_category, place_name, place_url, place_id, place_phone, rating, total_reviewers, blogging, mobile_site, created_at) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                        ('1213',address[i].get("category_name"), address[i].get("place_name"), address[i].get("place_url"), int(address[i].get("id")), 
                        address[i].get("phone"), rating, total_reviewers, int(total_blogging), mobile_web, time.strftime('%Y%m%d',now)))
            
            conn.commit()
            driver.quit()
            information.append({"place_name":address[i].get('place_name'),"place_url":address[i].get('place_url'),"rating":rating,"total_reviewers":total_reviewers,"blogging":total_blogging,"mobile_web":mobile_web})

        return information

    else:
        return None


@tool
async def place_search(keyword:str):
    "if you have to find the restaurants, use this tool. the input keyword is related to the food. keyword must be korean."
    
    headers = {"Authorization":f"KakaoAK {KAKAO_API_KEY}"}
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'

    response = requests.get(url,headers=headers,params={f"query":{keyword}})
    

    if response.status_code == 200:

        names = []
        website = []
        documents = []
        information = []
        infor = {}
        address = response.json().get('documents')
    
        for i in range(5):
            
            options = selenium_setting()
            driver = webdriver.Chrome(options=options)
            driver.get(address[i].get('place_url'))
            wait = WebDriverWait(driver, 15)
      
            btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn_fold2[aria-controls='foldDetail2']")))
            if btn.get_attribute("aria-expanded") != "true":
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)  
            panel = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#foldDetail2")))

            time.sleep(3)
            mobile_web =  f"https://map.kakao.com/link/map/{address[i].get('id')}"
            rating = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/a/span/span[2]').text
            total_reviewers = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[2]/a/span[2]').text
            total_blogging = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[3]/a/span[2]').text

            ###### 광고 제외시키는 module 만들기. 블로거 내돈내산 아닌거 제외해서 허수 줄이기. 


            now = time.localtime()
            cur.execute("""INSERT INTO users2 (id, place_category, place_name, place_url, place_id, place_phone, rating, total_reviewers, blogging, mobile_site, time_schedule, created_at) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """,
                        ('1213', address[i].get("category_name"), address[i].get("place_name"), address[i].get("place_url"), int(address[i].get("id")), address[i].get("phone"), rating,
                        total_reviewers, int(total_blogging), mobile_web, panel.text, time.strftime('%Y%m%d',now)))
            
            conn.commit()
            driver.quit()
            information.append({"place_name":address[i].get('place_name'),"place_url":address[i].get('place_url'),"rating":rating,"total_reviewers":total_reviewers,"blogging":total_blogging,"mobile_web":mobile_web})
  
        return information

    else:
        return None


async def rest_accomodation(state: State):


    AR_agent = create_react_agent(llm,tools=[place_search,accomodation_search],
                                    prompt =("you are a assistant to run the plan."
                                            "if you want to search the place that user want, use the place_search tool. input is the keyword of the restaurant"
                                            "if you want to search about the accomodation, use the accomodation_search tool. input is the keyword of the accomodation"
                                            "you have to translate the answer into language of user's query."))
    chunks = []

    async for chunk in AR_agent.astream({"messages":state['plan']}):
        chunks.append(chunk)
        print(chunk)

    state['restaurant'] = chunks[-1]

    return state