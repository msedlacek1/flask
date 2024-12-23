from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://ksadra:PWDj6ZCkw6J7X4mf@cluster0.olr53.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(mongo_uri)
db = client["npc"]  
collection = db["imgs"]  

@app.route("/create", methods=["POST"])
def create():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({"message": "Document created", "id": str(result.inserted_id)})

@app.route("/read/<id>", methods=["GET"])
def read(id):
    document = collection.find_one({"_id": ObjectId(id)})
    if document:
        document["_id"] = str(document["_id"])
        return jsonify(document)
    return jsonify({"error": "Document not found"}), 404

@app.route("/update/<id>", methods=["PUT"])
def update(id):
    data = request.json
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Document updated"})
    return jsonify({"error": "Document not found"}), 404

@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count:
        return jsonify({"message": "Document deleted"})
    return jsonify({"error": "Document not found"}), 404

@app.route("/list", methods=["GET"])
def list_documents():
    documents = list(collection.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return jsonify(documents)

if __name__ == "__main__":
    app.run(debug=True)