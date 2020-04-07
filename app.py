from flask import Flask, request, jsonify

from LancetPageScrapper import getPapersFromLancet
from utils.PaperJsonEncoder import PaperJsonEncoder

app = Flask(__name__)
app.json_encoder = PaperJsonEncoder

@app.route('/allPapers')
def papers():
    return jsonify(getPapersFromLancet())

@app.route('/papersOfInterest')
def papersOfInterest():
    word_in_title = request.args.get('word_in_title')
    word_in_paper = request.args.get('word_in_paper')
    return 'Hello, World!'