from flask import Flask, request, jsonify
from text_blind_watermark import TextBlindWatermark

app = Flask(__name__)
PASSWORD = b"p@ssw0rd"

@app.route('/embed', methods=['POST'])
def embed():
    data = request.json
    text = data.get('text', '')
    watermark = data.get('watermark', '').encode()
    twm = TextBlindWatermark(pwd=PASSWORD)
    result = twm.add_wm_rnd(text=text, wm=watermark)
    return jsonify({'text_with_watermark': result})

@app.route('/extract', methods=['POST'])
def extract():
    data = request.json
    text_with_wm = data.get('text_with_watermark', '')
    twm = TextBlindWatermark(pwd=PASSWORD)
    result = twm.extract(text_with_wm)
    return jsonify({'extracted_watermark': result.decode()})

if __name__ == '__main__':
    app.run()
