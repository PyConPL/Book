#Learn Django and Redis by Visualizing Twitter data - Haris Ibrahim K V

Autobots, transform and roll out!

##1. The origin of Django.

This will be a quick story about how Django came into being. It will
be kept to a minimum. The only intention is to welcome the audience
gracefully and plug in a little bit of inspiration showing how
wonderful things can happen from any of us.

##2. A general note on how a website works.

Again, this will be a quick picture of what all is involved in getting
a website up and running. The intention is to get the audience to
understand where Django fits in, in the bigger picture.  To be
explained by mentioning something like "What happens when you type in
google.com and hit enter?"

##3. Introducing the idea of MVC architecture.

This part will explain what a web framework is and how it will make
your life easier. Model, View and Controller will be explained one by
one, and mapped to the corresponding layer in Django.

##4. Starting off with Django.

Creating a project with Django. The hard part where the concept of a
"project" and "app" will be explained. The skeleton structures will be
discussed, including how the "project" is where everything starts
from. We will talk in a bit more detail regarding urls, views and the
ORM here.

##4. Creating your first Django app.

Creating your first app with Django. The concept of having to use apps
in order to modularize your code will be explained in much more
details over here.

##5. Customary "Hello, World" tutorial.

About time to put the knowledge of URLS and views into practice.

##6. Enter Templates.

We will play around with a few examples of directly returning an
HttpResponse and rendering templates. Passing in values, etc.

##7. Defining the problem statement.

The problem statement will be defined here. Fetching tweets related to
a certain hashtag from Twitter, storing them, and visualizing
them. Not just that, but we want to know the most popular tweets
(based on RT count) and the total number of tweets. These two use
cases will be covered by Redis.

##8. A small intro to Redis.

The definition of Redis and what a NoSQL datastore is. The different
data structures that it provides. More questions towards the end of
the session after seeing it in action.

##9. Thinking about models.

Now that we have the problem statement, let's decide our model
structure. The models will be agreed upon and implemented in this
phase. An elaborate note on syncdb and a quick note on migrations.

##10. Introducing ORM functions.

Dropping down to the shell, we will play around with creating a few
objects, retrieving and inspecting them.

##11. Receiving input from the user.

We will talk about Django forms here in order to implement a small
form through which we receive the username and the hashtag to be
tracked.

##12. The archival.

Once the user input comes through, how to invoke Twython in order to
fetch the Tweets from Twitter.

##13. Processing Tweets.

Code to process each tweet. Extracting the fields that we require from
within the jsons and saving them into the model.

##14. Plugging in redis.

Putting redis in between the archival process to implement the
leaderboard and count.

##15. A new view!

Creating a new URL and a view for displaying whatever we processed.

##16. Visualizing.

Fetch the contents from the DB within the new view. Writing code to
make it into a visualizable format, and passing it over to the
templates. This part will also cover fetching the saved data from
redis and sending that along as well.

##17. A note on static files.

In order to visualize, we will be using the JS library
Chart.js.However, we need to understand where to put our CSS, JS files
so that it can be served. That will be explained here.

##18. The Grand finale. Visualize!

Once the static files are served, we will use Chart to visualize the
processed data in a new template.

##19. Redis as cache.

If time permits, we will try to implement a really simple caching
mechanism in Redis to show the popular photos as well.
