from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task
import requests




@task
def place_search(keyword:str):
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
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("no-sandbox")
            options.add_argument('window-size=1920x1080')
            options.add_argument("disable-gpu") 
            options.add_argument("lang=ko_KR")    
            options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
            driver = webdriver.Chrome(options=options)
            driver.get(address[i].get('place_url'))
            wait = WebDriverWait(driver, 15)
            btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn_fold2[aria-controls='foldDetail2']")))
            if btn.get_attribute("aria-expanded") != "true":
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)  
            panel = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#foldDetail2")))

            time.sleep(3)
     
            rating = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[1]/a/span/span[2]').text
            total_reviewers = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[2]/a/span[2]').text
            total_blogging = driver.find_element(By.XPATH,'//*[@id="mainContent"]/div[1]/div[1]/div[2]/div[3]/a/span[2]').text

            ###### 광고 제외시키는 module 만들기. 블로거 내돈내산 아닌거 제외해서 허수 줄이기. 

            infor['place_name'] = address[i].get("place_name")
            infor['place_url'] = address[i].get("place_url")
            infor['rating'] = rating
            infor['total_reviewers'] = total_reviewers
            infor['blogging'] =  total_blogging
            infor['time_schedule'] = panel.text

            now = time.localtime()
            cur.execute("""INSERT INTO users (id, place_name, place_url, rating, total_reviewers, blogging, time_schedule, created_at) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """,
                        ('1213',infor['place_name'],infor['place_url'],infor['rating'],int(infor['total_reviewers']),int(infor['blogging']),infor['time_schedule'],time.strftime('%Y%m%d',now)))
            
            conn.commit()
            driver.quit()
            information.append(infor)
  
        return information

    else:
        return None



with DAG(
    dag_id = "place_search",
    catchup = False,
    tags=['kakao']
) as dag:


    place_search = place_search.override()


    place_search
