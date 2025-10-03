from flask import Flask, render_template, request, jsonify
from text_blind_watermark import TextBlindWatermark

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # 主页面，包含嵌入/提取面板

@app.route('/embed', methods=['POST'])
def embed_watermark():
    data = request.json
    pwd = data.get('password', '')
    wm = data.get('watermark', '')
    text = data.get('input_text', '')
    if not pwd or not text:
        return jsonify({'error': '密码或文本不能为空！'})
    try:
        twm = TextBlindWatermark(pwd=pwd.encode())
        text_with_wm = twm.add_wm_rnd(text=text, wm=wm.encode())
        return jsonify({'success': True, 'output_text': text_with_wm})
    except Exception as e:
        return jsonify({'error': f'嵌入失败: {str(e)}'})

@app.route('/extract', methods=['POST'])
def extract_watermark():
    data = request.json
    pwd = data.get('password', '')
    text_with_wm = data.get('input_text', '')
    if not pwd or not text_with_wm:
        return jsonify({'error': '密码或水印文本不能为空！'})
    try:
        twm = TextBlindWatermark(pwd=pwd.encode())
        extracted = twm.extract(text_with_wm)
        return jsonify({'success': True, 'output_text': extracted.decode()})
    except Exception as e:
        return jsonify({'error': f'提取失败: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)