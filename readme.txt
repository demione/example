1. install the latest distros of the following:
   a. python 2
   b. virtualenv
   c. tornado
2. pull [server git address]
   a. cd [server dictionary]
   b. virtualenv env
   c. source env/bin/activate
   d. pip install -r requirements.txt
   e. python setup.py install
   f. python FreshTomatoes.py
3. to access the service:
   a. GET http://[server address]:8080/movies
   b. GET http://[server address]:8080/movie/[movie_name]
   c. POST http://[server address]:8080/movie {movie_name, image_url, rating, description}
   d. DELETE http://[server address]:8080/movie/[movie_name]
