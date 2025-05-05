
from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/ai/upload')
def ai_upload():
    return render_template('ai/index.html')

@app.route('/ai/memory')
def ai_memory():
    return render_template('ai/memory.html')

if __name__ == '__main__':
    app.run(debug=True)
