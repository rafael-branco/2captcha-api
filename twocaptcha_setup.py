from twocaptcha import TwoCaptcha
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Don't forget to install the python module
# pip install 2captcha-python

def solve_funcaptcha(public_key, page_url, surl=None):

    api_key = 'c572dad22c39c8dae2789529499e2b40'
    
    config = {
        'apiKey':            api_key,
        'defaultTimeout':    240,
    }
    
    print("Configurando API Key")
    solver = TwoCaptcha(**config)

    try:
        print("Resolvendo Funcaptcha...")
        result = solver.funcaptcha(
            sitekey=public_key, 
            url=page_url, 
            surl=surl,
            proxy={
                'type': 'HTTP',
                'uri': 'uc672e6e756f805d0-zone-custom-region-rsa:uc672e6e756f805d0@43.152.113.55:2333'
            }
        )

    except Exception as e:
        print("Erro ao tentar resolver Funcaptcha")
        print(e)
        return False
    else:
        print("Resultado recebido do funcaptcha")
        print('Resultado: ' + str(result))
        return result


