from flask import Flask, jsonify, request
from flask_cors import CORS
from query_handler import execute_query

app = Flask(__name__)
CORS(app)


@app.route("/district_population", methods=["GET"])
def district_population():
    wikidata_id = request.args.get("wikidataId", type=str)
    if not wikidata_id:
        return jsonify({"error": "Missing wikidataId parameter"}), 400
    try:
        # Call the function from the query_handler module
        result = execute_query(wikidata_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
