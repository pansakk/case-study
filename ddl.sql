CREATE DATABASE novibet;
GO

USE novibet;
GO

CREATE TABLE dbo.countries(
    [country_id] SMALLINT NOT NULL,
    [country_name] VARCHAR(20) NOT NULL

    CONSTRAINT [pk_country_id] PRIMARY KEY([country_id] ASC) 
)

CREATE TABLE dbo.casino_users(
    [user_profile_id] INT NOT NULL,
    [birth_date] DATE NOT NULL,
    [zipcode] VARCHAR(10) NOT NULL,
    [sex] CHAR(1) ,
    [reg_date] DATETIME NOT NULL,
    [city] VARCHAR(50) NOT NULL,
    [country_id] SMALLINT NOT NULL,
    [status_sysname] VARCHAR(10)


    CONSTRAINT [pk_user_profile_id] PRIMARY KEY CLUSTERED([user_profile_id] ASC) ,
    CONSTRAINT [fk_country_id] FOREIGN KEY(country_id) REFERENCES dbo.countries(country_id) ON UPDATE CASCADE ON DELETE CASCADE ,

    CONSTRAINT [ch_sex] CHECK([sex] IN ('F', 'M')) ,
    CONSTRAINT [ch_status] CHECK([status_sysname] IN ('TEST', 'ACTIVE', 'INACTIVE'))
)

CREATE TABLE dbo.customer_wallet(
    [wallet_action_id] INT NOT NULL,
    [user_profile_id] INT NOT NULL,
    [type] CHAR(1) ,
    [type_sysname] CHAR(8) ,
    [amount] REAL NOT NULL,
    [method_sysname] VARCHAR(20) NOT NULL,
    [created] DATETIME2 NOT NULL 

    CONSTRAINT [pk_wallet_id] PRIMARY KEY([wallet_action_id] ASC) ,
    CONSTRAINT [fk_user_id] FOREIGN KEY(user_profile_id) REFERENCES dbo.casino_users(user_profile_id) ON UPDATE CASCADE ON DELETE CASCADE ,
    
    CONSTRAINT [ch_type] CHECK([type] = '1' OR [type] = '2') ,
    CONSTRAINT [ch_typename] CHECK([type_sysname] IN ('DEPOSIT','WITHDRAW'))
)

CREATE TABLE dbo.casino_games(
    [casino_provider] VARCHAR(20) NOT NULL,
    [user_id] INT NOT NULL,
    [jackpot_id] SMALLINT ,
    [free_spin_id] SMALLINT ,
    [date] DATE NOT NULL,
    [live_id] SMALLINT ,
    [hold] REAL NOT NULL

    CONSTRAINT [fk_user_id2] FOREIGN KEY([user_id]) REFERENCES dbo.casino_users(user_profile_id) ON UPDATE CASCADE ON DELETE CASCADE ,

    CONSTRAINT [ch_jackpot] CHECK([jackpot_id] IN (0, 1)) ,
    CONSTRAINT [ch_free_spin] CHECK([free_spin_id] IN (0, 1)) ,
    CONSTRAINT [ch_live] CHECK([live_id] IN (0, 1))
)



