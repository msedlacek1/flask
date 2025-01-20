from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI", "mongodb+srv://ksadra:PWDj6ZCkw6J7X4mf@cluster0.olr53.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = MongoClient(mongo_uri)
db = client["npc"]  
collection_imgs = db["imgs"]  
collection_npcs = db["npcs"]

@app.route("/create_img", methods=["POST"])
def createImg():
    data = request.json
    result = collection_imgs.insert_one(data)
    return jsonify({"message": "Document created", "id": str(result.inserted_id)})

@app.route("/read_img/<id>", methods=["GET"])
def readImg(id):
    document = collection_imgs.find_one({"_id": ObjectId(id)})
    if document:
        document["_id"] = str(document["_id"])
        return jsonify(document)
    return jsonify({"error": "Document not found"}), 404

@app.route("/update_img/<id>", methods=["PUT"])
def updateImg(id):
    data = request.json
    result = collection_imgs.update_one({"_id": ObjectId(id)}, {"$set": data})
    if result.matched_count:
        return jsonify({"message": "Document updated"})
    return jsonify({"error": "Document not found"}), 404

@app.route("/delete_img/<name>", methods=["DELETE"])
def deleteImg(name):
    # Attempt to delete the document by its name
    result = collection_imgs.delete_one({"name": name})
    if result.deleted_count:
        return jsonify({"message": f"Img with name '{name}' deleted"})
    return jsonify({"error": f"Img with name '{name}' not found"}), 404

@app.route("/list_imgs", methods=["GET"])
def listImgs():
    documents = list(collection_imgs.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return jsonify(documents)
#////////////////////////////////////////////////////////////////////////////////////

@app.route("/create_npc", methods=["POST"])
def createNpc():
    data = request.json
    result = collection_npcs.insert_one(data)
    return jsonify({"message": "Document created", "id": str(result.inserted_id)})

@app.route("/read_npc/<id>", methods=["GET"])
def readNpc(id):
    document = collection_npcs.find_one({"_id": ObjectId(id)})
    if document:
        document["_id"] = str(document["_id"])
        return jsonify(document)
    return jsonify({"error": "Document not found"}), 404

@app.route("/update_npc/<name>", methods=["PUT"])
def updateNpc(name):
    data = request.json  # Get the JSON payload from the request
    result = collection_npcs.update_one({"name": name}, {"$set": data})  # Match by name instead of ID

    if result.matched_count:
        return jsonify({"message": "Document updated"})  # Document was updated successfully
    return jsonify({"error": "Document not found"}), 404

@app.route("/delete_npc/<name>", methods=["DELETE"])
def deleteNpc(name):
    # Attempt to delete the document by its name
    result = collection_npcs.delete_one({"name": name})
    if result.deleted_count:
        return jsonify({"message": f"NPC with name '{name}' deleted"})
    return jsonify({"error": f"NPC with name '{name}' not found"}), 404

@app.route("/list_npcs", methods=["GET"])
def listNpcs():
    documents = list(collection_npcs.find())
    for doc in documents:
        doc["_id"] = str(doc["_id"])
    return jsonify(documents)

if __name__ == "__main__":
    app.run(debug=True)
