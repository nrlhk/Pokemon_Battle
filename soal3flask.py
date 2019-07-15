from flask import Flask, redirect, request, render_template, url_for, send_from_directory, abort
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json, requests
import joblib
import os, random

app = Flask(__name__)
app.config['upload_folder']='storage'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hasil', methods=['POST','GET'])
def post():
    pokemon1 = request.form['pokemon1']
    pokemon2 = request.form['pokemon2']
    pokemon1 = pokemon1.lower()
    pokemon2 = pokemon2.lower()

    urlpokemon1 = 'https://pokeapi.co/api/v2/pokemon/'+pokemon1
    urlpokemon2 = 'https://pokeapi.co/api/v2/pokemon/'+pokemon2

    getpokemon1 = requests.get(urlpokemon1)
    getpokemon2 = requests.get(urlpokemon2)
    
    if str(getpokemon1) == '<Response [404]>' or str(getpokemon2) == '<Response [404]>':
        return redirect('/NotFound')

    datapokemon = pd.read_csv('pokemon.csv')
    idpokemon1 = (datapokemon[datapokemon['Name'] == pokemon1.title()].index.values[0])+1
    idpokemon2 = (datapokemon[datapokemon['Name'] == pokemon2.title()].index.values[0])+1
   
    gambar1 = getpokemon1.json()['sprites']['front_default']
    gambar2 = getpokemon2.json()['sprites']['front_default']

    dfpokemon = pd.read_csv('pokemon.csv', index_col=0)

    hp1 = dfpokemon.loc[idpokemon1]['HP']
    hp2 = dfpokemon.loc[idpokemon2]['HP']
    attack1 = dfpokemon.loc[idpokemon1]['Attack']
    attack2 = dfpokemon.loc[idpokemon2]['Attack']
    defense1 = dfpokemon.loc[idpokemon1]['Defense']
    defense2 = dfpokemon.loc[idpokemon2]['Defense']
    spatk1 = dfpokemon.loc[idpokemon1]['Sp. Atk']
    spatk2 = dfpokemon.loc[idpokemon2]['Sp. Atk']
    spdef1 = dfpokemon.loc[idpokemon1]['Sp. Def']
    spdef2 = dfpokemon.loc[idpokemon2]['Sp. Def']
    speed1 = dfpokemon.loc[idpokemon1]['Speed']
    speed2 = dfpokemon.loc[idpokemon2]['Speed']

    predict = model1.predict(
        [[hp1, hp2, attack1, attack2, defense1, defense2,
        spatk1, spatk2, spdef1, spdef2, speed1, speed2]])[0]
    if predict == 0:
        winner = pokemon1.title()
    else:
        winner = pokemon2.title()

    proba = model1.predict_proba(
        [[hp1, hp2, attack1, attack2, defense1, defense2,
        spatk1, spatk2, spdef1, spdef2, speed1, speed2]])
    probamax = round(proba[0, predict] * 100)

    # ---- for plotting
    plt.close()
    plt.figure(figsize =(15,8))
    plt.subplot(161)
    plt.title('HP')
    plt.bar(pokemon1, hp1, width = 1)
    plt.bar(pokemon2, hp2, width = 1, color= 'green')

    plt.subplot(162)
    plt.title('Attack')
    plt.bar(pokemon1, attack1, width = 1)
    plt.bar(pokemon2, attack2, width = 1)

    plt.subplot(163)
    plt.title('Defense')
    plt.bar(pokemon1, defense1, width = 1)
    plt.bar(pokemon2, defense2, width = 1)

    plt.subplot(164)
    plt.title('Special Attack')
    plt.bar(pokemon1, spatk1, width = 1)
    plt.bar(pokemon2, spatk2, width = 1)

    plt.subplot(165)
    plt.title('Special Defense')
    plt.bar(pokemon1, spdef1, width = 1)
    plt.bar(pokemon2, spdef2, width = 1)

    plt.subplot(166)
    plt.title('Speed')
    plt.bar(pokemon1, speed1, width= 1)
    plt.bar(pokemon2, speed2, width= 1)

    address = './storage/' + pokemon1 + 'vs' + pokemon2 +'.png'
    urlgraph ='http://localhost:5000/graph/'+ pokemon1 +'vs'+ pokemon2 +'.png'
    plt.savefig(address)
    graph = urlgraph

    plt.close()
    return render_template(
    'hasil.html', nama1 = pokemon1.title(), nama2 = pokemon2.title(),
    gambar1 = gambar1, gambar2 = gambar2, winner = winner,
    proba = probamax, graph = graph
    )

@app.route('/graph/<path:x>')
def graph(x):
    return send_from_directory('storage', x)

@app.route('/NotFound')
def notFound():
    return render_template('error.html')

@app.errorhandler(404)
def notFound404(error):
    return render_template('error.html')

if __name__=='__main__':
    model1 = joblib.load('modelpokemon')
    app.run(debug=True)