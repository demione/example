import tornado.ioloop
import pyrestful.rest
import tornado.web
import tornado.options
import tornado.httpserver
import logging
import os
import tornado.escape
import sqlite3
import urllib2
import hashlib
from datetime import datetime
from pyrestful import mediatypes
from pyrestful.rest import get, post, put, delete

databaseName = 'FreshTomatoes.db'

class Movie(object):
    movie_name = str
    image_url = str
    rating = float
    description = str
	
class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'version': '1.0.0' }
        self.write(response)

class DatabaseHandler():
    con = sqlite3.Connection
    cur = sqlite3.Cursor
    
    def __init__(self):
        try:
            self.con = sqlite3.connect(databaseName)
            self.cur_con()
        except sqlite3.Error, e:
            print "Error %s" % (e.args[0])
            return None

    def __del__(self):
        if self.con:
            self.con.close()

    def cur_con(self):
        self.cur = self.con.cursor()
        
    def is_request_valid(self, postbody):
        illegalCharacters = '`'
        for char in illegalCharacters:
          if char.lower() in postbody.lower():
            print "unquoted postbody failed validation check"
            return False
          if char.lower() in urllib2.unquote(postbody):
            print "postbody failed validation check"
            return False

        return True

    def query_one(self, sql, params, commit=False):
        self.cur_con()
        self.cur.execute(sql, params)
        if commit == False:
            data = self.cur.fetchone()
            self.cur.close()
            return data
        else:
            self.con.commit()
            id = self.con.insert_id()
            self.cur.close()
            return id

    def query_one_dict(self, sql, params, commit=False):
        self.cur_con()
        self.cur.execute(sql, params)
        if commit == False:
            data = self.cur.fetchone()
            if data is None: return None
            cols = [ d[0] for d in self.cur.description ]
            self.cur.close()
            return dict(zip(cols, data))
        else:
            self.con.commit()
            id = self.con.insert_id()
            self.cur.close()
            return id

    def query_one_dict_noparams(self, sql, commit=False):
        self.cur_con()
        self.cur.execute(sql)
        if commit == False:
            data = self.cur.fetchone()
            if data is None: return None
            cols = [ d[0] for d in self.cur.description ]
            self.cur.close()
            return dict(zip(cols, data))
        else:
            self.con.commit()
            id = self.con.insert_id()
            self.cur.close()
            return id

    def query_all_dict(self, sql):
        self.cur_con()
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        if rows is None: return None
        cols = [ d[0] for d in self.cur.description ]
        self.cur.close()
        data = []
        for row in rows:
          data.append(dict(zip(cols, row)))
        return data

    def query_execute(self, sql, params):
        self.cur_con()
        self.cur.execute(sql, params)
        self.con.commit()
        self.cur.close()
        return

    def query_execute_noparams(self, sql):
        self.cur_con()
        self.cur.execute(sql)
        self.con.commit()
        self.cur.close()
        return
        
    def select_movies(self):
        sql = """SELECT movie_name, image_url, rating, description FROM Movies"""
        moviesArray = self.query_all_dict(sql)
        response = []
        if moviesArray != None and moviesArray != []:
            for movie in moviesArray:
                responseElement = dict()
                responseElement['movie_name'] = tornado.escape.url_unescape(movie['movie_name'])
                responseElement['image_url'] = tornado.escape.url_unescape(movie['image_url'])
                responseElement['rating'] = tornado.escape.url_unescape(str(movie['rating']))
                responseElement['description'] = tornado.escape.url_unescape(movie['description'])
                response.append(responseElement)
        #print response
        return response
        
    def select_movie(self, movie_name):
        if self.is_request_valid(movie_name) == False:
            return None
        sql = """SELECT movie_name, image_url, rating, description FROM Movies WHERE LOWER(movie_name) = ?"""
        #print movie_name
        escapedMovieName = tornado.escape.url_escape(tornado.escape.url_unescape(movie_name)).lower()
        params = (escapedMovieName,)
        movieDict = self.query_one_dict(sql,params)
        #print movieDict
        movie = None
        if movieDict != None and movieDict != []:
            movie = Movie()
            movie.movie_name = tornado.escape.url_unescape(movieDict['movie_name'])
            movie.image_url = tornado.escape.url_unescape(movieDict['image_url'])
            movie.rating = tornado.escape.url_unescape(str(movieDict['rating']))
            movie.description = tornado.escape.url_unescape(movieDict['description'])
        return movie
        
    def insert_movie(self, movie_name, image_url, rating, description):
        movie = DatabaseHandler().select_movie(movie_name)
        sql = """INSERT INTO Movies (movie_name, image_url, rating, description) VALUES (?, ?, ?, ?)"""
        params = (tornado.escape.url_escape(movie_name), tornado.escape.url_escape(image_url), rating, tornado.escape.url_escape(description))
        db.query_execute(sql, params)
        return self.select_movie(movie_name)
        
    def delete_movie(self, movie_name):
        movie = DatabaseHandler().select_movie(movie_name)
        sql = """DELETE FROM Movies WHERE movie_name = ?"""
        params = (tornado.escape.url_escape(movie_name),)
        db.query_execute(sql, params)

