#Imports
import pandas as pd
import pyodbc

#Data Input
casino_users = pd.read_csv("Casino Users.csv")
customer_wallet = pd.read_csv("Customer Wallet.csv")
casino_games = pd.read_csv("Casino games.csv")

casino_users.City = casino_users.City.str.capitalize()

countries = casino_users[['CountryName', 'CountryId']].drop_duplicates()

casino_users.BirthDate = pd.to_datetime(casino_users.BirthDate)

casino_users["Registration Date"] = pd.to_datetime(casino_users["Registration Date"])


conn = pyodbc.connect(
    'Driver={SQL Server}; \
    Server=PANOSPS\SQLEXPRESS; \
    Database=novibet; \
    Trusted_connection=yes')


# cursor = conn.cursor()
# for country in countries.itertuples():
#     cursor.execute('''
#                 INSERT INTO dbo.countries (country_id, country_name)
#                 VALUES (?,?)
#                 ''',
#                 country.CountryId, 
#                 country.CountryName
#                 )
# conn.commit()

cursor = conn.cursor()
for user in casino_users.itertuples():
    cursor.execute('''
                INSERT INTO dbo.casino_users (user_profile_id, birth_date, zipcode, sex, reg_date, city, country_id, status_sysname)
                VALUES (?,?,?,?,?,?,?,?)
                ''',
                user.UserProfileId, 
                user.BirthDate,
                user.ZipCode,
                user.Sex,
                user[4],
                user.City,
                user.CountryId,
                user.StatusSysname
                )
conn.commit()


for wallet in customer_wallet.itertuples():
    cursor.execute('''
                INSERT INTO dbo.customer_wallet (wallet_action_id, user_profile_id, type, type_sysname, amount, method_sysname, created)
                VALUES (?,?,?,?,?,?,?)
                ''',
                wallet.WalletActionId, 
                wallet.UserProfileId,
                wallet.Type,
                wallet.TypeSysname,
                wallet.Amount,
                wallet.MethodSysname,
                wallet.Created
                )
conn.commit()

for game in casino_games.itertuples():
    cursor.execute('''
                INSERT INTO dbo.casino_games (casino_provider, user_id, jackpot_id, free_spin_id, date, live_id, hold)
                VALUES (?,?,?,?,?,?,?)
                ''',
                game.Casino_Provider, 
                game.UserId,
                game.IsJackpotWinID,
                game.IsFreeSpinID,
                game.Date,
                game.IsLiveID,
                game.Hold
                )
conn.commit()

