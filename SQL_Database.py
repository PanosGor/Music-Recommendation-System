import pymysql
import pandas as pd
import numpy as np

mydb=pymysql.connect(host="localhost",user="",passwd="")
mycursor=mydb.cursor()
mycursor.execute("DROP DATABASE IF EXISTS lastfm")
mycursor.execute("CREATE DATABASE lastfm")
mycursor.execute("USE lastfm")

mycursor.execute("CREATE TABLE artists (id INT(20) NOT NULL PRIMARY KEY,name CHAR(200),url CHAR(255),pictureURL CHAR(255))")
mycursor.execute("CREATE TABLE tags (tagID INT(20) NOT NULL PRIMARY KEY,tagValue CHAR(200))")
mycursor.execute("CREATE TABLE userartists (userid INT(20) NOT NULL,artistid INT(20),FOREIGN KEY(artistid) REFERENCES artists(id),weight INT(20),PRIMARY KEY(userid,artistid))")
mycursor.execute("CREATE TABLE userfriends (userid INT(20),friendid INT(20))")
mycursor.execute("CREATE TABLE taggerartists (userid INT(20),artistid INT(20),tagid INT(20),day INT(2),month INT(2),year INT(4))")
mycursor.execute("CREATE TABLE taggerartiststimestamps (userid INT(20),artistid INT(20),tagid INT(20),timestamp CHAR(30))")


artists_df=pd.read_csv("Data\\artists.dat",delimiter="\t",error_bad_lines=False)
artists_df=artists_df.replace(np.nan,'empty')
tags_df=pd.read_csv("Data\\tags.dat",delimiter="\t",error_bad_lines=False)
tags_df=tags_df.replace(np.nan,'empty')
user_artists_df=pd.read_csv("Data\\user_artists.dat",delimiter="\t",error_bad_lines=False)
user_artists_df=user_artists_df.replace(np.nan,'empty')
user_friends_df=pd.read_csv("Data\\user_friends.dat",delimiter="\t",error_bad_lines=False)
user_friends_df=user_friends_df.replace(np.nan,'empty')
user_taggedartists_df=pd.read_csv("Data\\user_taggedartists.dat",delimiter="\t",error_bad_lines=False)
user_taggedartists_df=user_taggedartists_df.replace(np.nan,'empty')
user_taggedartists_timestamps_df=pd.read_csv("Data\\user_taggedartists_timestamps.dat",delimiter="\t",error_bad_lines=False)
user_taggedartists_timestamps_df=user_taggedartists_timestamps_df.replace(np.nan,'empty')


list_artists=[tuple(row) for i,row in artists_df.iterrows()]
list_tags=[tuple(row) for i,row in tags_df.iterrows()]
user_artists_list=[tuple(row) for i,row in user_artists_df.iterrows()]
user_friends_list=[tuple(row) for i,row in user_friends_df.iterrows()]
user_taggedartists_list=[tuple(row) for i,row in user_taggedartists_df.iterrows()]
user_taggedartists_timestamps_list=[tuple(row) for i,row in user_taggedartists_timestamps_df.iterrows()]

sql1="INSERT INTO artists (id,name,url,pictureURL) VALUES (%s,%s,%s,%s)"
sql2="INSERT INTO tags (tagID,tagValue) VALUES (%s,%s)"
sql3="INSERT INTO userartists (userid,artistid,weight) VALUES (%s,%s,%s)"
sql4="INSERT INTO userfriends (userid,friendid) VALUES (%s,%s)"
sql5="INSERT INTO taggerartists (userid,artistid,tagid,day,month,year) VALUES (%s,%s,%s,%s,%s,%s)"
sql6="INSERT INTO taggerartiststimestamps (userid,artistid,tagid,timestamp) VALUES (%s,%s,%s,%s)"

mycursor.executemany(sql1,list_artists)
mydb.commit()

mycursor.executemany(sql2,list_tags)
mydb.commit()

mycursor.executemany(sql3,user_artists_list)
mydb.commit()

mycursor.executemany(sql4,user_friends_list)
mydb.commit()

mycursor.executemany(sql5,user_taggedartists_list)
mydb.commit()

mycursor.executemany(sql6,user_taggedartists_timestamps_list)
mydb.commit()

mydb.close()

