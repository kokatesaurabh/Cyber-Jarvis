from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    response = {"message": f"Received query: {data['query']}"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
