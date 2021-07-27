from flask import render_template, request, jsonify, redirect
from app import app
# from app import database as db_helper
from app import db

@app.route('/search',methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        state = request.form['state']
        date = request.form['date']
        conn = db.connect()
        query = "SELECT * from State where state=\"{}\" and date=\"{}\";".format(state,date)
        results = conn.execute(query)
        return render_template('index.html',data=results)
    else:
        return redirect('/')
    
# @app.route("/delete/<int:fips>",methods = ['POST'])
# def delete(fips):




#  @app.route("/delete/<int:task_id>", methods=['POST'])
#  def delete(task_id):
#      try:
#      db_helper.remove_task_by_id(task_id)
#          result = {'success': True, 'response': 'Removed task'}
#      except:
#          result = {'success': False, 'response': 'Something went wrong'}
#      return jsonify(result)

# @app.route("/edit/<int:task_id>", methods=['POST'])
# def update(task_id):
#     data = request.get_json()
#     print(data)
#     try:
#         if "status" in data:
#     # db_helper.update_status_entry(task_id, data["status"])
#             result = {'success': True, 'response': 'Status Updated'}
#         elif "description" in data:
#     # db_helper.update_task_entry(task_id, data["description"])
#             result = {'success': True, 'response': 'Task Updated'}
#         else:
#             result = {'success': True, 'response': 'Nothing Updated'}
#     except:
#         result = {'success': False, 'response': 'Something went wrong'}
#     return jsonify(result)

# @app.route("/create", methods=['POST'])
# def create():
#     data = request.get_json()
#     # db_helper.insert_new_task(data['description'])
#     result = {'success': True, 'response': 'Done'}
#     return jsonify(result)


@app.route("/")
def homepage():
    return render_template("index.html")