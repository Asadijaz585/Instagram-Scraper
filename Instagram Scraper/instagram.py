import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from sqlalchemy import create_engine
from  sqlalchemy.orm import scoped_session ,sessionmaker
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
# , options=chrome_options

chrome_path = 'chromedriver'
driver = webdriver.Chrome(chrome_path)
driver.get('https://www.instagram.com/')
time.sleep(3)
driver.find_element(By.XPATH,"(//form[@id='loginForm']/div/div/div/label/input)[1]").send_keys('testing.second.dev@gmail.com')
time.sleep(5)
driver.find_element(By.XPATH,"(//form[@id='loginForm']/div/div/div/label/input)[2]").send_keys('Spiderhunts.123')
time.sleep(5)
driver.find_element(By.XPATH,"(//button[@class='_acan _aiit _acap _aijb _acas _aj1-'])").click()
time.sleep(5)
keyword = 'islam'
driver.get('https://www.instagram.com/{}'.format(keyword))
time.sleep(3)
driver.find_element(By.XPATH,"(//div[@class='_aacl _aacp _aacu _aacx _aad6 _aade'])[3]").click()
time.sleep(4)

while len(driver.find_elements(By.XPATH, "//div[@class='xt0psk2']/a")) > 0:
    options = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@class='_aano']")))
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', options)
    if len(driver.find_elements(By.XPATH, "//div[@class='xt0psk2']/a")) % 2 != 0:
        break

Following=[]
for url in driver.find_elements(By.XPATH, "//div[@class='xt0psk2']/a"):
    Following.append(url.get_attribute("href"))
    time.sleep(3)

engine = create_engine('mysql+pymysql://root@localhost/scraping')
db = scoped_session(sessionmaker(bind=engine))

for user in Following:
    driver.get(user)
    time.sleep(2)
    try:
        name = driver.find_element(By.XPATH, "//h2[@class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x4zkp8e xw06pyt x10wh9bi x1wdrske x8viiok x18hxmgj']").text
    except:
        name = " - "
    try:
        posts = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[1]").text
    except:
        posts = " - "
    try:
        followers = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[2]").text
    except:
        followers = " - "
    try:
        following = driver.find_element(By.XPATH, "(//span[@class='_ac2a'])[3]").text
    except:
        following = " - "
    try:
        sql = "INSERT INTO `insta_record` (`name`,`posts`,`followers`,`following`) VALUES ('{}','{}','{}','{}')".format(name,posts,followers,following)
    except:
        sql = " - "
    db.execute(sql)
    db.commit()
    print("inserted")