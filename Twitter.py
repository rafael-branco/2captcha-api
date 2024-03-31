# Import necessary libraries
import json
import time
import requests
from seleniumbase import Driver
from selenium.webdriver.common.by import By

# Set up proxy and 2captcha API key
proxy = "uc672e6e756f805d0-zone-custom-region-rsa:uc672e6e756f805d0@43.152.113.55:2334"  # Your proxy here
my_key = "c572dad22c39c8dae2789529499e2b40"

# Initialize SeleniumBase driver
driver = Driver(uc=True, headless=False, proxy=proxy)

# Navigate to Twitter signup page
url = 'https://twitter.com/i/flow/signup'
driver.get(url)
time.sleep(8)

try:
    # Click on the signup button
    m = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/div/span/span")
    m.click()
    time.sleep(3)
    
    input('Enter any key to continue...')

    # # Fill in the registration form
    # driver.find_element(By.NAME, "name").send_keys("AlexStorm")  # Your desired username
    # while True:
    #     try:
    #         driver.find_element(By.NAME, "email").send_keys("mogyvh@mailbox.in.ua")  # Your working email
    #         break
    #     except:
    #         # Handle exception for email field not found, click on the alternative method
    #         driver.find_element(By.CSS_SELECTOR, "#layers > div:nth-child(2) > div > div > div > div > div > div.css-175oi2r.r-1ny4l3l.r-18u37iz.r-1pi2tsx.r-1777fci.r-1xcajam.r-ipm5af.r-g6jmlv.r-1awozwy > div.css-175oi2r.r-1wbh5a2.r-htvplk.r-1udh08x.r-1867qdf.r-kwpbio.r-rsyp9y.r-1pjcn9w.r-1279nm1 > div > div > div.css-175oi2r.r-1ny4l3l.r-6koalj.r-16y2uox.r-14lw9ot.r-1wbh5a2 > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-1jgb5lz.r-13qz1uu.r-1ye8kvj > div.css-175oi2r.r-16y2uox.r-1wbh5a2.r-1dqxon3 > div > div:nth-child(2) > div.css-1rynq56.r-bcqeeo.r-qvutc0.r-37j5jr.r-1ff274t.r-a023e6.r-rjixqe.r-16dba41 > span").click()

    # time.sleep(1)

    # # Fill in the birthdate details
    # driver.find_element(By.ID, "SELECTOR_1").send_keys("June")  # Month
    # driver.find_element(By.ID, "SELECTOR_2").send_keys("10")  # Day
    # driver.find_element(By.ID, "SELECTOR_3").send_keys("1999")  # Year
    # time.sleep(1)

    # # Click on the "Next" button
    # driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div").click()
    time.sleep(10)

    # Set up 2captcha parameters
    sitekey = "867D55F2-24FD-4C56-AB6D-589EDAF5E7C5"  # Twitter sitekey
    surl = "https://client-api.arkoselabs.com"

    data = {"key": my_key,
            "method": "funcaptcha",
            "json": 1,
            "publickey": sitekey,
            "pageurl": url,
            "surl": surl,
            "proxy": proxy,
            "proxytype": "HTTP",
            }

    # Make a request to 2captcha for solving the captcha
    response = requests.post("https://2captcha.com/in.php?", data=data)
    print("Request sent", response.text)

    s = response.json()["request"]
    time.sleep(15)

    # Poll 2captcha for captcha solution
    while True:
        solu = requests.get(f"https://2captcha.com/res.php?key={my_key}&action=get&json=1&id={s}").json()
        if solu["request"] == "CAPCHA_NOT_READY":
            print(solu["request"])
            time.sleep(8)
        elif "ERROR" in solu["request"]:
            print(solu["request"])
            driver.close()
            driver.quit()
            exit(0)
        else:
            break

    # Print captcha solution details
    for key, value in solu.items():
        print(key, ": ", value)
    time.sleep(2)
    solu = solu["request"]

    # Insert the obtained token into the verification form
    iframe1 = driver.find_element(By.ID, "arkoseFrame")
    driver.switch_to.frame(iframe1)
    time.sleep(1)
    iframe2 = driver.find_element(By.CSS_SELECTOR, "#arkose > div > iframe")
    driver.switch_to.frame(iframe2)
    driver.execute_script("document.getElementsByName('verification-token')[0].value = arguments[0];", solu)
    driver.execute_script("document.getElementsByName('fc-token')[0].value = arguments[0];", solu)
    time.sleep(1)
    driver.switch_to.default_content()

    # Submit the captcha
    script = f"""
        parent.postMessage(JSON.stringify({{
            eventId: "challenge-complete",
            payload: {{sessionToken: '{solu}'}}
        }}), "*");
    """
    driver.execute_script(script)

    print("Solution inserted")
    time.sleep(3)

    # Continue with the registration process and further work
    input('Enter any key to continue...')

except Exception as e:
    print(e)

finally:
    # Close the SeleniumBase driver
    driver.quit()
