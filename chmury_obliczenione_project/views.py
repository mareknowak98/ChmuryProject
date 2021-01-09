# -*- coding: utf-8 -*-
from urllib.parse import parse_qs, urlparse, urlunparse
from flask import Flask, request, session, redirect, url_for, render_template, flash
from .models import list_all_persons, list_all_locations, Person, Location
import json
import ast

def create_app():
  app = Flask(__name__)
  return app

app=create_app()

@app.route('/person/add', methods=['GET','POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        if not Person(name).add():
            flash('Osoba z tym imieniem istnieje w bazie!')
        else:
            return redirect(url_for('index'))
    return render_template('add_person.html')

@app.route('/location/add', methods=['GET','POST'])
def add_location():
    if request.method == 'POST':
        city = request.form['city']
        state = request.form['state']
        if not Location(city, state).add():
            flash('Miasto w tym województwie już istnieje!')
        else:
            return redirect(url_for('index'))
    return render_template('add_location.html')


@app.route('/person/delete', methods=['GET','POST'])
def delete_person():
    if request.method == 'POST':
        name = request.form['name']
        Person(name).delete()
        return redirect(url_for('index'))

    p = list_all_persons()
    return render_template('delete_person.html', persons = p)


@app.route('/location/delete', methods=['GET','POST'])
def delete_location():
    if request.method == 'POST':
        location = request.form['location']
        l = location.split(",")
        Location(l[0][2:-1], l[1][2:-2]).delete()
        return redirect(url_for('index'))

    loc = list_all_locations()
    return render_template('delete_location.html', locations = loc)


@app.route('/', methods=['GET','POST'])
def index():
    p = list_all_persons()
    l = list_all_locations()
    return render_template('index.html', persons=p, locations=l)



@app.route('/person/liveplace/add', methods=['GET','POST'])
def add_birthplace():
    if request.method == 'POST':
        location = request.form['location']
        l = location.split(",")
        name =  request.form['name']
        Person(name).add_birthplace(Location(l[0][2:-1], l[1][2:-2]))
        return redirect(url_for('index'))
    p = list_all_persons()
    l = list_all_locations()
    return render_template('add_residentcity.html', persons=p, locations=l)



@app.route('/friends/connect', methods=['GET','POST'])
def add_friend():
    if request.method == 'POST':
        person1 = request.form['person1']
        person2 = request.form['person2']
        Person(person1).add_friend(Person(person2))
        return redirect(url_for('index'))
    p1 = list_all_persons()
    p2 = list_all_persons()
    return render_template('add_friend.html', persons1 = p1, persons2 = p2)

@app.route('/distance/add', methods=['GET','POST'])
def add_distance():
    if request.method == 'POST':
        city1 = request.form['city1']
        city2 = request.form['city2']
        dist = request.form['dist']
        city_dict = city1.split(",")
        city_dict2 = city2.split(",")
        c1 = city_dict[0][10:-1]
        s1 = city_dict[1][11:-2]
        c2 = city_dict2[0][10:-1]
        s2 = city_dict2[1][11:-2]
        Location(c1, s1).add_dist(Location(c2, s2), dist)
        return redirect(url_for('index'))
    c1 = list_all_locations()
    c2 = list_all_locations()
    return render_template('add_distance.html', city1=c1, city2=c2)


@app.route('/search', methods=['GET','POST'])
def search_person():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('info_person') + "?name=" + name)
    
    p = list_all_persons()
    return render_template('search_person.html', persons = p)


@app.route('/person/info', methods=['GET','POST'])
def info_person():
    url = urlparse(request.url)
    name = parse_qs(url.query)['name'][0]
    person = Person(name)
    residentcity = person.get_birthplace()
    friends = person.get_friends()
    return render_template('info_person.html', name = name, residentcity = residentcity, friends = friends)


@app.route('/city/info', methods=['GET'])
def info_city():
    url = urlparse(request.url)
    city = parse_qs(url.query)['city'][0]
    state = parse_qs(url.query)['state'][0]
    location = Location(city, state)
    people_live_in = location.get_people_live_in(city)
    distances = location.get_dist()
    dist_dict = {}
    for elem in distances:
        temp1 = elem[1]
        temp2 = elem[0][0]['data']['dist']
        dist_dict[temp1] = temp2

    return render_template('info_city.html', city = location, people_live_in = people_live_in, distances=dist_dict)


# @app.route('/distance/get', methods=['GET','POST'])
# def get_distance():
#     url = urlparse(request.url)
#     city = parse_qs(url.query)['city'][0]
#     state = parse_qs(url.query)['state'][0]
#     location = Location(city, state)
#     distances = location.get_dist()
#     print(distances)
#     return render_template('info_city.html')