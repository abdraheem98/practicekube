from flask import Flask, request, jsonify
from azure.cosmos import CosmosClient

app = Flask(__name__)

# Cosmos DB connection details
#url = ""
#key = ""
client = CosmosClient(url, credential=key)

#database = client.get_database_client("ECommerceDB")
#container = database.get_container_client("Products")

@app.route('/products', methods=['GET'])
def get_products():
    category = request.args.get('category')
    if not category:
        return jsonify({"error": "Category is required"}), 400

    query = f"SELECT * FROM Products p WHERE p.category = '{category}'"
    items = list(container.query_items(query=query, enable_cross_partition_query=True))
    return jsonify(items)


@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    container.upsert_item(data)
    return jsonify({"message": "Product added successfully!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
