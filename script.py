import random
import re
import time

import pyperclip
import requests
from httpx import TimeoutException
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from twocaptcha_setup import solve_funcaptcha


def extract_pk_and_surl(input_str):
    items = input_str.split("|")

    pk_value = None
    surl_value = None

    for item in items:
        if item.startswith("pk="):
            pk_value = item.split("=")[1]
        elif item.startswith("surl="):
            surl_value = item.split("=")[1]

    print(f"pk_value = {pk_value}")
    print("surl_value = https://client-api.arkoselabs.com")
    return pk_value, "https://client-api.arkoselabs.com"


def solve_website_funcaptcha(driver):

    print("Localizando URL atual")
    get_url = driver.current_url

    print("Entrando na primeira camada do iframe")
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#arkoseFrame"))
    )
    print("Entrando na segunda camada do iframe")
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "#arkose > div > iframe")
        )
    )
    print("Entrando na terceira camada do iframe")
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#game-core-frame"))
    )

    print("Localizando autenticação")
    wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div/div[1]/button"))
    )

    print("Saindo das camadas do iframe")
    driver.switch_to.default_content()

    print("Entrando na primeira camada do iframe")
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "#arkoseFrame"))
    )
    print("Entrando na segunda camada do iframe")
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, "#arkose > div > iframe")
        )
    )

    print("Localizando FunCaptcha Token")
    fc_token = driver.find_element(By.CSS_SELECTOR, "#FunCaptcha-Token")

    print("Pegando atributo value do FC_Token")
    token_value = fc_token.get_attribute("value")

    print("Saindo das camadas do iframe")
    driver.switch_to.default_content()

    print("Extraindo PK e SURL")
    pk_value, surl_value = extract_pk_and_surl(token_value)

    attempts = 0
    while attempts < 5:
        print(f"Executando função solve funcaptcha - Tentativa [{str( attempts + 1 )}]")
        captcha_result = solve_funcaptcha(pk_value, get_url, surl_value)
        print(pk_value, get_url, surl_value)
        if captcha_result:
            print("Processo do funcaptcha finalizado com sucesso!")
            print("\n########## Resultado Captcha ##########\n")
            print(captcha_result)

            print("Entrando na primeira camada do iframe")
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "#arkoseFrame")
                )
            )
            print("Entrando na segunda camada do iframe")
            WebDriverWait(driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it(
                    (By.CSS_SELECTOR, "#arkose > div > iframe")
                )
            )
            print("Preparando script JS")
            script = f"document.querySelector('#verification-token').value = '{str(captcha_result['code'])}';"
            time.sleep(0.5)
            print("Inserindo code no input")
            driver.execute_script(script)
            time.sleep(0.5)
            driver.execute_script(
                f"document.getElementsByName('fc-token')[0].value = '{str(captcha_result['code'])}';"
            )
            time.sleep(0.5)
            print("Saindo das camadas do iframe")
            driver.switch_to.default_content()

            script = f"""
                parent.postMessage(JSON.stringify({{
                    eventId: "challenge-complete",
                    payload: {{sessionToken: '{captcha_result['code']}'}}
                }}), "*");
            """
            driver.execute_script(script)
            time.sleep(0.5)
            return captcha_result
        else:
            attempts += 1
            print(f"Tentativa {attempts}/5 falhou. Tentando novamente...")

    print("Saindo das camadas do iframe")
    driver.switch_to.default_content()
    print("Processo do funcaptcha finalizado!")
    return captcha_result


print("iniciando navegador")

# PROXY = 'uc672e6e756f805d0-zone-custom-region-rsa:uc672e6e756f805d0@43.152.113.55:2333'

# firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument(f'--proxy-server={PROXY}')
driver = webdriver.Firefox()

# abrir twitter
print("Acessando X")
driver.get("https://twitter.com/?lang=pt-br")

print("Acessando email")
driver.execute_script("window.open('about:blank', '_blank');")
driver.switch_to.window(driver.window_handles[1])

# abrir Email
driver.get("https://tempmail.plus/pt/#!")

# Encontrar o elemento de entrada pelo ID
elemento_input = driver.find_element(By.ID, "pre_button")

