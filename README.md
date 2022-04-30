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

### DATA PREPROCESSING

As was discussed earlier the range of the users’ ratings is extremely high 352697 with 352698 being the highest rating in the dataset and 1 being the smallest user rating in the dataset. 
As a result, the outliers among the users’ rating were affecting the analysis. 

**An example from a user case:**
User 2 which also happens to be the first user in the data set (user_artist.dat) had high ratings for her favorite artists. 
Among the artists that user 2 liked was artist ID 51 with a rating of 13883. User 1454 had 11 common artists with similar ratings to user 2 but user 1505 had only one common artist with user 2 and that is Artist ID 51 with a rating of 13790. 
As a result, Users 1505 because of the common ratings, he had for Artists 51 would be categorized as much more similar User 2. 
Even though in reality User 1454 has more similar taste in music to User 2.
To fix this issue a standardization methodology was used on the dataset in order to standardize the values in the dataset. 

More specifically the following formula was used:

-	new_rating=(rating-user_ratings.mean())/(user_ratings.max()- ratings.min())

The reason behind this, is to bring the mean of all the ratings that the User gives to 0 and dividing it by the range of the ratings of the User. 
The range of the new values is [-1,1]. This method can correct for any users that are too harsh (very low ratings) or too lenient (very high ratings).
Negative values indicated no interest or dislike to the artist while positive values indicating positive feedback to the artist by the user with values closer to one indicating high ratings

*Screenshot 1*

![image](https://user-images.githubusercontent.com/82097084/166108503-bbf7afbe-9559-4277-be66-e7ec4ca31d10.png)


After applying the standardization function on the dataset, the next step was to find the similarity between the users. 
In order to do that, the angular distance between the ratings needed to be calculated. Cosine_similarity function from Sklearn library was used in order to calculate the similarity among the users. 
The result was a new dataframe that had the users both on the vertical and the horizontal axis and for every row the cosine similarity of each user to the rest of the users in the dataset. 
The idea behind cosine similarity because every row in the dataframe is expressed as vector and in this case every row expresses a different user. 
The whole dataset can be expressed in vector space. Users that have similar tastes in music have smaller angular distance than the rest of the users. 
The similarity is calculated based on the following formula:

![image](https://user-images.githubusercontent.com/82097084/166108564-a89fd1b7-b9c7-4bb8-a55b-ff354c0fba24.png)



