# Music-Recommendation-System
This a Recomendation system made in Python based on the famous last-fm dataset


## PROJECT REVIEW

Main purpose of this project is to create a recommendation system for artists. 
The system will recommend to users new artists they have never heard of before and these artists will be close to the users’ taste in music. 
To achieve that a user based collaborative filtering methodology was used. 
According to this method, recommendations can be made to a user that derives from the taste of another user with similar taste. 
One of the main drawbacks of this method is that new users that the system does not have enough data yet cannot match them to other users.

During the analysis:

-	Examined the data for patterns 
-	Preprocessed the data to handle outliers
-	Found the k nearest users per user
-	Created a recommendation system by using the user based collaborative filtering methodology and by including into the model friendship relationship among users
-	Evaluated the systems results by using MAE, RMSE, Precision, Recall, F1

## DATA DESCRIPTION

For the creation and the analysis 6 data files were used:

-	Artists.dat which contains a list with all the artists of Last.FM
-	Tags.dat which contains a list with all the tag IDs of Last.FM and their meaning
-	User_Artists.dat which contains a list with all the User IDs of Last.FM and their favorite Artists as well as the User Ratings for the artists
-	User_friends.dat which contains a list of all the friend IDs per user
-	User_taggedartists.dat which provides information with regards to the number of tags per user 
-	user_taggedartists_timestamps.dat which provides information with regards to the number of tags per user in addition to information with regards to date and time of each tag made by each user
