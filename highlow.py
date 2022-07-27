#selenium起動
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# 指定時間待機
import time
import re

#gmail
#from gmail import sendGmail

# マウスやキーボード操作に利用
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

# セレクトボックスの選択に利用
from selenium.webdriver.support.ui import Select

CHROMEDRIVER = "C:\MyPrg\Python\chromedriver.exe"
DISP_MODE = "ON"   # "ON" or "OFF"
USER_ID = "mtake88@gmail.com"
USER_PWD = "zX6XiGFK"
ORD_PWD = "fAGgL9vWzJ"
MAIL_ADR = 'mtake88@gmail.com'
MAIL_PWD = 'jnfzzdwkghwmrgkm'

RETRY = 3
orderList = []  # 注文内容をメールで送信


#-----------------------------
#ログアウトする
#-----------------------------
def hiloLogOut():
    '''
    try:
        tmp = driver.find_element(by=By.XPATH, value="//img[@title='ログアウト']")
    except NoSuchElementException:
        print("err")
        sendIpoMail(-3)
        return
    tmp.click()
    time.sleep(2)
    '''
    time.sleep(1)

#-----------------------------
#HighLowの口座にログインし、指定の時間が来たら申し込みをする
#-----------------------------
def hiloLogin():
    # サイトを開く
    driver.get("https://highlow.com/login/")
    time.sleep(3)


    # ユーザIDを入力
    userID = driver.find_element(by=By.ID, value="username")
    userID.send_keys(USER_ID)

    time.sleep(3)
    return 0

    # パスワードを入力
    userpass = driver.find_element(by=By.NAME, value="password")
    userpass.send_keys(USER_PWD)


    '''

    # ログインをクリック
    login = driver.find_element(by=By.NAME, value="ACT_login")
    login.click()
    time.sleep(3)
'''

'''
    # name属性で指定
    try:
        moneyTag = driver.find_element(by=By.XPATH,
                                       value="/html/body/table/tbody/tr[1]/td[1]/div[2]/div[1]/div/div/div/div/table/tbody/tr/td[1]/span")
    except NoSuchElementException:
        tmp = driver.find_elements(by=By.XPATH, value="//b[contains(text(),'重要なお知らせ')]")
        if len(tmp) >= 1:
            ii = -1
        else:
            ii = -2
        return ii

    money = int(moneyTag.text.replace(",", ""))
    print(money)

    # IPOページに入る
    driver.find_element(by=By.LINK_TEXT, value="IPO・PO").click()
    time.sleep(3)
    driver.find_element(by=By.XPATH, value="//img[@alt='新規上場株式ブックビルディング / 購入意思表示']").click()
    time.sleep(3)

    # 申込できる銘柄をチェック
    while True:
        reqs = driver.find_elements(by=By.XPATH, value="//img[@alt='申込']")

        if len(reqs) > 0:
            order_one = []
            print(f"ipo = {len(reqs)}")
            reqs[0].click()
            time.sleep(3)

            # ===== 個別の申し込み画面 =====
            # 銘柄名
            tag = driver.find_element(by=By.XPATH,
                                      value="/html/body/table/tbody/tr/td/table[1]/tbody/tr/td/table[1]/tbody/tr[1]/td/form/table[4]/tbody/tr/td")
            print(tag.text)
            order_one.append(tag.text)

            kari_tag = driver.find_element(by=By.XPATH,
                                           value="/html/body/table/tbody/tr/td/table[1]/tbody/tr/td/table[1]/tbody/tr[1]/td/form/table[5]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/div")
            ss = kari_tag.text.split(' ')
            kari = int(ss[-2].replace(",", ""))
            # print(kari)
            order_one.append(kari)

            unit_tag = driver.find_element(by=By.XPATH, value="//td[contains(text(),'売買単位')]")
            unit = int(re.findall(r'/(.*)株', unit_tag.text)[0])
            # print(unit)
            cnt = int(money / (kari * unit)) * unit  # 申込株数
            # print(cnt)

            # name属性で数量指定
            suryo = driver.find_element(by=By.NAME, value="suryo")
            suryo.send_keys(str(cnt))
            order_one.append(cnt)

            # id属性で「ストライクプライス」にチェック指定
            strike = driver.find_element(by=By.ID, value="strPriceRadio")
            strike.click()

            # print(order_one)

            # name属性で数量指定
            toripass = driver.find_element(by=By.NAME, value="tr_pass")
            toripass.send_keys(ORD_PWD)

            # name属性で申込確認ボタン指定・クリック
            driver.find_element(by=By.NAME, value="order_kakunin").click()
            time.sleep(2)

            # ===== 申し込み確認画面 =====
            # name属性で申込ボタン指定・クリック
            driver.find_element(by=By.NAME, value="order_btn").click()
            time.sleep(2)

            # ===== 申し込み完了画面 =====
            # IPOトップへ戻る・クリック
            orderList.append(order_one)
            driver.find_element(by=By.XPATH, value="//a[contains(text(),'購入意思表示画面へ戻る')]").click()
            time.sleep(3)
        else:
            break
    return 0
'''

if __name__ == "__main__":

    chrome_service = fs.Service(executable_path=CHROMEDRIVER)

    if DISP_MODE == "OFF":
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=chrome_service, options=options)
    else:
        driver = webdriver.Chrome(service=chrome_service)

    for retry in range(RETRY):
        ret = hiloLogin()
        hiloLogOut()
        if ret == 0:
            break

    driver.quit()

    print(orderList)
    print("complete")

