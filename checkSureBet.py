import sqlite3
import math
import time
import random

# ✅ Connect to both databases

db_1xbet = sqlite3.connect("C:/Users/amitb/Desktop/Projects/Scraper/match_data_1xbet.db",uri=True)
db_real11 = sqlite3.connect("C:/Users/amitb/Desktop/Python Projects/Appium/match_data.db",uri=True)

db_sure_bet = sqlite3.connect("sure_bet_data.db")
cursor_sure_bet = db_sure_bet.cursor()

cursor_1xbet = db_1xbet.cursor()
cursor_real11 = db_real11.cursor()
tableName = "Punjab_vs_CSK_8_04_25_SureBets"
cursor_sure_bet.execute(f"""
    CREATE TABLE IF NOT EXISTS "{tableName}" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        team1_odds FLOAT,
        team2_odds FLOAT,
        arbitrage FLOAT,
        money_on_team1 FLOAT,
        money_on_team2 FLOAT,
        profit FLOAT
    )
""")
db_sure_bet.commit()



def get_latest_odds(db_cursor, table_name):
    """Fetch latest odds from the given table"""
    query = f'SELECT TEAM1_WIN, TEAM2_WIN FROM "{table_name}" ORDER BY id DESC LIMIT 1'
    db_cursor.execute(query)
    return db_cursor.fetchone()


def calculate_sure_bet(team1_odds, team2_odds, real11_fixed_bet=True):
    """Check if arbitrage betting is possible and calculate stake amounts"""
    arbitrage_condition = (1 / team1_odds) + (1 / team2_odds)
    print("team 1 odds --> ", team1_odds)
    print("team 2 odds --> ", team2_odds)
    print(" arbitrage condition ",arbitrage_condition)
    if arbitrage_condition < 1:  # ✅ Sure bet exists

        total_investment = 10000  # Example: Total money available

        # stake_team1 = (total_investment / team1_odds) / arbitrage_condition
        # stake_team2 = (total_investment / team2_odds) / arbitrage_condition
        #
        # if real11_fixed_bet:  # ✅ Ensure Real11 stakes follow multiples of 50/team_win
        #     stake_team2 = math.ceil(stake_team2 / (50 / team2_odds)) * (50 / team2_odds)
        #
        # total_profit = total_investment - (stake_team1 + stake_team2)

        stake_team1 = 50/team1_odds
        stake_team2 = 50/team2_odds

        total_profit  = 50 - stake_team1 - stake_team2
        timestamp = time.strftime("%H:%M:%S")

        cursor_sure_bet.execute(f"""
                        INSERT INTO {tableName} (timestamp, team1_odds, team2_odds, arbitrage, money_on_team1, money_on_team2, profit)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
        timestamp, team1_odds, team2_odds, arbitrage_condition, stake_team1, stake_team2, total_profit))
        db_sure_bet.commit()

        return stake_team1, stake_team2, total_profit
    else:
        return None


while True:  # ✅ Keep checking continuously
    odds_1xbet = get_latest_odds(cursor_1xbet, "Punjab vs CSK 8-4-25 1xbet")
    odds_real11 = get_latest_odds(cursor_real11, "Punjab vs CSK 8-4-25 Real11")

    if odds_1xbet and odds_real11:
        team1_odds_1xbet = odds_1xbet[0]
        team2_odds_1xbet = odds_1xbet[1]
        team1_odds_real11 = odds_real11[0]
        team2_odds_real11 = odds_real11[1]

        # ✅ Check both arbitrage scenarios
        sure_bet_1 = calculate_sure_bet(team1_odds_1xbet, team2_odds_real11, real11_fixed_bet=True)
        sure_bet_2 = calculate_sure_bet(team1_odds_real11, team2_odds_1xbet, real11_fixed_bet=True)

        if sure_bet_1:
            stake_team1, stake_team2, profit = sure_bet_1
            print(f"\n🔥 Arbitrage Opportunity Found! (Team1 on 1xBet & Team2 on Real11)")
            print(f"✅ Invest {stake_team1:.2f} rupees on Team1 at {team1_odds_1xbet} (1xBet)")
            print(f"✅ Invest {stake_team2:.2f} rupees on Team2 at {team2_odds_real11} (Real11)")
            print(f"💰 Guaranteed profit: {profit:.2f} rupees")

        if sure_bet_2:
            stake_team1, stake_team2, profit = sure_bet_2
            print(f"\n🔥 Arbitrage Opportunity Found! (Team1 on Real11 & Team2 on 1xBet)")
            print(f"✅ Invest {stake_team1:.2f} rupees on Team1 at {team1_odds_real11} (Real11)")
            print(f"✅ Invest {stake_team2:.2f} rupees on Team2 at {team2_odds_1xbet} (1xBet)")
            print(f"💰 Guaranteed profit: {profit:.2f} rupees")

        if not sure_bet_1 and not sure_bet_2:
            print("⚠️ No sure bet opportunity at the moment.")

    # ✅ Add random sleep interval to avoid overwhelming the system
    sleep_time = random.uniform(1, 2.5)
    print(f"⏳ Waiting {sleep_time:.2f} seconds before next check...")
    time.sleep(sleep_time)

# ✅ Close connections when script is stopped
db_sure_bet.close()
db_1xbet.close()
db_real11.close()