""" Specifies routing for the application"""
from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/delete/<string:State_FIPS>", methods=['POST'])
def delete(State_FIPS):
    """ recieved post requests for entry delete """

    try:
        db_helper.remove_state_by_fips(State_FIPS)
        result = {'success': True, 'response': 'Removed state'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/edit/<string:State_FIPS>", methods=['POST'])
def update(State_FIPS):
    """ recieved post requests for entry updates """

    data = request.get_json()

    try:
        # if "State_Name" in data:
        #     db_helper.update_statename_entry(State_FIPS, data["State_Name"])
        #     result = {'success': True, 'response': 'State Name Updated'}
        if "Safety_Index" in data:
            db_helper.update_safetyindex_entry(State_FIPS, data["Safety_Index"])
            result = {'success': True, 'response': 'Safety Index Updated'}
        else:
            result = {'success': True, 'response': 'Nothing Updated'}
    except:
        result = {'success': False, 'response': 'Something went wrong'}

    return jsonify(result)


@app.route("/create", methods=['POST'])
def create():
    """ recieves post requests to add new state """
    data = request.get_json()
    db_helper.insert_new_state(data["State_Name"])
    result = {'success': True, 'response': 'Done'}
    return jsonify(result)


@app.route("/")
def homepage():
    """ returns rendered homepage """
    items = db_helper.fetch_StateSafetyIndex()
    return render_template("index.html", items=items)