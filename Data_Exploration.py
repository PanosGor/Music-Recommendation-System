import pandas as pd
import numpy as n
import matplotlib.pyplot as plt



def reading_data(path):
    artists_df=pd.read_csv(path+"\\artists.dat",delimiter="\t",error_bad_lines=False)
    uart_df=pd.read_csv(path+"\\user_artists.dat",delimiter="\t")
    user_artists_tags=pd.read_csv(path+"\\user_taggedartists.dat",delimiter="\t")
    uart_df.columns=["userID","id","weight"]
    merged_df=pd.merge(artists_df,uart_df,on="id")
    artists_fr=merged_df.groupby("name")["userID"].count()
    return artists_fr,user_artists_tags

def plot_artists_fr(df):
    fig1,ax1=plt.subplots(figsize=(9,5))
    df.plot(ax=ax1)
    ax1.set_title("Artists Frequency")
    ax1.set_xlabel("Artists")
    ax1.set_ylabel("Viewing Frequency")
    ax1.tick_params(axis='x', rotation=90)

def plot_user_tags(df):
    new_df=df.groupby(["userID"]).count()
    fig2,ax2=plt.subplots(figsize=(9,5))
    new_df["tagID"].plot(ax=ax2)
    ax2.set_title("Tags Frequency per User")
    ax2.set_xlabel("User ID")
    ax2.set_ylabel("Tags Frequency")
    ax2.tick_params(axis='x', rotation=90)
    return new_df

def plot_artist_tags(df):
    new_df=df.groupby(["artistID"]).count()
    fig3,ax3=plt.subplots(figsize=(9,5))
    new_df["tagID"].plot(ax=ax3)
    ax3.set_title("Tags Frequency per Artist")
    ax3.set_xlabel("Artist ID")
    ax3.set_ylabel("Tags Frequency")
    ax3.tick_params(axis='x', rotation=90)
    return new_df

def check_outliers(df):
    upper=df.mean()+(df.std()*3)
    lower=df.mean()-(df.std()*3)
    outliers_df=df[(df>upper)|(df<lower)]
    return outliers_df

file_path="Data"
artists_fr,user_artist_tgs=reading_data(file_path)
plot_artists_fr(artists_fr)
x=plot_user_tags(user_artist_tgs)
y=plot_artist_tags(user_artist_tgs)

print(" ")
Tags_fr=user_artist_tgs.groupby("tagID")["userID"].count()
TagsID_outliers=check_outliers(Tags_fr)
print(f"Out of the total {Tags_fr.count()} tags {TagsID_outliers.count()} outliers were found")

print(" ")
user_fr=user_artist_tgs.groupby("userID")["tagID"].count()
userID_outliers=check_outliers(user_fr)
print(f"Out of the total {user_fr.count()} userIDs {userID_outliers.count()} outliers were found")
print(" ")