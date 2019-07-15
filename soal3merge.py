import numpy as np
import pandas as pd

datapokemon = pd.read_csv(
    'pokemon.csv',
    index_col = 0
)
datapokemon = datapokemon[['Name','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']]
datacombats = pd.read_csv('combats.csv')

id1 = []
id2 = []
hp1 = []
hp2 = []

attk1 = []
attk2 = []
def1 = []
def2 = []
spAtk1 = []
spAtk2 = []

spDef1 = []
spDef2 = []
spd1 = []
spd2 = []
winner = []

for i in range(len(datacombats)):
    pokemonid1 = datacombats.iloc[i]['First_pokemon']
    pokemonid2 = datacombats.iloc[i]['Second_pokemon']
    winners = datacombats.iloc[i]['Winner']
    id1.append(pokemonid1)
    id2.append(pokemonid2)

    hp1.append(datapokemon.loc[pokemonid1]['HP'])
    hp2.append(datapokemon.loc[pokemonid2]['HP'])
    
    attk1.append(datapokemon.loc[pokemonid1]['Attack'])
    attk2.append(datapokemon.loc[pokemonid2]['Attack'])

    def1.append(datapokemon.loc[pokemonid1]['Defense'])
    def2.append(datapokemon.loc[pokemonid2]['Defense'])

    spAtk1.append(datapokemon.loc[pokemonid1]['Sp. Atk'])
    spAtk2.append(datapokemon.loc[pokemonid2]['Sp. Atk'])

    spDef1.append(datapokemon.loc[pokemonid1]['Sp. Def'])
    spDef2.append(datapokemon.loc[pokemonid2]['Sp. Def'])

    spd1.append(datapokemon.loc[pokemonid1]['Speed'])
    spd2.append(datapokemon.loc[pokemonid2]['Speed'])
    
    if winners == pokemonid1:
        win = 0
        winner.append(win)
    else:
        win = 1
        winner.append(win)

df = pd.DataFrame(
    dict(
        pokemonid1 = id1, pokemonid2 = id2,
        hp1 = hp1, hp2 = hp2, attk1 = attk1,
        attk2 = attk2, def1 = def1, def2 = def2,
        spAtk1 = spAtk1, spAtk2 = spAtk2, spDef1 = spDef1,
        spDef2 = spDef2, spd1 = spd1, spd2 = spd2, winner = winner))
df.to_csv('mergedata.csv')
