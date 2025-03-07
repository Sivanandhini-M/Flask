
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/count_words', methods=['POST'])
def count_words():
    file = request.files.get('file')
    words = json.loads(request.form.get('words'))
    
    if not words or not file:
        return jsonify({"error": "Missing words or file input"}), 400
    
    file_content = file.read().decode('utf-8')
    word_counts = {word: file_content.lower().split().count(word.lower()) for word in words}
    
    return jsonify(word_counts)

if __name__ == '__main__':
    app.run(debug=True)
