from LinkedIn.modules import *

def login(browser, email, password, delay=10):
    ''' To Login LinkedIn Account '''
    
    url = 'https://www.linkedin.com/login'
    try:
        browser.get(url)
        username = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='username']")))
        username.send_keys(email)
        passwd = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        passwd.send_keys(password)
        submit = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, "//button[@type='submit']")))
        submit.click()

        cur_url = browser.current_url
        if 'feed' not in cur_url:
            print('Check Your Username & Password!!!')
            return

        return email

    except TimeoutException as exc:
        print(f'TimeOutError : {exc}')


def logout(browser):
    ''' To Logout LinkedIn Account '''
    url = 'https://www.linkedin.com/m/logout/'
    browser.get(url)