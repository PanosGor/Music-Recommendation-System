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

### SUMMARY OF DATA 

The analysis of the data provided the following results:

-	In total 17632 unique Artist IDs were found
-	1892 unique User IDs were found
-	11946 different Tag IDs were found
-	92834 unique combinations of users and artist IDs. This is the total number of artists that have been heard by all users in the dataset
-	25434 total Friend Relationships among Users. This number refers to all the user interrelationships or the total number of friends per user for all users
-	186479 total Tag Assignments by all users
-	Ratings Range = 352697 (Highest rate = 352698, Lowest Rate = 1)
-	
As can be seen from the above analysis one of the worth mentioning results is the huge rating range (352697) this inconsistency in the dataset can create inaccurate results. 

*Graph 1*

![image](https://user-images.githubusercontent.com/82097084/166108196-e9a05a8f-41ee-4ac8-bde6-6b5330d2e099.png)

Graph 1 provides a graphical representation of the frequency that each artist had been heard by the users. 
The vertical axis (y) describes the artist frequency while at the horizontal axis (x) is the names of the bands. 
In the Graph only few band names appear as there are more than 17 thousand artists in the dataset and presenting all of them would not provide any useful insight.

*Graph 2*

![image](https://user-images.githubusercontent.com/82097084/166108217-6b9a1f2d-108d-463d-972c-4001f35657b8.png)

Graph 2 provides a graphical representation of the tag frequency per user. 
More specifically on the vertical axis(y) the Tag frequencies are presented while on the horizontal axis (x) the user IDs are presented. 
Again, only few of the User IDs are presented as there are more than 1800 users in the dataset.

*Graph 3*

![image](https://user-images.githubusercontent.com/82097084/166108250-5a8b6dfd-a5dc-4360-a94f-cc084fd0a578.png)

Graph 3 provides a graphical representation of the Tags frequency per artist. 
The vertical axis (y) presents the Tag frequency per artist while on the horizontal axis(x) the artist IDs are presented. 
Due to the thousands of artists IDs only few of them are presented in the graph in order to ensure readability.

### OUTLIER DETECTION 

Outliers are cases that have data values that are very different from the rest of the dataset. 
Usually, they can take extremely high or extremely low values. 
Detecting and handling outliers is a very important step because they can affect the results of the analysis.
A good method to usually detect outliers is to find all the data values that are more than 3 standard deviations away from the mean of the population.

*Graph 4*

![image](https://user-images.githubusercontent.com/82097084/166108328-4372892b-c640-44ec-b398-3a38250f3e14.png)

For the outlier detection among the users in terms of how many tags they have used as well as the outliers among the tags in terms of how many times they were used by users the same methodology was used. 
More specifically the mean and standard deviation was calculated for the users in terms of how many tags they have used as well as the mean and standard deviation for the tags in terms of how many times they were used by users. 

Then the upper and lower limits for each population were calculated:
-	Upper Limit = population_mean() + (population_std()*3)
-	Lower Limit= population_mean() - (population_std ()*3)
-	Any values bigger than the upper limit or smaller than the lower limit automatically considered to be an outlier
-	
The analysis for the two populations shown the following results:
-	Out of the total 11946 tags 68 outliers were found in terms of how many the tag IDs have been used by the users
-	Out of the total 1892 user IDs 40 outliers were found in terms of how many tags they have used



