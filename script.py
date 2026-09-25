from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

print("Iniciando a Extração com o Chrome Oficial...")

# 1. Configuração com o Chrome Oficial
opcoes = webdriver.ChromeOptions()
opcoes.add_argument('--headless=new') # Modo invisível moderno
opcoes.add_argument('--no-sandbox')
opcoes.add_argument('--disable-dev-shm-usage')
# Não precisamos mais passar o caminho do arquivo, o webdriver_manager faz isso sozinho!

servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=opcoes)

# 2. Lista completa de links
mapas = {
    "bo1": {
        "kino_der_toten": "https://zwr.gg/leaderboards/bo/high-round/kino-der-toten/",
        "five": "https://zwr.gg/leaderboards/bo/high-round/five/",
        "ascension": "https://zwr.gg/leaderboards/bo/high-round/ascension/",
        "call_of_the_dead": "https://zwr.gg/leaderboards/bo/high-round/call-of-the-dead/",
        "shangri_la": "https://zwr.gg/leaderboards/bo/high-round/shangri-la/",
        "moon": "https://zwr.gg/leaderboards/bo/high-round/moon/",
        "nacht_der_untoten": "https://zwr.gg/leaderboards/bo/high-round/nacht-der-untoten/",
        "verruckt": "https://zwr.gg/leaderboards/bo/high-round/verruckt/",
        "shi_no_numa": "https://zwr.gg/leaderboards/bo/high-round/shi-no-numa/",
        "der_riese": "https://zwr.gg/leaderboards/bo/high-round/der-riese/"
    },
    "bo2": {
        "tranzit": "https://zwr.gg/leaderboards/bo2/high-round/tranzit/",
        "nuketown": "https://zwr.gg/leaderboards/bo2/high-round/nuketown/",
        "die_rise": "https://zwr.gg/leaderboards/bo2/high-round/die-rise/",
        "mob_of_the_dead": "https://zwr.gg/leaderboards/bo2/high-round/mob-of-the-dead/",
        "buried": "https://zwr.gg/leaderboards/bo2/high-round/buried/",
        "origins": "https://zwr.gg/leaderboards/bo2/high-round/origins/",
        "bus_depot": "https://zwr.gg/leaderboards/bo2/high-round/bus-depot/",
        "town": "https://zwr.gg/leaderboards/bo2/high-round/town/",
        "farm": "https://zwr.gg/leaderboards/bo2/high-round/farm/"
    },
    "bo3": {
        "shadows_of_evil": "https://zwr.gg/leaderboards/bo3/high-round/shadows-of-evil/",
        "the_giant": "https://zwr.gg/leaderboards/bo3/high-round/the-giant/",
        "der_eisendrache": "https://zwr.gg/leaderboards/bo3/high-round/der-eisendrache/",
        "zetsubou_no_shima": "https://zwr.gg/leaderboards/bo3/high-round/zetsubou-no-shima/",
        "gorod_krovi": "https://zwr.gg/leaderboards/bo3/high-round/gorod-krovi/",
        "revelations": "https://zwr.gg/leaderboards/bo3/high-round/revelations/",
        "nacht_der_untoten": "https://zwr.gg/leaderboards/bo3/high-round/nacht-der-untoten/",
        "verruckt": "https://zwr.gg/leaderboards/bo3/high-round/verruckt/",
        "shi_no_numa": "https://zwr.gg/leaderboards/bo3/high-round/shi-no-numa/",
        "kino_der_toten": "https://zwr.gg/leaderboards/bo3/high-round/kino-der-toten/",
        "ascension": "https://zwr.gg/leaderboards/bo3/high-round/ascension/",
        "shangri_la": "https://zwr.gg/leaderboards/bo3/high-round/shangri-la/",
        "moon": "https://zwr.gg/leaderboards/bo3/high-round/moon/",
        "origins": "https://zwr.gg/leaderboards/bo3/high-round/origins/"
    }
}

botoes = {"1_player": "1", "2_players": "2", "3_players": "3", "4_players": "4"}
recordes_finais = {}

# 3. O Motor de Busca
for jogo, mapas_do_jogo in mapas.items():
    print(f"\n=== {jogo.upper()} ===")
    recordes_finais[jogo] = {}
    
    for nome_mapa, url in mapas_do_jogo.items():
        print(f"\nColetando: {nome_mapa}")
        recordes_finais[jogo][nome_mapa] = {}
        
        if "/bo1/" in url:
            url = url.replace("/bo1/", "/bo/")
            
        try:
            driver.get(url)
            time.sleep(6) 
            
            for modo, numero_aba in botoes.items():
                try:
                    abas = driver.find_elements(By.XPATH, f"//*[normalize-space(text())='{numero_aba}']")
                    abas_visiveis = [aba for aba in abas if aba.is_displayed()]
                    if abas_visiveis:
                        abas_visiveis.sort(key=lambda x: x.location['y'])
                        driver.execute_script("arguments[0].click();", abas_visiveis[0])
                        time.sleep(3) 
                except:
                    pass
                    
                texto = driver.find_element(By.TAG_NAME, 'body').text
                linhas = texto.split('\n')
                round_atual = "N/A"
                
                for i, linha in enumerate(linhas):
                    if linha.strip() == "Platform":
                        for j in range(i + 1, min(i + 10, len(linhas))):
                            if str(linhas[j]).strip() == "1":
                                for k in range(j + 1, min(j + 15, len(linhas))):
                                    if linhas[k].strip().isdigit():
                                        round_atual = int(linhas[k].strip())
                                        break
                                break
                        break
                        
                recordes_finais[jogo][nome_mapa][modo] = round_atual
                print(f" -> {modo}: {round_atual}")

        except Exception as e:
            print(f" -> Erro ao ler mapa.")
            for modo in botoes.keys():
                recordes_finais[jogo][nome_mapa][modo] = "Erro"

driver.quit()

# 4. Salva o resultado no arquivo final
with open('recordes.json', 'w') as arquivo:
    json.dump(recordes_finais, arquivo, indent=4)

print("\n✅ Sucesso absoluto! O arquivo 'recordes.json' completo foi gerado.")
