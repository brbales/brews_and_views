import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc, inspect
from flask import (
    Flask, 
    render_template,
    jsonify,
    request,
    redirect)
import numpy as np
import try_something_new as tsn
import json

# Create app
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

db = SQLAlchemy(app)

class Beer(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key = True)

    Name = db.Column(db.String(99))
    Style = db.Column(db.String(99))
    StyleId = db.Column(db.Integer())
    OG = db.Column(db.Float())
    FG = db.Column(db.Float(20))
    ABV = db.Column(db.Float(20))
    IBU = db.Column(db.Float(20))
    Color = db.Column(db.Float(20))
    BoilSize = db.Column(db.Float(20))
    BoilTime = db.Column(db.Integer())
    Effeciency = db.Column(db.Float(20))
    ViewCount = db.Column(db.Float(20))
    BrewCount = db.Column(db.Float(20))
    LastUpdated = db.Column(db.Float(20))
    Category = db.Column(db.String(99))
    clusters_7param = db.Column(db.Integer())
    clusters_3param = db.Column(db.Integer())


@app.route("/", methods = ['GET','POST'])

def index():
    if request.method == "POST":
        abv = int(request.form['abv'])
        ibu = int(request.form['ibu'])
        color = int(request.form['color'])
        inputs = [abv, ibu, color]
        answer_dict = tsn.user_predict(inputs)
        names = []
        pcts = []
        

        for key, value in answer_dict.items():
            names.append(key)
            pcts.append("{0:.0f}%".format(value * 100))
        return render_template('index.html', topName = names[0], topPct = pcts[0], secondName = names[1], secondPct = pcts[1], thirdName = names[2], thirdPct = pcts[2])
        
        
    else:
        return render_template('index.html')

@app.route('/style')
def style():

    result = db.session.query(Beer.Style.distinct()).filter(Beer.Style != None).order_by(Beer.Style).all()

    b = np.ravel(result)
    results = b.tolist()
    return jsonify(results)

@app.route('/style_guesses')
def style_guesses():
    if request.method == "POST":
        color = request.form['color']
        abv = request.form['abv']
        ibu = request.form['ibu']
        return jsonify(color, abv, ibu)
    else:
        return render_template('index.html')

#setup a route to recommend beers (drives Action in forms), return a jsonified response
@app.route('/recommendations/<beer>')
def reco(beer):
    # Then get the data from the form
    #selected_beer = request.form['beer_search']
    selected_beer_cluster = db.session.query(Beer.clusters_7param, func.count(Beer.clusters_7param).label('amount')).\
    filter(Beer.Name == beer).\
    group_by(Beer.clusters_7param).order_by(desc('amount')).all()[0][0]

    rec_beer_info = db.session.query(Beer.Name, Beer.Style, Beer.ABV, Beer.IBU, Beer.Color).\
    filter(Beer.clusters_7param == selected_beer_cluster, Beer.Name != beer).\
    order_by(func.random()).\
    limit(5).all()

    return jsonify(rec_beer_info)

@app.route('/beers/<beer_style>')
def beers_list(beer_style):
    # Then get the data from the form
    #selected_beer = request.form['beer_search']
    
    list_beers = db.session.query(Beer.Name).filter(Beer.Style == beer_style).order_by(Beer.Name).all()
    b = np.ravel(list_beers)
    results = b.tolist()

    return jsonify(results)

#after we get the json response right (server is acting right).
#then use ajax to send the 
#prevent default to stop it from updating the page until it's all working... then work on getting the HTML object right


#setup a route to classify beers

@app.route('/names')
def names():

    result = db.session.query(Beer.name.distinct()).filter(Beer.style != None).order_by(Beer.name).all()

    b = np.ravel(result)
    results = b.tolist()

    return jsonify(results)



#CODE FOR AFTER THE MODEL RETURNS A CLUSTER

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port, debug=True)
    #app.run(debug=True)