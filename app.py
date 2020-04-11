from flask import Flask, request, jsonify

from LancetScrapper.LancetScraper import LANCET_URL, LancetScraper
from MBIOSrapper.MbioScraper import MbioScraper, MBIO_URL
from utils.PaperJsonEncoder import PaperJsonEncoder

app = Flask(__name__)
app.json_encoder = PaperJsonEncoder
lancetScraper = LancetScraper()
mbioScraper = MbioScraper()

# lancet routes

@app.route('/lancet/allPapers')
def papers():
    return jsonify(lancetScraper.getPapersFromUrl(LANCET_URL))

@app.route('/lancet/papersOfInterest')
def lancetPapersOfInterest():
    word_in_title = request.args.get('word_in_title')
    word_in_paper = request.args.get('word_in_paper')
    return jsonify(lancetScraper.getPapersOfInterest(
        LANCET_URL,
        word_in_title,
        word_in_paper)
    )

@app.route('/lancet/openLinksOfInterest')
def openLinksOfInterest():
    word_in_title = request.args.get('word_in_title')
    word_in_paper = request.args.get('word_in_paper')
    lancetScraper.scrappingAndOpenLinks(LANCET_URL, word_in_title, word_in_paper)
    return jsonify({'message': 'this can take some time'})

# mbio routes

@app.route('/mbio/papersOfInterest')
def mbioPapersOfInterest():
    word_in_title = request.args.get('word_in_title')
    word_in_paper = request.args.get('word_in_paper')
    return jsonify(mbioScraper.getPapersOfInterest(
        MBIO_URL,
        word_in_title,
        word_in_paper)
    )
