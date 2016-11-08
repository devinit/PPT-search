from flask import Flask
from flask import render_template, request, flash
from mainFunction import clean_variables, translations, clean_variables2, translations2
from flask_cors import CORS
from flask import jsonify

app = Flask(__name__)
CORS(app)
app.secret_key = 'some_secret'

@app.route('/')
def index():
    return "PPT search API app running"

@app.route('/translator', methods=['POST'])
def input_dropdown():
    if request.method == 'POST':
        code = request.form['code']
        term = request.form['term']
        term = term.lower()
        code = code.upper()
        if term == '' and code == '':
            flash('Please input your search term or code')
            return render_template("translator2.html")
        if term != '':
            source = request.form['source']
            match = request.form['match']
            starting_classification = request.form['start']
            destination_classification = request.form['destination']
            results_in_list, DownloadUrl = clean_variables(source, match, term)
            translation = translations(
                results_in_list,
                source,
                starting_classification,
                destination_classification,
            )
            number_of_results = len(results_in_list)
            number_of_translations = len(translation)
            links = []
            for i in results_in_list:
                a = i.split(':')
                uri = a[1] + ':' + a[2]
                links.append(uri)
        if code != '':
            source = request.form['source']
            match = request.form['match']
            starting_classification = request.form['start']
            destination_classification = request.form['destination']
            if source == 'er':
                flash('You forgot to choose your starting data standard!')
                return render_template("translator2.html")
            results_in_list, DownloadUrl = clean_variables2(
                source, match, code)
            translation = translations2(
                results_in_list,
                source,
                starting_classification,
                destination_classification)
            number_of_results = len(results_in_list)
            number_of_translations = len(translation)
            links = []
            for i in results_in_list:
                a = i.split(':')
                if (a[0] == 'Original code' or a[0] == 'Translated code'):
                    links.append('')
                else:
                    uri = a[1] + ':' + a[2]
                    links.append(uri)

    return jsonify(
        no=number_of_results,
        no2=number_of_translations,
        trans=translation,
        DownloadXML=DownloadUrl,
        Links_and_Matches=zip(
            links,
            results_in_list),
        scroll='results')

if __name__ == "__main__":
    app.run(debug=True)
