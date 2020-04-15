from flask import Flask, request, jsonify

from ArxivScrapper.ArxivScrapper import ArxivScraper, ARXIV_URL
from GoogleScholarScrapper.GoogleScholarScraper import GoogleScholarScrapper
from LancetScrapper.LancetScraper import LANCET_URL, LancetScraper
from MBIOSrapper.MbioScraper import MbioScraper, MBIO_URL
from utils.PaperJsonEncoder import PaperJsonEncoder
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": [
    'http://localhost:3000',
    'https://covida-fd704.web.app',
    'http://papers.covida.cl',
    'https://papers.covida.cl'
]}})
app.json_encoder = PaperJsonEncoder

lancetScraper = LancetScraper()
mbioScraper = MbioScraper()
arxivScraper = ArxivScraper()

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
    return jsonify(mbioScraper.getPapersOfInterestPaginatedSource(
        MBIO_URL,
        startIdx=0,
        endIdx=3,
        word_in_title=word_in_title,
        word_in_paper=word_in_paper)
    )

# google scholar

@app.route('/googlescholar/papersOfInterest')
def googleScholarOfInterest():
    word_in_paper = request.args.get('word_in_paper')
    return jsonify(GoogleScholarScrapper().getPapersFromGoogleScholar(
        3,
        word_in_paper))

# arxiv

@app.route('/arxiv/papersOfInterest')
def arxivPapersOfInterest():
    word_in_title = request.args.get('word_in_title')
    word_in_paper = request.args.get('word_in_paper')
    return jsonify(arxivScraper.getPapersOfInterest(
        ARXIV_URL,
        word_in_title,
        word_in_paper)
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
