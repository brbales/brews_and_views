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

'''def index():
    if request.method == "POST":
        color = request.form['color']
        abv = request.form['abv']
        ibu = request.form['ibu']
        return render_template('index.html', color = color, abv = abv, ibu = ibu)
    else:
        return render_template('index.html')'''

@app.route('/style')
def style():

    result = db.session.query(Beer.style.distinct()).filter(Beer.style != None).order_by(Beer.style).all()

    b = np.ravel(result)
    results = b.tolist()
    return jsonify(results)

@app.route('/style_guesses')
def style_guesses():
    if request.method == "POST":
        color = request.form['color']
        abv = request.form['abv']
        ibu = request.form['ibu']
        return jsonified(color, abv, ibu)
    else:
        return render_template('index.html')

#setup a route to recommend beers (drives Action in forms), return a jsonified response
@app.route('/recommendations')
    if request.method == 'POST':
            # Then get the data from the form
            selected_beer = request.form['beer_search']


            selected_beer_cluster = db.session.query(Beer.clusters_7param, func.count(Beer.clusters_7param).label('amount')).\
            filter(Beer.Name == selected_beer).\
            group_by(Beer.clusters_7param).order_by(desc('amount')).all()[0][0]


            rec_beer_info = db.session.query(Beer.Name, Beer.Style, Beer.ABV, Beer.IBU, Beer.Color).\
            filter(Beer.clusters_7param == selected_beer_cluster, Beer.Name != selected_beer).\
            order_by(func.random()).\
            limit(5).all()

    

        return jsonify(rec_beer_info)

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
def rec_beers():

    predicted_cluster = #INSERT NAME FOR MODEL OUTPUT
    rec_beer_info = db.session.query(Beer.name, Beer.style,Beer.abv,Beer.ibu, Beer.color)\
    .filter(Beer.cluster_7param = predicted_cluster)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port = port, debug=True)
    #app.run(debug=True)