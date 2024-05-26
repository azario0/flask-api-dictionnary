from flask import Flask, jsonify
import mysql.connector
import json

app = Flask(__name__)

db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'dictionaire',
}

def get_definition(mot):
    try:
        mot = mot.capitalize()
        
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = "SELECT definition FROM Mots WHERE mot = %s;"
        cursor.execute(query, (mot,))

        result = cursor.fetchone()
        
        if result:
            definitions_json = result[0]
            definitions = json.loads(definitions_json)  
            definitions = eval(definitions)
            return definitions
        else:
            return [f"Le mot '{mot}' n'a pas été trouvé dans la base de données."]

    except mysql.connector.Error as err:
        return f"Error: {err}"
    finally:
        
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/api/<mot>', methods=['GET'])
def definition(mot):
    definitions = get_definition(mot)
    if isinstance(definitions, list):
        data = {
            "mot": mot,
            "definition": [
                {"number": i + 1, "text": definition}
                for i, definition in enumerate(definitions)
            ]
        }
        return jsonify(data)
    else:
        return jsonify({"error": definitions}), 404

if __name__ == '__main__':
    app.run(debug=True)
