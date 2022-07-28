#selenium起動
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# 指定時間待機
import datetime
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

BET_MONEY = 1000

RETRY = 3
orderList = []  # 注文内容をメールで送信
holidayList =\
[
    "2022-07-18",
    "2022-07-28",
    "2022-08-11",
    '2022-09-19',
    '2022-09-23',
    '2022-10-10',
    '2022-11-03',
    '2022-12-31',
    '2023-01-01',
    '2023-01-02',
    '2023-01-09',
    '2023-02-11',
    '2023-02-23',
    '2023-03-21',
    '2023-04-29',
    '2023-05-03',
    '2023-05-04',
    '2023-05-05',
    '2023-07-17',
    '2023-08-11',
    '2023-09-18',
    '2023-09-23',
    '2023-10-09',
    '2023-11-03',
    '2023-11-23',
    '2023-12-31'
]

#-----------------------------
# 本日がトレード日かどうかチェックする
#-----------------------------
def check_tradeDay(dt):
    ret = True
    holy = False

    week = dt.date().weekday()
    day = dt.date().day

    # 祭日チェック
    if str(dt.date()) in holidayList:
        holy = True

    # もし今日が5,10日で、かつ土日祭でなければ、トレード日とする
    if ((day % 5) == 0):
        if (week < 5) and (holy == False):
            return True
    else:

    return ret

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
    time.sleep(1)

    # 本日が5,10日かどうかを確認する
    dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得
    if check_tradeDay(dt) == False:
        print(f'トレード日ではない：{dt.date()}')
        return -1

    # ユーザIDを入力
    userID = driver.find_element(by=By.ID, value="login-username")
    userID.send_keys(USER_ID)

    # パスワードを入力
    userpass = driver.find_element(by=By.ID, value="login-password")
    userpass.send_keys(USER_PWD)

    # ログインをクリック
    login = driver.find_element(by=By.ID, value="login-submit-button")
    login.click()
    time.sleep(3)

    #ログインチェック（口座残高を取得）
    try:
        moneyTag = driver.find_element(by=By.ID, value="balanceValue")

    except NoSuchElementException:  #口座残高が取得できなかった
        #tmp = driver.find_elements(by=By.XPATH, value="//b[contains(text(),'重要なお知らせ')]")
        #if len(tmp) >= 1:
        #    ii = -1
        #else:
        #    ii = -2
        print("Error!!!")
        return -1

    #口座残高の"￥(半角)"と、","を削除
    mmm = re.sub(r",", "", moneyTag.text[1:])   # "￥"が取り除けなかったので、[1:]で先頭文字を無視するようにした
    money = int(mmm)
    print(money)

    #残高があるか確認
    if BET_MONEY > money:
        print("残高不足！")
        return -2

    betBox = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[4]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/input")
    betBox.send_keys(str(BET_MONEY))

    # LOWをクリック
    login = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[4]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div[3]/div")
    login.click()

    # 今すぐ購入をクリック
    #login = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[4]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div/div")
    #login.click()

    time.sleep(1)

    return 0


    '''

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

