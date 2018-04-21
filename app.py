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

# Create app
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

db = SQLAlchemy(app)

class Beer(db.Model):
    __tablename__ = 'data'

    id = db.Column(db.Integer, primary_key = True)

    name = db.Column(db.String(99))
    url = db.Column(db.String(299))
    style = db.Column(db.String(99))
    style_Id = db.Column(db.Integer())
    size_L = db.Column(db.Float())
    og = db.Column(db.Float())
    fg = db.Column(db.Float(20))
    abv = db.Column(db.Float(20))
    ibu = db.Column(db.Float(20))
    color = db.Column(db.Float(20))
    boil_size = db.Column(db.Float(20))
    boil_time = db.Column(db.Integer())
    boil_gravity = db.Column(db.Float(20))
    effeciency = db.Column(db.Float(20))
    mash_thickness = db.Column(db.Float(20))
    sugar_scale = db.Column(db.String(99))
    brew_method = db.Column(db.String(99))
    view_count = db.Column(db.Float(20))
    brew_count = db.Column(db.Float(20))
    last_upadted = db.Column(db.Float(20))


@app.route("/", methods = ['GET','POST'])
def index():
    if request.method == "POST":
        color = request.form['color']
        abv = request.form['abv']
        ibu = request.form['ibu']
        return render_template('index.html', color = color, abv = abv, ibu = ibu)
    else:
        return render_template('index.html')

@app.route('/style')
def style():

    result = db.session.query(Beer.style.distinct()).filter(Beer.style != None).order_by(Beer.style).all()

    b = np.ravel(result)
    results = b.tolist()
    return jsonify(results)

@app.route('/names')
def names():

    result = db.session.query(Beer.name.distinct()).filter(Beer.style != None).order_by(Beer.name).all()

    b = np.ravel(result)
    results = b.tolist()

    return jsonify(results)

#Form in index.html will have a post method, call the POST
def server():
if request.method == 'POST':
    # Then get the data from the form
    selected_beer = request.form['beer_input']

    selected_beer_cluster = db.session.query(Beer.cluster_7param).filter(Beer.name = selected_beer)

     #ETHAN pick up her - write a query to pull and display names and style, abv, ibu, and color for 5
     #random beers of the same cluster... starter code below
    rec_beer_info = db.session.query(Beer.name, Beer.style,Beer.abv,Beer.ibu, Beer.color)
    .filter(Beer.cluster_7param = selected_beer_cluster)

    return rec_beer_info


#CODE FOR AFTER THE MODEL RETURNS A CLUSTER
def rec_beers():

    predicted_cluster = #INSERT NAME FOR MODEL OUTPUT
    rec_beer_info = db.session.query(Beer.name, Beer.style,Beer.abv,Beer.ibu, Beer.color)
    .filter(Beer.cluster_7param = predicted_cluster)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port, debug=True)
    #app.run(debug=True)