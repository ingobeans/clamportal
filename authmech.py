from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

import clam

class Authmech:
    AT_SCHOOL=0
    MICROSOFT=1

def login_authmech_school(username,password)->dict:
    session = requests.Session()
    session.auth = HttpNtlmAuth(username, password)
    portal1 = first_skolportal()
    hag_cookies = parse_cookies(portal1.headers["Set-Cookie"])
    print("got skolportalen session")
    portal2 = second_skolportal(hag_cookies)
    portal3 = third_skolportal(hag_cookies, session)
    if portal3.status_code == 401:
        raise ValueError("Invalid credentials using School Authmech")
    print("authenticated skolportalen")
    return hag_cookies

def login_authmech_microsoft(email,password)->dict:
    options = Options()
    options.add_argument("--headless=new")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options)

    driver.get("https://skolportal.uppsala.se/wa/auth?authmech=uf9yulgic7b4")

    wait = WebDriverWait(driver, 5)

    email_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[type=email]")))
    email_element.send_keys(email)
    wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "win-button"))).click()
    
    password_element = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, "input[type=password]")))
    password_element.send_keys(password)
    wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".win-button[value=\"Sign in\"]"))).click()
    

    try:
        wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".win-button[value=\"Yes\"]"))).click()
        wait.until(ec.url_contains("desktop.html"))
    except:
        raise ValueError("Invalid credentials using Microsoft Authmech")
    cookies = {key: driver.get_cookie(key)["value"] for key in ["WAAK_HAG_SN","WASID_HAG_SN"]}
    #driver.close()
    return cookies
    
    

if __name__ == "__main__":
    with open("config.txt","r") as f:
        config = f.read().split("\n")
        username = config[0]
        password = config[1]
    login(username,password)