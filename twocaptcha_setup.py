from twocaptcha import TwoCaptcha

# Don't forget to install the python module
# pip install 2captcha-python

def solve_funcaptcha(public_key, page_url, surl=None):
    config = {
        'server':           '2captcha.com',
        'apiKey':           'YOUR_API_KEY',
        'softId':            123,
        'callback':         'https://your.site/result-receiver',
        'defaultTimeout':    120,
        'recaptchaTimeout':  600,
        'pollingInterval':   10,
    }

    solver = TwoCaptcha(**config)

    try:
        result = solver.funcaptcha(
            sitekey=public_key,
            url=page_url,
            surl=surl
        )

    except Exception as e:
        print("An error occurred:", e)
        return None

    return result

public_key = 'PUBLIC_KEY_FOR_FUNCAPTCHA'
page_url = 'http://mysite.com/page/with/funcaptcha/'
surl = 'https://client-api.arkoselabs.com'

result = solve_funcaptcha(public_key, page_url, surl)

if result:
    token = result.get('code')
    print("FunCaptcha Token:", token)
else:
    print("Failed to solve FunCaptcha.")
