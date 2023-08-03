import time
import math
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


# Configurando as opções do ChromeDriver
options = webdriver.ChromeOptions()

# Executando em modo headless, sem abrir o navegador
# Descomentar para abrir o navegador e ver o script sendo executado
# options.add_argument("--headless")

# Insira o caminho para o seu chromedriver
service = Service('AppData\Local\Programs\Python\Python311')

# Inicializando o driver do Chrome
driver = webdriver.Chrome(service=service, options=options)

# URL do site a ser feito o scraping
url = 'https://www.psicologiaviva.com.br/psicologo/'

# Acessando a página
driver.get(url)

# Armazena a janela original (página com todos os psicólogos)
original_tab = driver.current_window_handle

while True:
    for current_psychologist in range(1, 6):
        time.sleep(1)
        # Espera o botão com o link para o perfil do psicólogo ser carregado
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[1]/main/div/div/div/div[4]/div/div/div/div[1]/div[2]/div[%d]/div/div[2]/div/div[1]/div/div[6]' % current_psychologist)))

        # Obtendo o link do perfil do psicólogo
        new_tab_link = driver.find_element(
            "xpath", '/html/body/div[1]/div[1]/main/div/div/div/div[4]/div/div/div/div[1]/div[2]/div[%d]/div/div[2]/div/div[1]/div/div[6]/div/a/span' % current_psychologist)

        # Abre o perfil do psicólogo em uma nova aba
        action = ActionChains(driver)
        action.key_down(Keys.CONTROL).click(
            new_tab_link).key_up(Keys.CONTROL).perform()
        time.sleep(1)

        # Acessa a aba com o perfil do psicólogo aberto
        try:
            driver.switch_to.window(driver.window_handles[1])
        except:
            driver.switch_to.window(driver.window_handles[0])

        # Tentando clicar para liberar todo o conteúdo da página, se houver
        try:
            # Botão "ver mais" da biografia do psicólogo
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[3]/div/div[2]/button/span'))).click()

            # Botão "ver mais" da formação do psicólogo
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[4]/div/div[2]/button/span'))).click()
        except:
            pass

        # Contagem do número de campos preenchidos pelo psicólogo
        # Primeiro, verifica se o psicólogo tem um vídeo de apresentação no perfil
        # Se sim, o valor de número de campos começa em 2
        if driver.find_element(
                "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[1]/div/h1').text == 'Conheça a Psicóloga' or driver.find_element(
                    "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[1]/div/h1').text == 'Conheça o Psicólogo':
            current_field = 2
        else:
            # Caso o psicólogo não tenha um vídeo de apresentação, o valor começa em 1
            current_field = 1

        ###########################################################################################################################
        # Obtendo os dados do psicólogo

        # Nome
        try:
            name = driver.find_element(
                "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[1]/div/div/div[2]/div[3]/h1').text
            print("\n->Nome:")
            print(name)
            current_field += 1
        except:
            name = None

        # Especialidades
        try:
            expertises = driver.find_element(
                "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[%d]/div/div' % current_field).text
            expertises = ', '.join(expertises.splitlines()).strip()
            print("\n->Especialidades:")
            print(expertises)
            current_field += 1
        except:
            expertises = None

        # Biografia
        try:
            bio = driver.find_element(
                "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[%d]/div/div[1]/pre' % current_field).text
            bio = ', '.join(bio.splitlines()).strip()
            print("\n->Biografia:")
            print(bio)
            current_field += 1
        except:
            bio = None

        # Formação
        try:
            education = driver.find_element(
                "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[%d]/div/div[1]/pre' % current_field).text
            education = ', '.join(education.splitlines()).strip()
            print("\n->Formação:")
            print(education)
            current_field += 1
        except:
            education = None

        ###########################################################################################################################
        # Obtendo os dados de avaliação
        try:
            # Número total de avaliações recebidas pelo psicólogo
            total_ratings = driver.find_element(
                "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[%d]/div/h1' % current_field).text
            total_ratings = int(total_ratings[13:-1])
            average_rating = 0

            while True:
                try:
                    # Número da avaliação da página atual (vai de 1 à 5)
                    for current_rating in range(1, 6):
                        # Iniciais do paciente que fez a avaliação
                        patient = driver.find_element(
                            "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[%d]/div/div[1]/div/div[%d]/div[1]/span/b' % (current_field, current_rating)).text
                        # Nota dada pelo paciente ao psicólogo
                        rating = driver.find_element(
                            "xpath", '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[%d]/div/div[1]/div/div[%d]/div[2]/div[1]' % (current_field, current_rating)).text
                        # Transforma a nota em inteiro
                        rating = int(rating[0])

                        # Adiciona o valor da nota a uma variável para posteriormente calcular a média
                        average_rating += rating

                        # Inserindo os dados no arquivo.csv
                        # Abre o arquivo .csv que irá conter os dados de avaliação
                        with open('C:\PsiViva Scraping/ratings.csv', 'a', newline='', encoding='utf-8') as ratings_csv:
                            # Cria o writer do arquivo .csv
                            ratings = csv.writer(ratings_csv)

                            # Inserindo os dados de avaliação no arquivo .csv
                            rating_row = [patient, name, rating]
                            ratings.writerow(rating_row)
                except:
                    break

                try:
                    # Calculando em que posição estará o botão 'next page' com base no número de avaliações
                    if total_ratings > 35:
                        next_page_position = 10
                    else:
                        next_page_position = math.ceil(
                            (total_ratings/5) + 2)

                    # Tentando clicar no botão "próxima página" para obter mais avaliações, se houverem
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[1]/div/div/div[1]/main/div/div/div[2]/div[2]/div[%d]/div/div[2]/nav/ul/li[%d]/button' % (current_field, next_page_position)))).click()
                    # Espera induzida para carregamento da página
                    time.sleep(1)

                except:
                    break

            ###########################################################################################################################
            # Inserindo os dados nos arquivos .csv

            # Abre o arquivo .csv que irá conter os dados do psicólogo
            with open('C:\PsiViva Scraping/psychologists.csv', 'a', newline='', encoding='utf-8') as psychologists_csv:
                # Cria o writer do arquivo .csv
                psychologists = csv.writer(psychologists_csv)

                # Inserindo os dados do psicólogo no arquivo csv (caso ele possua dados de avaliações)
                average_rating = average_rating/total_ratings
                psychologist_row = [name, bio, expertises,
                                    total_ratings, average_rating]
                psychologists.writerow(psychologist_row)

            # Fecha a aba atual (página com o perfil do psicólogo atual)
            driver.close()

            # Retorna para a aba original (página com todos os psicólogos)
            driver.switch_to.window(driver.window_handles[0])

        except:
            # Inserindo os dados do psicólogo no arquivo csv (caso ele não possua dados de avaliações)
            # Abre o arquivo .csv que irá conter os dados do psicólogo
            with open('C:\PsiViva Scraping/psychologists.csv', 'a', newline='', encoding='utf-8') as psychologists_csv:
                # Cria o writer do arquivo .csv
                psychologists = csv.writer(psychologists_csv)
                psychologist_row = [name, bio, expertises, 0, 0]
                psychologists.writerow(psychologist_row)

            # Fecha a aba atual (página com o perfil do psicólogo)
            driver.close()

            # Retorna para a aba original (página com todos os psicólogos)
            driver.switch_to.window(driver.window_handles[0])
            # Tentando clicar para liberar todo o conteúdo da página, se houver
    try:
        # Tenta clicar no botão "Mostre-me outros profissionais" para atualizar a página e obter novos psicólogos
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/div[1]/main/div/div/div/div[4]/div/div/div/div[1]/div[3]/button'))).click()
        time.sleep(1)
    except:
        driver.quit()
