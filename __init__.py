from flask import Flask, render_template_string, render_template, jsonify, requests
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)    

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

#@app.route("/commits/")
#def commits():
    #return render_template("https://api.github.com/repos/najjahi/5MCSI_Metriques/commits") 


@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minutes = date_object.minute
        return jsonify({'minutes': minutes})
  

@app.route("/commits/")
def commits():
    url = "https://api.github.com/repos/najjahi/5MCSI_Metriques/commits"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs HTTP
        commits_data = response.json()  # Récupère les données JSON
        commits_count = len(commits_data)  # Compte le nombre de commits
        return render_template("commits.html", commits=commits_data, count=commits_count)
    except requests.exceptions.RequestException as e:
        return f"Une erreur s'est produite : {e}", 500


if __name__ == "__main__":
  app.run(debug=True)