# Obter o valor do atributo "value" do elemento de entrada
texto_copiado = elemento_input.get_attribute("value")

# Encontre o elemento do botão pelo XPath
button_element = driver.find_element(By.XPATH, '//*[@id="domain"]')

# Clique no botão
button_element.click()

# Gere um número aleatório entre 1 e 9
numero_botao = random.randint(1, 9)

# Construa o XPath do botão com base no número aleatório
xpath_botao = (
    f"/html/body/div[8]/div[1]/div[2]/div[1]/form/div/div[2]/div/button[{numero_botao}]"
)

# Encontre o botão usando o XPath construído
botao = driver.find_element(By.XPATH, xpath_botao)

# Copie o texto do botão
texto_copiado_botao = botao.text

# Clique no botão
botao.click()

email = texto_copiado + "@" + texto_copiado_botao

print("email gerado:", email)

# Obtenha os identificadores de todas as guias abertas
janelas = driver.window_handles

# Volte para a primeira guia (índice 0)
driver.switch_to.window(janelas[0])

# Defina um tempo máximo de espera para que o elemento seja clicável
wait = WebDriverWait(driver, 100)

try:
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/a/div/span/span',
            )
        )
    )

    # Clique no elemento
    elemento.click()

    print("Preenchendo informações.")
except:
    print("Não foi possível clicar no elemento.")

print("Gerando Nome")
# URL da API
url = "https://api.invertexto.com/v1/faker"

# Token de autenticação
token = "6428|C3ge7G5YHRD8ifbS4p5DS0zEOIvfEpi8"

# Parâmetros da requisição (incluindo o token)
params = {"token": token}

# Fazendo a requisição GET para a API
response = requests.get(url, params=params)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    # Se a requisição foi bem-sucedida, você pode acessar os dados da resposta
    data = response.json()

    # Acessando o nome gerado
    nome = data["name"]

else:
    # Se houve algum erro na requisição, imprima o código de status HTTP
    print("Erro:", response.status_code)

# Lista de prefixos para remover
prefixos = ["Dr.", "Sr.", "Sra.", "Srta."]


# Função para remover prefixos do nome
def remover_prefixos(nome, prefixos):
    for prefixo in prefixos:
        if nome.startswith(prefixo + " "):
            nome = nome.replace(prefixo + " ", "")
    return nome


# Removendo prefixos do nome gerado
nome_sem_prefixo = remover_prefixos(nome, prefixos)

print("Nome gerado:", nome_sem_prefixo)

try:
    # Localize o elemento que você deseja digitar texto (por exemplo, usando XPath)
    campo_input = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[1]/label/div/div[2]/div/input",
            )
        )
    )

    campo_input.clear()  # Limpa o campo de entrada, se houver texto pré-existente
    campo_input.send_keys(nome_sem_prefixo)  # Digita o texto gerado no campo de entrada

    print("Nome preenchido.")
except:
    print("Não foi possível preencher o nome.")


wait = WebDriverWait(driver, 10)

try:
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[3]/span",
            )
        )
    )

    # Clique no elemento
    elemento.click()

except:
    print("Não foi possível clicar no elemento.")


wait = WebDriverWait(driver, 10)

try:
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/label/div/div[2]/div/input",
            )
        )
    )

    # Clique no elemento
    elemento.click()

    print("Enserindo Email.")
except:
    print("Não foi possível clicar no elemento.")


# Preenchendo E-mail


campo_input = driver.find_element(
    By.XPATH,
    "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/label/div/div[2]/div/input",
)

# Cole o texto na área de transferência no campo de entrada
campo_input.send_keys(email)
time.sleep(1)

# Localize o elemento dropdown
dropdown_element = driver.find_element(By.XPATH, '//*[@id="SELECTOR_1"]')

# Crie um objeto Select com o elemento dropdown
dropdown = Select(dropdown_element)

# Obtenha todas as opções do dropdown
opcoes = dropdown.options

# Escolha uma opção aleatória
opcao_aleatoria = random.choice(opcoes)

# Selecione a opção aleatória
opcao_aleatoria.click()
print("Mês preenchido")
time.sleep(1)

