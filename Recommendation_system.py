import pandas as pd
import numpy as np
import math
from sklearn.metrics.pairwise import cosine_similarity

def standardize_df(row):
    new_row=(row-row.mean())/(row.max()-row.min())
    return new_row

def findKNeighbors(df,k):
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False).iloc[:k].index),axis=1)
    df.columns=[f"User{i}" for i in range(1,k+1)]
    return df

def artists_for_consideration(similar_users,artists_per_user,user):
    results=[]
    artists_our_user_likes=artists_per_user[user]
    for u in similar_users:
        for artist in artists_per_user[u]:
            if(artist not in artists_our_user_likes):
                results.append(artist)
    return list(set(results))

def artists_per_user(df,neighbor_users,user):
    results={}
    neighbor_users.append(user)
    for user in neighbor_users:
        results[user]=list(df.columns[df[df.index==user].notna().any()])
    return results

def artists_per_neighbor(some_dict,neighbors):
    art_per_neighb={}
    for user in neighbors:
        art_per_neighb[user]=some_dict[user]
    return art_per_neighb

def friends_reweighting(file_path,user_sim,users_correlation,user):
    friends_df=pd.read_csv(file_path+"\\user_friends.dat",sep="\t")
    list_of_friends=friends_df.groupby('userID')['friendID'].apply(list)
    for user_friend in user_sim:
        if(user_friend in list_of_friends.loc[user]):
            users_correlation2=users_correlation.replace(to_replace = users_correlation.loc[user_friend], value = users_correlation.loc[user_friend]*2)
    return users_correlation2

def artists_ratings(artists,df_mr,df,neighbors,user,similarity):
    results=[]
    for artist in artists:
        #neighbors_average_ratings calculkates the average rating of the siliar users for the artist
        neighbors_average_ratings=df_mr[artist][df_mr[artist].index.isin(neighbors)]
        #is the average of all ratings the user has given
        ratings_avg=df.groupby("id")["rating"].mean().loc[user]
        #gives us the correlations between the target user and his neighbors
        users_correlation=similarity.loc[user,neighbors]
        df_concat=pd.concat([neighbors_average_ratings, users_correlation], axis=1)
        df_concat.columns=['predicted_score','user_correlation']
        df_concat['final_score']=df_concat.apply(lambda x:x['predicted_score'] * x['user_correlation'],axis=1)
        numerator=df_concat['final_score'].sum()
        denominator = df_concat['user_correlation'].sum()
        final_results = ratings_avg + (numerator/denominator)
        results.append(final_results)
    return results

# This function is an alternative of artists_ratings that takes into consideration the users friends
#and doubles their equivalent weights
def artists_ratings2(artists,df_mr,df,neighbors,user,similarity,file_path,user_sim):
    results=[]
    for artist in artists:
        #neighbors_average_ratings calculkates the average rating of the siliar users for the artist
        neighbors_average_ratings=df_mr[artist][df_mr[artist].index.isin(neighbors)]
        #is the average of all ratings the user has given
        ratings_avg=df.groupby("id")["rating"].mean().loc[user]
        #gives us the correlations between the target user and his neighbors
        users_correlation=similarity.loc[user,neighbors]
        users_correlation_rw=friends_reweighting(file_path,user_sim,users_correlation,user)
        df_concat=pd.concat([neighbors_average_ratings, users_correlation_rw], axis=1)
        df_concat.columns=['predicted_score','user_correlation']
        df_concat['final_score']=df_concat.apply(lambda x:x['predicted_score'] * x['user_correlation'],axis=1)
        numerator=df_concat['final_score'].sum()
        denominator = df_concat['user_correlation'].sum()
        final_results = ratings_avg + (numerator/denominator)
        results.append(final_results)
    return results

def Prediction(userID,itemID,user_similarities,mean_artist,avg_urating,similarity_with_artist):
    Mean_ratings=avg_urating
    #Mean_ratings.set_index('id', inplace=True)
    a = user_similarities[user_similarities.index==userID].values
    b = a.squeeze().tolist()
    c = mean_artist.loc[:,itemID]
    d = c[c.index.isin(b)]
    f = d[d.notnull()]
    avg_user = Mean_ratings.loc[userID]['rating']
    #index = f.index.values.squeeze().tolist()
    #print(index)
    corr = similarity_with_artist.loc[userID,b]
    Mean_ratings=Mean_ratings.loc[b]['rating']
    fin = pd.concat([f, corr,Mean_ratings], axis=1)
    fin.columns = ['adg_score','correlation','Avg_rating']
    fin['score'] = fin['correlation'] * (fin['adg_score'] - fin['Avg_rating'])
    nume = fin['score'].sum()
    deno = fin['correlation'].sum()
    final_score = avg_user + (nume/deno)
    return final_score

