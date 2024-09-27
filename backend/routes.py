from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Load the pictures data from a JSON file
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """Return the length of the data"""
    if data:
        return jsonify(length=len(data)), 200
    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return the list of picture URLs."""
    if data:
        return jsonify(data), 200  # Return the list of URLs in JSON format
    return jsonify({"message": "No pictures found."}), 404  # Handle case when there are no pictures

######################################################################
# GET A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return the picture URL with the given id."""
    if data:
        for picture in data:
            if picture.get("id") == id:
                return jsonify(picture), 200  # Return the picture with the matching id
        return jsonify({"message": "Picture not found."}), 404  # Return 404 if no matching id is found
    return jsonify({"message": "No pictures found."}), 404  # Handle case when there is no data

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture entry."""
    picture = request.get_json()  # Get the new picture data from the request body

    # Check if a picture with the given ID already exists
    for pic in data:
        if pic.get("id") == picture.get("id"):
            return jsonify({"message": f"Picture with id {picture['id']} already present"}), 302

    # Add the new picture to the data list
    data.append(picture)

    # Save the updated data back to the JSON file
    with open(json_url, 'w') as outfile:
        json.dump(data, outfile)

    return jsonify(picture), 201  # Return the created picture data with 201 status

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture."""
    updated_picture = request.get_json()  # Get the updated picture data from the request body

    for picture in data:
        if picture.get("id") == id:
            picture.update(updated_picture)

            # Save the updated data back to the JSON file
            with open(json_url, 'w') as outfile:
                json.dump(data, outfile)

            return jsonify(picture), 200  # Return the updated picture

    return jsonify({"message": "Picture not found"}), 404  # Return 404 if picture is not found

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by id."""
    global data
    for picture in data:
        if picture.get("id") == id:
            data.remove(picture)  # Remove the picture from the data list

            # Save the updated data back to the JSON file
            with open(json_url, 'w') as outfile:
                json.dump(data, outfile)

            return '', 204  # Return an empty body with 204 status code

    return jsonify({"message": "Picture not found"}), 404  # Return 404 if picture not found

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