# Localize o elemento dropdown
dropdown_element = driver.find_element(By.XPATH, '//*[@id="SELECTOR_2"]')

# Crie um objeto Select com o elemento dropdown
dropdown = Select(dropdown_element)

# Obtenha todas as opções do dropdown
opcoes = dropdown.options

# Escolha uma opção aleatória
opcao_aleatoria = random.choice(opcoes)

# Selecione a opção aleatória
opcao_aleatoria.click()
print("dia preenchido")
time.sleep(1)

# Localize o elemento dropdown
dropdown_element = driver.find_element(By.XPATH, '//*[@id="SELECTOR_3"]')

# Crie um objeto Select com o elemento dropdown
dropdown = Select(dropdown_element)

# Obtenha todas as opções do dropdown
opcoes = dropdown.options

# Filtrar as opções desejadas
opcoes_desejadas = [
    opcao
    for opcao in opcoes
    if opcao.text.isdigit() and 1990 <= int(opcao.text) <= 2007
]

# Escolha uma opção aleatória
opcao_aleatoria = random.choice(opcoes_desejadas)

# Selecione a opção aleatória
opcao_aleatoria.click()
print("Ano preenchido")
time.sleep(1)

# Clicando em avançar 2
wait = WebDriverWait(driver, 10)
print("Verificando data de nascimento.")
try:
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div",
            )
        )
    )

    # Clique no elemento
    elemento.click()

except:
    print("Não foi possível avançar.")


try:
    
    dropdown_element = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                '//*[@id="SELECTOR_1"]'
            )
        )
    )

    # Localize o elemento dropdown
    print("data incompleta")
    print("Preenchendo Novamente")
    # Crie um objeto Select com o elemento dropdown
    dropdown = Select(dropdown_element)

    # Obtenha todas as opções do dropdown
    opcoes = dropdown.options

    # Escolha uma opção aleatória
    opcao_aleatoria = random.choice(opcoes)

    # Selecione a opção aleatória
    opcao_aleatoria.click()
    print("Mês preenchido")
    time.sleep(1)

    # Localize o elemento dropdown
    dropdown_element = driver.find_element(By.XPATH, '//*[@id="SELECTOR_2"]')

    # Crie um objeto Select com o elemento dropdown
    dropdown = Select(dropdown_element)

    # Obtenha todas as opções do dropdown
    opcoes = dropdown.options

    # Escolha uma opção aleatória
    opcao_aleatoria = random.choice(opcoes)

    # Selecione a opção aleatória
    opcao_aleatoria.click()
    print("dia preenchido")
    time.sleep(1)

    # Localize o elemento dropdown
    dropdown_element = driver.find_element(By.XPATH, '//*[@id="SELECTOR_3"]')

    # Crie um objeto Select com o elemento dropdown
    dropdown = Select(dropdown_element)

    # Obtenha todas as opções do dropdown
    opcoes = dropdown.options

    # Filtrar as opções desejadas
    opcoes_desejadas = [
        opcao
        for opcao in opcoes
        if opcao.text.isdigit() and 1990 <= int(opcao.text) <= 2007
    ]

    # Escolha uma opção aleatória
    opcao_aleatoria = random.choice(opcoes_desejadas)

    # Selecione a opção aleatória
    opcao_aleatoria.click()
    print("Ano preenchido")
    time.sleep(1)

    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div",
            )
        )
    )

    # Clique no elemento
    elemento.click()
    elemento.click()
except:
    print("Data Completa")
    print("Avançando")
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div",
            )
        )
    )

    # Clique no elemento
    elemento.click()


# Defina um tempo máximo de espera
wait = WebDriverWait(driver, 3600)
time.sleep(5)
try:

    if "Enviamos um código para você" in driver.page_source:
        print("Nao pediu verificação.")
    else:
        print("Verificação necessária.")
        solve_website_funcaptcha(driver)

    # Esperar até que o texto esteja presente em algum elemento da página
    wait.until(
        EC.text_to_be_present_in_element(
            (By.XPATH, "//*[contains(text(), 'Enviamos um código para você')]"),
            "Enviamos um código para você",
        )
    )

    print("Verificação resolvida.")
