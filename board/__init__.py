from flask import Flask, jsonify, request 
from board.build_data import compile_data, save_ingredient_set
from board.create_pdf import create__shopping_list_pdf, create_pdf

app = Flask(__name__)

@app.route("/scraper", methods=['GET'])
def scraper():
    url = request.args.get('q')
    recipe_id = request.args.get('id')
    compile_data(url,recipe_id)
    response = jsonify({'recipe': recipe_id})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/send_email", methods=['GET'])
def send_email():# create a recipe PDF from the arguments and send it as an email
    recipe_id = request.args.get('q')
    create_pdf(recipe_id)
    response = jsonify({'recipe': "test"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/send_shopping_email", methods=['GET'])
def send_shopping_email():# create a shopping list
    create__shopping_list_pdf()
    response = jsonify({'recipe': "test"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/save_ingredients", methods=['POST'])
def save_ingredients():
    recipe_id = request.args.get('recipe_id')
    list_references = request.args.get('list_references')
    ingredients_data = request.args.get('ingredients_data')
    save_ingredient_set(recipe_id,list_references,ingredients_data)
    response = jsonify({'recipe': "test"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)