from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

print("WSR-1500AX2L FW アップデート & 自動設定スクリプト")
print("> adminのパスワードを入力してEnterキーを押下してください。")
password = input()

# FWのフルパスを入力
print("> このウインドウにファームウェアのファイルをドラッグアンドドロップしてEnterキーを押下してください。")
firmware_file_path = input()

# WebDriverの初期化（Chromeの場合）
driver_path = "./chromedriver.exe" # 実行ファイルと同じ階層にWebDriverのバイナリを配置
driver = webdriver.Chrome(service=ChromeService(driver_path))

# ルーターのIPアドレス
router_ip = "http://192.168.11.1"

# ログインページにアクセス
driver.get(router_ip)
driver.maximize_window()

# ログインフォームにユーザー名とパスワードを入力して送信
password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "id_nosave_Password")))
password_input.send_keys(password)
time.sleep(3)
driver.find_element(By.ID, "id_login").click()

# ログイン後、設定画面に移動
driver.get("http://192.168.11.1/index_adv.html")

# EashMeshを無効化
driver.switch_to.default_content()
driver.find_element(By.ID, "AT_WIRELESS").click()
driver.find_element(By.ID, "sub_meu3_8").click()
time.sleep(3)
driver.switch_to.frame("content_main")
driver.find_element(By.ID, "id_EasyMesh_Enable").click()
driver.find_element(By.CLASS_NAME, "button5").click()
time.sleep(8)
WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.ID,"id_warn_message")))
driver.switch_to.default_content()

# WPA3 SSIDを無効化

## 2.4GHz
driver.switch_to.default_content()
driver.find_element(By.ID, "sub_meu3_2").click()
time.sleep(3)
driver.switch_to.frame("content_main")
driver.find_element(By.ID, "id_wpa3").click()
driver.find_element(By.CLASS_NAME, "button2").click()
time.sleep(5)
WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.ID,"basic_content")))

## 5.0GHz
driver.switch_to.default_content()
driver.find_element(By.ID, "sub_meu3_3").click()
time.sleep(3)
driver.switch_to.frame("content_main")
driver.find_element(By.ID, "id_wpa3").click()
driver.find_element(By.CLASS_NAME, "button2").click()
time.sleep(5)
WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.ID,"basic_content")))

# DHCPサーバーからの自動取得に変更
time.sleep(3)
driver.switch_to.default_content()
driver.find_element(By.ID, "AT_WAN").click()
driver.find_element(By.ID, "sub_meu1_0").click()
time.sleep(3)
driver.switch_to.frame("content_main")
driver.find_element(By.ID, "id_WanMethod1").click()
driver.find_element(By.ID, "wan_apply").click()
time.sleep(3)
WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.ID,"routeron")))
driver.switch_to.default_content()

# IPv6を無効化
driver.switch_to.default_content()
driver.find_element(By.ID, "sub_meu1_4").click()
time.sleep(3)
driver.switch_to.frame("content_main")
driver.find_element(By.ID, "id_IPv6Method1").click()
driver.find_element(By.CLASS_NAME, "button22").click()
time.sleep(5)
WebDriverWait(driver, 300).until(EC.visibility_of_element_located((By.ID,"routeron")))
driver.switch_to.default_content()

# ファームウェアアップデート
driver.find_element(By.ID, "AT_ADMIN").click()
driver.find_element(By.ID, "sub_meu6_3").click()
time.sleep(3)
driver.switch_to.frame("content_main")
time.sleep(5)
driver.find_element(By.NAME, "file").send_keys(firmware_file_path)
time.sleep(10)
driver.find_element(By.NAME, "fwupbutton").click()

# WebDriverを終了
driver.quit()
