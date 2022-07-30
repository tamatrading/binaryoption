#selenium起動
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

# 指定時間待機
import datetime
import time
import re
import configparser

#gmail
#from gmail import sendGmail

# マウスやキーボード操作に利用
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By

# セレクトボックスの選択に利用
from selenium.webdriver.support.ui import Select


USER_ID = ""
USER_PWD = ""
BET_MONEY = 0
ENTRY_TIME = ""

CHROMEDRIVER = "C:\MyPrg\Python\chromedriver.exe"
DISP_MODE = "ON"   # "ON" or "OFF"
ORD_PWD = "fAGgL9vWzJ"
MAIL_ADR = 'mtake88@gmail.com'
MAIL_PWD = 'jnfzzdwkghwmrgkm'

#ENTRY_TIME = "09:54:33"

v_dt = ""  # ローカルな現在の日付と時刻を取得
v_entryTime = ""
v_entryBefore1Minute = ""

RETRY = 3
holidayList = []

def getConfigFile():
    global holidayList
    global v_dt
    global v_entryTime
    global v_entryBefore1Minute
    global USER_ID
    global USER_PWD
    global BET_MONEY
    global ENTRY_TIME

    config_txt = configparser.ConfigParser()
    config_txt.read('config.txt', encoding='utf-8')

    USER_ID = config_txt.get('DEFAULT', 'userid')
    USER_PWD = config_txt.get('DEFAULT', 'passwd')
    ENTRY_TIME = config_txt.get('DEFAULT', 'entryTime')
    BET_MONEY = config_txt.get('DEFAULT', 'betPrice')

    holidayList = eval(config_txt.get('HOLYDAY','holyday'))

    v_dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得
    v_entryTime = datetime.datetime.strptime(ENTRY_TIME, '%H:%M:%S').replace(year=v_dt.year, month=v_dt.month, day=v_dt.day)
    v_entryBefore1Minute = (datetime.datetime.strptime(ENTRY_TIME, '%H:%M:%S') + datetime.timedelta(minutes=-1)).replace(year=v_dt.year, month=v_dt.month, day=v_dt.day)

#-----------------------------
# 本日が休日かどうかチェックする
#-----------------------------
def isHoliday(day: datetime):
    ret = False

    # 本日が土日であれば休日
    if day.weekday() > 4:
        ret = True
    else:
        # 本日が祝日であれば休日
        if str(day) in holidayList:
            ret = True

    return ret

#-----------------------------
# 本日がトレード日かどうかチェックする
#-----------------------------
def check_tradeDay(dt):
    today = dt.date()

    # 本日が休日ならトレード日ではない
    if isHoliday(today) == True:
        return False

    # 5, 10日チェック
    if (today.day % 5) == 0: #今日は5,10日である
        return True
    else: #今日は5,10日でない営業日
        t1 = today + datetime.timedelta(days=1)
        if isHoliday(t1) == True:
            if (t1.day % 5)== 0:
                return True
            else:
                t2 = today + datetime.timedelta(days=2)
                if isHoliday(t2) == True:
                    if (t2.day % 5) == 0:
                        return True
                    else:
                        t3 = today + datetime.timedelta(days=3)
                        if isHoliday(t3) == True:
                            if (t3.day % 5) == 0:
                                return True

    return False

#-----------------------------
#ログアウトする
#-----------------------------
def hiloLogOut():

    #「お客様情報」をクリック
    try:
        tmp = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[3]/div[9]")
    except NoSuchElementException:
        print("LogOut 1 Err")
        return
    tmp.click()
    time.sleep(1)

    #「ログアウト」をクリック
    try:
        tmp = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[6]/div/div[5]/div")
    except NoSuchElementException:
        print("LogOut 2 Err")
        return
    tmp.click()
    time.sleep(2)

#-----------------------------
# 取引日付・取引時間のチェック
#-----------------------------
def checkEntryDateTime():

    # 本日が5,10日かどうかを確認する
    v_dt = datetime.datetime.today()  # ローカルな現在の日付と時刻を取得
    if check_tradeDay(v_dt) == False:
        print(f'トレード日ではありません：{v_dt.date()}')
    #        return -1

    # 現在時刻がエントリ時刻の１分前より前かどうかを確認する

    if v_dt > v_entryBefore1Minute:
        print("エントリ時刻を過ぎています")
        return -2

    return 0

# -----------------------------
# 現在時刻が指定時間になるまで待つ
# -----------------------------
def waitDateTime(tm:datetime):
    # 現在時刻がエントリ時刻の１分前になるまでループして待つ
    while True:
        v_dt = datetime.datetime.today()
        print(v_dt)
        if v_dt >= tm:
            break
        time.sleep(1)

#-----------------------------
#HighLowの口座にログインし、指定の時間が来たら申し込みをする
#-----------------------------
def hiloLogin():

    # サイトを開く
    driver.get("https://highlow.com/login/")
    time.sleep(1)

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
        print("Login Error!!!")
        return -3

    #口座残高の"￥(半角)"と、","を削除
    mmm = re.sub(r",", "", moneyTag.text[1:])   # "￥"が取り除けなかったので、[1:]で先頭文字を無視するようにした
    money = int(mmm)
    print(money)

    #残高があるか確認
    if BET_MONEY > money:
        print("残高不足！")
        return -4

    try:
        betBox = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[4]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div/input")
        betBox.send_keys(str(BET_MONEY))
    except NoSuchElementException:  #金額設定ができなかった
        print("取引時間外？")
    #    return -5

    # LOWをクリック
    #   login = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[4]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div[3]/div")
    #login.click()

    # 現在時刻がエントリ時刻になるまでループして待つ
    waitDateTime(v_entryTime)

    # 今すぐ購入をクリック
    #login = driver.find_element(by=By.XPATH, value="/html/body/main/div/div[4]/div[2]/div[1]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[2]/div/div")
    #login.click()

    return 0

'''
メインルーチン
'''
if __name__ == "__main__":

    getConfigFile()
    print(v_dt)
    print(v_entryTime)
    print(v_entryBefore1Minute)

    if checkEntryDateTime() == 0:

        # 現在時刻がエントリ時刻の１分前になるまでループして待つ
        waitDateTime(v_entryBefore1Minute)

        #chromeを起動する
        chrome_service = fs.Service(executable_path=CHROMEDRIVER)
        if DISP_MODE == "OFF":
            options = Options()
            options.add_argument('--headless')
            driver = webdriver.Chrome(service=chrome_service, options=options)
        else:
            driver = webdriver.Chrome(service=chrome_service)

        hiloLogin()
        time.sleep(6)
        hiloLogOut()

        #chromeを閉じる
        driver.quit()


    print("complete")