class MovieResource(pyrestful.rest.RestHandler):

    @get(_path="/movies", _produces=mediatypes.APPLICATION_JSON)
    def getMovies(self):
        movies = DatabaseHandler().select_movies()
        return movies
        
    @get(_path="/movie/{movie_name}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def getMovie(self, movie_name):
        movie = DatabaseHandler().select_movie(movie_name)
        if movie == None:
            self.gen_http_error(404,"Error 404 : no such movie exists")
        return movie
        
    @delete(_path="/movie/{movie_name}", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def deleteMovie(self, movie_name):
        db = DatabaseHandler()        
        movie = None
        if db.is_request_valid(movie_name) == False or db.is_request_valid(image_url) == False or db.is_request_valid(rating) == False or db.is_request_valid(description) == False:
            self.gen_http_error(400,"Error 400 : bad request")
        else:
            movie = db.select_movie(movie_name)
        if movie == None:
            self.gen_http_error(404,"Error 404 : no such movie exists")
        else:
            db.delete_movie(movie_name)
        return movie
    
    @post(_path="/movie",_types=[str, str, str, str],_produces=mediatypes.APPLICATION_JSON)
    def postMovie(self, movie_name, image_url, rating, description):
        db = DatabaseHandler()
        movie = None
        if db.is_request_valid(movie_name) == False or db.is_request_valid(image_url) == False or db.is_request_valid(rating) == False or db.is_request_valid(description) == False:
            self.gen_http_error(400,"Error 400 : bad request")
        else:
            movie = db.insert_movie(movie_name, image_url, rating, description)
        if movie == None:
            self.gen_http_error(404,"Error 404 : a movie with this name already exists")
        return movie



def rebuild_db():
    if os.path.isfile(databaseName):
        os.remove(databaseName)
    db = DatabaseHandler()
    db.cur_con()
    
    db.query_execute_noparams("CREATE TABLE Movies (movie_name TEXT, image_url TEXT, rating FLOAT, description TEXT)")
    
    db.query_execute("""INSERT INTO Movies (movie_name, image_url, rating, description) VALUES (?, ?, ?, ?)""", (tornado.escape.url_escape("Avengers - Age of Ultron"), tornado.escape.url_escape("https://resizing.flixster.com/s8kIQtOhr36lGPkcUGCVeqVWw9Y=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/19/01/11190143_ori.jpg"), 4.5, tornado.escape.url_escape("When Tony Stark jumpstarts a dormant peacekeeping program things go awry and Earth's Mightiest Heroes, including Iron Man, Captain America Thor, The Incredible Hulk, Black Widow and Hawkeye, are put to the ultimate test as they battle to save the planet from destruction at the hands of the villainous Ultron.")))
    
    db.query_execute("""INSERT INTO Movies (movie_name, image_url, rating, description) VALUES (?, ?, ?, ?)""", (tornado.escape.url_escape("Furious 7"), tornado.escape.url_escape("https://resizing.flixster.com/tBSZ6CjTf-YkvC4o-VC0JFIY-vk=/170x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/18/14/11181482_ori.jpg"), 4.0, tornado.escape.url_escape("Continuing the global exploits in the unstoppable franchise built on speed, Vin Diesel, Paul Walker and Dwayne Johnson lead the returning cast of Fast & Furious 7. James Wan directs this chapter of the hugely successful series that also welcomes back favorites Michelle Rodriguez, Jordana Brewster, Tyrese Gibson, Chris Ludacris Bridges, Elsa Pataky and Lucas Black. They are joined by international action stars new to the franchise including Jason Statham, Djimon Hounsou, Tony Jaa, Ronda Rousey and Kurt Russell.")))
    
    db.query_execute("""INSERT INTO Movies (movie_name, image_url, rating, description) VALUES (?, ?, ?, ?)""", (tornado.escape.url_escape("Tomorrowland"), tornado.escape.url_escape("https://resizing.flixster.com/dH2TEhqdJ5A6xxV3mQBPZ_1yEac=/180x267/dkpu1ddg7pbsk.cloudfront.net/movie/11/19/06/11190666_ori.jpg"), 3.5, tornado.escape.url_escape("From Disney comes two-time Oscar (R) winner Brad Bird's riveting, mystery adventure Tomorrowland, starring Academy Award (R) winner George Clooney. Bound by a shared destiny, former boy-genius Frank (Clooney), jaded by disillusionment, and Casey (Britt Robertson), a bright, optimistic teen bursting with scientific curiosity, embark on a danger-filled mission to unearth the secrets of an enigmatic place somewhere in time and space known only as Tomorrowland. What they must do there changes the world-and them-forever. Featuring a screenplay by Lost writer and co-creator Damon Lindelof and Brad Bird, from a story by Lindelof & Bird & Jeff Jensen, Tomorrowland promises to take audiences on a thrill ride of nonstop adventures through new dimensions that have only been dreamed of.(C) Walt Disney")))
    
    db.query_execute("""INSERT INTO Movies (movie_name, image_url, rating, description) VALUES (?, ?, ?, ?)""", (tornado.escape.url_escape("Pitch Perfect 2"), tornado.escape.url_escape("https://resizing.flixster.com/CSaptdyboc7JUz266OumNJHeAl4=/180x257/dkpu1ddg7pbsk.cloudfront.net/movie/11/19/12/11191224_ori.jpg"), 3.0, tornado.escape.url_escape("Surprise hit Pitch Perfect gets sequelized in this Universal Pictures production once again scripted by Kay Cannon. ~ Jeremy Wheeler, Rovi")))
    
    db.query_execute("""INSERT INTO Movies (movie_name, image_url, rating, description) VALUES (?, ?, ?, ?)""", (tornado.escape.url_escape("Mad Max: Fury Road"), tornado.escape.url_escape("https://resizing.flixster.com/GbDqFVUc_9VBNAnanZVQxlYD0ZM=/180x267/dkpu1ddg7pbsk.cloudfront.net/movie/11/19/12/11191276_ori.jpg"), 4.0, tornado.escape.url_escape("Filmmaker George Miller gears up for another post-apocalyptic action adventure with Fury Road, the fourth outing in the Mad Max film series. Charlize Theron stars alongside Tom Hardy (Bronson), with Zoe Kravitz, Adelaide Clemens, and Rosie Huntington Whiteley heading up the supporting cast. ~ Jeremy Wheeler, Rovi")))
    
    db.query_execute("""INSERT INTO Movies (movie_name, image_url, rating, description) VALUES (?, ?, ?, ?)""", (tornado.escape.url_escape("Far From The Madding Crowd"), tornado.escape.url_escape("https://resizing.flixster.com/c8g2_ZQY4dBR7lxc9zWgzQnA01U=/180x267/dkpu1ddg7pbsk.cloudfront.net/movie/11/19/09/11190928_ori.jpg"), 4.5, tornado.escape.url_escape("Based on the literary classic by Thomas Hardy, FAR FROM THE MADDING CROWD is the story of independent, beautiful and headstrong Bathsheba Everdene (Carey Mulligan), who attracts three very different suitors: Gabriel Oak (Matthias Schoenaerts), a sheep farmer, captivated by her fetching willfulness; Frank Troy (Tom Sturridge), a handsome and reckless Sergeant; and William Boldwood (Michael Sheen), a prosperous and mature bachelor. This timeless story of Bathsheba's choices and passions explores the nature of relationships and love - as well as the human ability to overcome hardships through resilience and perseverance. (C) Fox Searchlight")))
    #print db
    #rows = db.query_all_dict("SELECT * FROM Movies")
    #print rows
    #return

if __name__ == "__main__":
    try:
        rebuild_db()
        print("Service started")
        app = pyrestful.rest.RestService([MovieResource])
        app.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print("\nService stopped")
