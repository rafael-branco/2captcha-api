from twocaptcha import TwoCaptcha
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Don't forget to install the python module
# pip install 2captcha-python

def solve_funcaptcha(public_key, page_url, surl=None):

    api_key = 'ab6ffd3f64502f12075260644905551f'
    
    config = {
        'apiKey':            api_key,
        'defaultTimeout':    240,
    }
    
    print("Configurando API Key")
    solver = TwoCaptcha(**config)

    try:
        print("Resolvendo Funcaptcha...")
        result = solver.funcaptcha(sitekey=public_key, url=page_url, surl=surl)

    except Exception as e:
        print("Erro ao tentar resolver Funcaptcha")
        print(e)
        return False
    else:
        print("Resultado recebido do funcaptcha")
        print('Resultado: ' + str(result))
        return result