except TimeoutException:
    print("Verificação nao resolvida")


#
# Volte para a guia
print("Aguardando código")
driver.switch_to.window(janelas[1])

# Esperar até que o texto esteja presente em algum elemento da página
wait.until(
    EC.text_to_be_present_in_element(
        (By.XPATH, "//*[contains(text(), 'é seu código de verificação do X')]"),
        "é seu código de verificação do X",
    )
)

try:
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[8]/div[2]/div/div[1]/div[2]")
        )
    )

    # Clique no elemento
    elemento.click()

    print("Copiando Código.")
except:
    print("Não foi possível copiar o codigo.")


wait = WebDriverWait(driver, 20)

# Encontre o elemento na página que contém o código
elemento_codigo = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div[8]/div[2]/div/div[1]/div[2]/div[2]")
    )
)

# Obtenha o texto do elemento
texto = elemento_codigo.text

# Use uma expressão regular para encontrar apenas os números no texto
numeros = re.findall(r"\d+", texto)

# Concatene os números encontrados para formar o código
codigo = "".join(numeros)

print("Código copiado:", codigo)


# Volte para a guia
driver.switch_to.window(janelas[0])


# Inserindo código
campo_input = driver.find_element(
    By.XPATH,
    "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input",
)

campo_input.clear()  # Limpa o campo de entrada, se houver texto pré-existente
campo_input.send_keys(
    codigo
)  # Cole o texto na área de transferência no campo de entrada
print("codigo inserido")

# Clicando em avançar
wait = WebDriverWait(driver, 10)

try:
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/div",
            )
        )
    )
    time.sleep(0.5)
    elemento.click()
    print("Avançando.")
except:
    print("Não foi possível clicar no elemento.")


# Digitar senha
# Importar as bibliotecas necessáriasprint("Digitando senha")
# Definir um tempo máximo de espera
wait = WebDriverWait(driver, 10)

try:
    # Localizar o elemento para digitar a senha (usando XPath)
    campo_input = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/div/label/div/div[2]/div[1]/input",
            )
        )
    )

    # Verificar se o elemento está visível e habilitado
    if campo_input.is_displayed() and campo_input.is_enabled():
        # Definir a senha
        senha = "#Senha02"

        # Digitar a senha no campo de entrada
        campo_input.send_keys(senha)

        print("Senha digitada com sucesso.")
    else:
        print("O elemento não está visível ou habilitado para interação.")
except StaleElementReferenceException:
    print(
        "O elemento de referência está obsoleto. Relocalizando o elemento e tentando novamente."
    )
    # Lógica para relocalizar e interagir com o elemento novamente
except ElementNotInteractableException:
    print("O elemento não é interagível.")
    # Lógica para lidar com o elemento não interagível

# Clicando em avançar
time.sleep(1)

try:
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div/div",
            )
        )
    )

    # Clique no elemento
    elemento.click()

    print("Conta criada com sucesso!")
except:
    print("Não foi possível clicar no elemento.")


# Clicar em start

try:
    wait = WebDriverWait(driver, 10)
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/form/input[6]"))
    )

    # Clique no elemento
    elemento.click()
    print("Resolva a Verificação")
    solve_website_funcaptcha(driver)
    
    

except:
    print("Oba não tem verificação")


# Clicar em continue no x
wait = WebDriverWait(driver, 3600)


print("Localizando elemento input")
# Localize o elemento que você deseja clicar (por exemplo, usando XPath)
elemento = wait.until(
    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/form/input[6]"))
)

# Clique no elemento
elemento.click()

try:
    # Clicar no OK
    wait = WebDriverWait(driver, 2)
    print("Localizando elemento div")
    # Localize o elemento que você deseja clicar (por exemplo, usando XPath)
    elemento = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "/html/body/div/div/div/div[1]/div[3]/div/div/div/div/div/div[2]/div[2]/div[2]/div/div",
            )
        )
    )

    # Clique no elemento
    elemento.click()
    print("Processo finalizado, Altere a foto de perfil")
except:
    print("Processo finalizado, Altere a foto de perfil")