print(" ")
print("Initializing...")
print(" ")
file_path='Data'
user_artists_df=pd.read_csv(file_path+"\\user_artists.dat",delimiter="\t",error_bad_lines=False)
user_artists_df.columns=['id','artistID','rating']
user_ids=user_artists_df['id'].values.tolist()
artist_ids=user_artists_df['artistID'].values.tolist()
true_ratings=user_artists_df['rating'].values.tolist()
user_artist=list(zip(user_ids, artist_ids,true_ratings))
Mean_user_ratings = user_artists_df.groupby(by="id",as_index=False)['rating'].mean()
final = pd.pivot_table(user_artists_df,values='rating',index='id',columns='artistID')
adj_rating=final.fillna(final.mean(axis=0))
final.fillna(0,inplace=True)
#2nd method instead of adj_rating: final_artist=final.apply(standardize_df)
final_artist=final.apply(standardize_df)
user_similarity = cosine_similarity(final_artist)
np.fill_diagonal(user_similarity, 0 )
similarity = pd.DataFrame(user_similarity,index=final_artist.index,columns=final_artist.index)
similarity.to_csv(file_path+'\\user-pairs-lastFM.data')
similar_users = findKNeighbors(similarity,5)
similar_users.to_csv(file_path+'\\neighbors-k-lastFM.data')



#Your can change the user's id here in case you want recomendations for another user other than user = 2
user=2
print(f"Fetching Results for user {user}...")
print(" ")
print(f"5 Most similar users to user {user}")
print(similar_users.loc[user])
print(" ")

artists_df=pd.read_csv(file_path+"\\artists.dat",delimiter="\t",error_bad_lines=False)
user_sim=similar_users.loc[user].values.tolist()
final1=pd.pivot_table(user_artists_df,values='rating',index='id',columns='artistID')
user_pref=artists_per_user(final1,user_sim,user)
artists_to_check=artists_for_consideration(user_sim,user_pref,user)
#scores=artists_ratings(artists_to_check,adj_rating,user_artists_df,user_sim,user,similarity)
scores=artists_ratings2(artists_to_check,adj_rating,user_artists_df,user_sim,user,similarity,file_path,user_sim)
df_score=pd.DataFrame({'artistID':artists_to_check,'score':scores})
top_recom=df_score.sort_values(by='score',ascending=False).head(5)
Top_Artists= top_recom.merge(artists_df, how='inner', left_on='artistID', right_on = 'id')
final_df=Top_Artists.drop(["artistID","id","url","pictureURL"],axis=1)


print(f"Recomended Artists for user {user}")
print(final_df)

#Calculating a threshold for all artists in order to use it and calculate Tp , fp, fn for Precision and Recall
artists_mean_rat=user_artists_df.groupby(["artistID"]).mean()
new_df=artists_mean_rat.drop(columns='id')
Mean_rating_thresh=int(new_df.mean())
print(" ")
print(f"Mean Rating Threshold : {Mean_rating_thresh}")

print(" ")
print("Calculating MAE/RMSE/Precision/Recall/F1 this can take up to 5 minutes...")
Mean_ratings=Mean_user_ratings
Mean_ratings.set_index('id', inplace=True)
mae=0
rmse=0
tp=0
fp=0
fn=0
for i in user_artist:
    user_item_pred=Prediction(i[0],i[1],similar_users,adj_rating,Mean_user_ratings,similarity)
    mae=mae+np.abs(user_item_pred-i[2])
    rmse=rmse+((user_item_pred-i[2])**2)
    if user_item_pred>Mean_rating_thresh and i[2]>Mean_rating_thresh:
        tp+=1
    elif user_item_pred>Mean_rating_thresh and i[2]<Mean_rating_thresh:
        fp+=1
    elif user_item_pred<Mean_rating_thresh and i[2]>Mean_rating_thresh:
        fn+=1
final_mae=mae/len(user_artist)
final_rmse=math.sqrt(rmse/len(user_artist))
precision=tp/(tp+fp)
recall = tp/(tp+fn)
f1=2*precision*recall/(precision+recall)
print(" ")
print(f"Final MAE = {round(final_mae,2)}")
print(f"Final RMSE = {round(final_rmse,2)}")
print(f"Precision = {round(precision,2)}")
print(f"Recall = {round(recall,2)}")
print(f"F1 = {round(f1,2)}")