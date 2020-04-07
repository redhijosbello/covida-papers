from flask import Flask, request, jsonify

from LancetPageScrapper import getPapersFromLancet, getLancetPapersOfInterest, lancetScrappingAndOpenLinks
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
    return jsonify(getLancetPapersOfInterest(word_in_title, word_in_paper))

@app.route('/openLinksOfInterest')
def openLinksOfInterest():
    word_in_title = request.args.get('word_in_title')
    word_in_paper = request.args.get('word_in_paper')
    lancetScrappingAndOpenLinks(word_in_title, word_in_paper)
    return jsonify({'message': 'this can take some time'})
