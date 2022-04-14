import pandas as pd
import datetime
import numpy as np

#Data Input
casino_users = pd.read_csv("Casino Users.csv")
customer_wallet = pd.read_csv("Customer Wallet.csv")
casino_games = pd.read_csv("Casino games.csv")

#Casino Users Data Processing
#Convert Dates to correct type
casino_users.BirthDate = pd.to_datetime(casino_users.BirthDate)
casino_users['Registration Date'] = pd.to_datetime(casino_users['Registration Date'])

#City column cleaning data
casino_users.City = casino_users.City.str.lower()

casino_users.City = casino_users.City.str.replace('α','a')
casino_users.City = casino_users.City.str.replace('β','b')
casino_users.City = casino_users.City.str.replace('γ','g')
casino_users.City = casino_users.City.str.replace('δ','d')
casino_users.City = casino_users.City.str.replace('ε','e')
casino_users.City = casino_users.City.str.replace('ζ','z')
casino_users.City = casino_users.City.str.replace('η','i')
casino_users.City = casino_users.City.str.replace('θ','th')
casino_users.City = casino_users.City.str.replace('ι','i')
casino_users.City = casino_users.City.str.replace('κ','k')
casino_users.City = casino_users.City.str.replace('λ','l')
casino_users.City = casino_users.City.str.replace('μ','m')
casino_users.City = casino_users.City.str.replace('ν','n')
casino_users.City = casino_users.City.str.replace('ξ','x')
casino_users.City = casino_users.City.str.replace('ο','o')
casino_users.City = casino_users.City.str.replace('π','p')
casino_users.City = casino_users.City.str.replace('ρ','r')
casino_users.City = casino_users.City.str.replace('σ','s')
casino_users.City = casino_users.City.str.replace('ς','s')
casino_users.City = casino_users.City.str.replace('τ','t')
casino_users.City = casino_users.City.str.replace('υ','i')
casino_users.City = casino_users.City.str.replace('φ','f')
casino_users.City = casino_users.City.str.replace('χ','ch')
casino_users.City = casino_users.City.str.replace('ψ','ps')
casino_users.City = casino_users.City.str.replace('ω','o')
casino_users.City = casino_users.City.str.replace('ά','a')
casino_users.City = casino_users.City.str.replace('ή','i')
casino_users.City = casino_users.City.str.replace('ί','i')
casino_users.City = casino_users.City.str.replace('ύ','i')
casino_users.City = casino_users.City.str.replace('ό','o')
casino_users.City = casino_users.City.str.replace('ώ','o')

casino_users.City = casino_users.City.str.capitalize()

casino_users.loc[casino_users.CountryName == 'Greece', "City"] = casino_users.loc[casino_users.CountryName == 'Greece',"City"].str.replace('y','i')
casino_users.loc[casino_users.CountryName == 'Greece', "City"] = casino_users.loc[casino_users.CountryName == 'Greece',"City"].str.replace('oi','i')
casino_users.loc[casino_users.CountryName == 'Greece', "City"] = casino_users.loc[casino_users.CountryName == 'Greece',"City"].str.replace('ei','i')

casino_users.loc[casino_users.City == 'Athina', "City"] = 'Athens'
casino_users.loc[casino_users.City == 'Halkida', "City"] = 'Chalkida'
casino_users.loc[casino_users.City == 'Xalkida', "City"] = 'Chalkida'
casino_users.loc[casino_users.City == 'Xania', "City"] = 'Chania'
casino_users.loc[casino_users.City == 'Hania', "City"] = 'Chania'


#Calculate Age of User and Months that has been a member
def calc_age(born):
    today = datetime.date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

casino_users['Age'] = casino_users['BirthDate'].apply(lambda x: calc_age(x))

casino_users['MonthsMember'] = datetime.date.today()
casino_users.MonthsMember = pd.to_datetime(casino_users.MonthsMember)
casino_users['MonthsMember'] = ((casino_users.MonthsMember - casino_users['Registration Date'])/np.timedelta64(1, 'M'))
casino_users.MonthsMember = casino_users.MonthsMember.astype(int)



#Check for duplicates and remove
print('Casino Users Duplicate Rows:')
print(casino_users.duplicated().sum())
casino_users = casino_users.drop_duplicates()
print("Removed. No of duplicates:")
print(casino_users.duplicated().sum())

print('Casino Users Rows with Duplicate UserId+Status:')
print(casino_users.duplicated(['UserProfileId','StatusSysname']).sum())
casino_users = casino_users.drop_duplicates(subset=['UserProfileId','StatusSysname'])
print("Removed. No of duplicates:")
print(casino_users.duplicated(['UserProfileId','StatusSysname']).sum())

print('Casino Users Rows with Duplicate UserId:')
print(casino_users.duplicated(['UserProfileId']).sum())
casino_users = casino_users.drop_duplicates(subset=['UserProfileId'])
print("Removed. No of duplicates:")
print(casino_users.duplicated(['UserProfileId']).sum())

casino_users.to_csv('Casino Users New.csv')

#Customer Wallet Data
customer_wallet.Created = pd.to_datetime(customer_wallet.Created)
customer_wallet = customer_wallet.sort_values(by=['UserProfileId', 'Type', 'Created'])

#Calculate interval between deposit or withdraw
customer_wallet['Interval'] = customer_wallet.Created.diff().apply(lambda x: x/np.timedelta64(1, 'D'))

mask1 = customer_wallet[['UserProfileId']] != customer_wallet[['UserProfileId']].shift(1) 
mask2 = customer_wallet[['Type']] != customer_wallet[['Type']].shift(1) 
mask3 = mask1.UserProfileId + mask2.Type

customer_wallet.Interval[mask3] = np.nan
customer_wallet.Interval = customer_wallet.Interval.fillna(0).astype(int)

#Check for Duplicates
print('Customer Wallet Duplicate Rows:')
print(customer_wallet.duplicated().sum())

customer_wallet.to_csv('Customer Wallet New.csv')

#Casino Games
print('Casino Games Duplicate Rows')
print(casino_games.duplicated().sum())


