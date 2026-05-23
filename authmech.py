from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec

import clam

def login_authmech_school(username,password)->dict:
    """Attempt login with the "At School" authmech
    """
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

def login_authmech_microsoft(email,password,backend="chrome",persistent_login_cache_location=None)->dict:
    """Attempt login with Microsoft Authmech

    `backend` can be either: `chrome` or `firefox`.
    `persistent_login_cache_location` can be set to stay logged in, to make future logins faster.
    """
    options = Options()
    options.add_experimental_option("detach", True)
    #options.add_argument("--headless=new")

    if backend == "chrome":
        if persistent_login_cache_location:
            options.add_argument(f"user-data-dir={persistent_login_cache_location}")
        driver = webdriver.Chrome(options)
    elif backend == "firefox":
        if persistent_login_cache_location:
            options.profile = persistent_login_cache_location
        driver = webdriver.Firefox(options)
    else:
        raise ValueError("Unrecognized backend")

    driver.get("https://skolportal.uppsala.se/wa/auth?authmech=uf9yulgic7b4")

    wait = WebDriverWait(driver, 5)

    # figure out if microsoft login is required or if already logged in
    start_wait = wait.until(lambda driver :  "desktop.html" in driver.current_url or ec.presence_of_element_located((By.CSS_SELECTOR, "input[type=email]"))(driver) )
    if not "desktop.html" in driver.current_url:
        print("not already logged in, attempting log in now.")
        email_element = driver.find_element(By.CSS_SELECTOR, "input[type=email]")
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
    driver.close()
    return cookies
    