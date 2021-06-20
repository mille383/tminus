from flask.helpers import make_response
from app import app, db
from flask import render_template, request, redirect, url_for, flash, json, jsonify, make_response
from app.models import Comment
import requests as r
import traceback
import pandas as pd
import numpy as np
from datetime import datetime as dt
import random
import plotly
import plotly.express as px

# set this to 'dev' to avoid the api call limit
dev = ''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        provider = request.form['provider']

        upcoming = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/launch/upcoming/?rocket__configuration__manufacturer__name__icontains={provider}').json()
        # data = r.get(f'https://lldev.thespacedevs.com/2.2.0/launch/previous/?rocket__configuration__full_name__icontains={program}&is_crewed=true&include_suborbital=true&related=false').json()
        upcoming = upcoming['results']
        context = {
            "upcoming": upcoming
        }
        return render_template('index.html', **context)
    return render_template('index.html')

@app.route('/<id>', methods=['GET', 'POST'])
def upcomingid(id):

    single = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/launch/upcoming/{id}').json() # search by a certain id
    
    context = {
        "single": single
    }
    return render_template('index.html', **context)
    # return render_template('historical.html')

@app.route('/historical', methods=['GET', 'POST'])
def historical():
    if request.method == 'POST':
        program = request.form['program_select']
        
        # data = r.get(f'https://lldev.thespacedevs.com/2.2.0/launch/previous/?rocket__configuration__full_name__icontains={program}&is_crewed=true&include_suborbital=true&related=false').json()
        # launches = r.get('https://ll.thespacedevs.com/2.0.0/launch/previous/?limit=100 view previous with a set limit

        # 1 is Starship
        # 2 is Mercury
        # 3 is ? should be Gemini
        # 4 is Apollo
        # 5 is falcon 9 ... crewed?
        # 6 is 
        # 7 is ?
        # 8 is Soyuz
        # 9 is 
        # 10 is Voskhod
        # 11 is CRS?
        # 12 shuttle?
        launches = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/launch/previous/?program={program}').json() # search by a certain program
        # launches = [r['name'] for r in data['results']]
        launches = launches['results']
        # launchers = pd.DataFrame(launchers, columns=['Launcher'])
        context = {
            "launches": launches
        }
        return render_template('historical.html', **context)
    return render_template('historical.html')

@app.route('/historical/<id>', methods=['GET', 'POST'])
def historicalid(id):
    # if request.method == 'POST':
        # program = request.form['program']
        
        # data = r.get(f'https://lldev.thespacedevs.com/2.2.0/launch/previous/?rocket__configuration__full_name__icontains={program}&is_crewed=true&include_suborbital=true&related=false').json()
        # launches = r.get('https://ll.thespacedevs.com/2.0.0/launch/previous/?limit=100 view previous with a set limit

    single = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/launch/{id}').json() # search by a certain program
    try:
        # single['rocket']['spacecraft_stage']['launch_crew']
        astronauts = [i for i in single['rocket']['spacecraft_stage']['launch_crew']]
    except: astronauts = None
    # launches = [r['name'] for r in data['results']]
    # single = single['results']
    # launchers = pd.DataFrame(launchers, columns=['Launcher'])
    context = {
        "single": single,
        "astronauts": astronauts
    }
    return render_template('historical.html', **context)
    # return render_template('historical.html')

@app.route('/astronauts', methods=['GET', 'POST'])
def astronauts():
    if request.method == 'POST':
        aname = request.form['astronaut']

        single = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/astronaut/?search={aname}').json()
        # data = r.get(f'https://lldev.thespacedevs.com/2.2.0/launch/previous/?rocket__configuration__full_name__icontains={program}&is_crewed=true&include_suborbital=true&related=false').json()
        id = single['results'][0]['id']
        flight = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/astronaut/{id}').json()
        single = single['results'][0]
        flights = flight['flights']
        context = {
            "single": single,
            "flights": flights
        }
        return render_template('astronauts.html', **context)
    return render_template('astronauts.html')

@app.route('/pads', methods=['GET', 'POST'])
def pads():
    
    pads_initial = r.get(f'https://ll{dev}.thespacedevs.com/2.2.0/pad/?limit=100').json()
    pads = []
    for i in pads_initial['results']:
        data_dict = {
            'name': i['name'],
            'latitude': i['latitude'],
            'longitude': i['longitude'],
            'location': i['location']['name'],
            'launch_count': i['total_launch_count']
        }
        pads.append(data_dict)
    return render_template('pads.html', pads = pads)

@app.route('/astronauts/<id>', methods=['GET', 'POST'])
def astronautid(id):
    
    single = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/astronaut/{id}').json() # search by a certain program
    flights = single['flights']
    context = {
        "single": single,
        "flights": flights
    }
    return render_template('astronauts.html', **context)
    # return render_template('historical.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        comment = request.form['comments']

        new_comment = Comment(
            name = name,
            email = email,
            feedback = comment,
            created = dt.now()
        )
        db.session.add(new_comment)
        db.session.commit()
        return render_template('feedbackrcvd.html', data = name)
    return render_template('contactme.html')

@app.route('/visuals', methods=['GET', 'POST'])
def visuals():
    # data = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/launch/previous/?limit=100').json() # view previous with a set limit
    # launchers = [r['launch_service_provider']['name'] for r in data['results']]
    # dflaunch = pd.DataFrame(launchers, columns=['Launcher'])
    # fig = px.histogram(dflaunch, x='Launcher', template = 'plotly_dark').update_xaxes(categoryorder="total descending")
    # fig.update_layout(
    #     yaxis_title_text = 'Launch Count',
    #     xaxis_title_text = 'Company / Entity'
    # )
    # graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # return render_template('visualizations.html', graphJSON=graphJSON)

    data = r.get(f'https://ll{dev}.thespacedevs.com/2.0.0/launch/previous/?limit=100').json() # view previous with a set limit
    l = []
    for i in data['results']:
        line = {
            'launcher': i['launch_service_provider']['name'],
            'date': i['net'][:10]
        }
        l.append(line)
    dflaunch = pd.DataFrame(l)
    fig = px.histogram(dflaunch, x='launcher', template = 'plotly_dark').update_xaxes(categoryorder="total descending")
    spacex = dflaunch[dflaunch['launcher'] == 'SpaceX']
    figline = px.line(spacex, x='date', y='launcher')
    fig.update_layout(
        title_text = 'Previous 100 Launches', title_x = 0.5,
        yaxis_title_text = 'Launch Count',
        xaxis_title_text = 'Company / Entity'
    )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSONline = json.dumps(figline, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('visualizations.html', graphJSON=graphJSON, graphJSONline = graphJSONline)
