import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
import sqlite3

conn = sqlite3.connect("match_data.db")
cursor = conn.cursor()

table_name = "Punjab vs CSK 8-4-25 Real11"

def create_table(table_name):
    query = f"""
    CREATE TABLE IF NOT EXISTS "{table_name}" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        TEAM1_TIME TEXT,
        TEAM1_WIN FLOAT,
        TEAM2_TIME TEXT,
        TEAM2_WIN FLOAT
    )
    """
    cursor.execute(query)
    conn.commit()

create_table(table_name)

def get_last_values(table_name):
    query = f'SELECT TEAM1_WIN, TEAM2_WIN FROM "{table_name}" ORDER BY id DESC LIMIT 1'
    cursor.execute(query)
    return cursor.fetchone()

def insert_data(table_name, team1_time, team1_win, team2_time, team2_win):
    last_values = get_last_values(table_name)

    # Append only if values are different from last row
    if not last_values or (last_values[0] != team2_win or last_values[1] != team1_win):
        query = f'''
            INSERT INTO "{table_name}" (TEAM1_TIME, TEAM1_WIN, TEAM2_TIME, TEAM2_WIN)
            VALUES (?, ?, ?, ?)
        '''
        cursor.execute(query, (team2_time, team2_win, team1_time, team1_win))
        conn.commit()

capabilities = {
    'platformName': 'Android',
    'automationName': 'uiautomator2',
    'deviceName': 'Nothing Phone (2a)',
    'udid': '10.51.1.85:5555',  # ✅ Specific device targeting
    'appPackage': 'os.real11',
    'appActivity': 'com.app.sports.real11.ui.screens.splash.SplashActivity',  # ✅ Correct launcher activity
    'noReset': True,  # ✅ Prevents app data reset
    'autoGrantPermissions': True,  # ✅ Auto-accepts app permissions
    'unicodeKeyboard': False,  # ✅ Critical: Avoids keyboard hijacking
    'resetKeyboard': False,  # ✅ Critical: Preserves keyboard settings
    'appWaitActivity': 'com.app.sports.real11.ui.*',  # Wildcard for dynamic screens
    'disableWindowAnimation': True,  # Reduces flakiness in UI interactions
    'skipDeviceInitialization': True,  # Speeds up session start (if device is pre-setup)
}

appium_server_url = 'http://localhost:4723'
yes_btn = "os.real11:id/txtYesOption"
no_btn = "os.real11:id/txtNoOption"
close_popup = "os.real11:id/img_cancel"
put_val = "os.real11:id/txtPutValue"
get_val = "os.real11:id/txtGetValue"
start_bnt = "os.real11:id/btnYes"

class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_find_battery(self) -> None:
        self.driver.implicitly_wait(3)  # Waits up to 3 seconds

        try:
            # self.driver.find_element(AppiumBy.XPATH,'//android.widget.TextView[@resource-id="os.real11:id/txt_team1" and @text="KOL"]').click()
            print("started")
            # if match is on home screen
            # self.driver.find_element(AppiumBy.ID,start_bnt).click()
            # self.driver.find_element(AppiumBy.ID,"os.real11:id/clTopQuestion_trade").click()
            # self.driver.find_element(AppiumBy.ID, start_bnt).click()

            self.driver.find_element(AppiumBy.ID, "os.real11:id/txtViewAll").click()
            self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="os.real11:id/txtQuestion_trade" and @text="Chennai to win the T20 match vs Punjab ?(Match 22)"]').click()
            self.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="os.real11:id/txtQuestion_trade" and @text="Chennai to win the T20 match vs Punjab ?(Match 22)"]').click()
            self.driver.find_element(AppiumBy.ID, start_bnt).click()



            yes = self.driver.find_element(AppiumBy.ID,yes_btn)
            no = self.driver.find_element(AppiumBy.ID,no_btn)
            put = self.driver.find_element(AppiumBy.ID,put_val)

            while True:
                # print(put.text)
                team1_time  = time.strftime('%H:%M:%S')
                team1_win  = float(put.text[1:])
                team1_win = 50/team1_win
                no.click()
                # print(put.text)
                team2_time = time.strftime('%H:%M:%S')
                team2_win = float(put.text[1:])
                team2_win = 50/team2_win
                insert_data(table_name,team1_time,team1_win, team2_time, team2_win)
                yes.click()

            # print("found")
        except Exception as e:
            print(f"⚠️ Error encountered: {e}")



        print("settings achieved")
if __name__ == '__main__':
    unittest.main()