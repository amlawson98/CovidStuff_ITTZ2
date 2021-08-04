from flask import render_template, request, jsonify, redirect
from app import app
# from app import database as db_helper
from app import db

@app.route('/search',methods = ['GET','POST'])
def keyword_search():
    if request.method == 'POST':
        state = request.form['state']
        date = request.form['date']
        conn = db.connect()
        query = "SELECT * from State where state=\"{}\" and date=\"{}\";".format(state,date)
        results = conn.execute(query)
        return render_template('index.html',data=results)
    else:
        return redirect('/')

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

# Test case: Deleted from database: covid19 table: State row: illinois 2020-01-31
# Once the add function is written, we should re-insert this row of data
# date="2020-01-31" state="illinois" fips=17 cases=2 deaths=0
@app.route("/delete",methods = ['GET','POST'])
def delete():
    if request.method == 'POST':
        state = request.form['state']
        date = request.form['date']
        conn = db.connect()
        query = "DELETE from State where state=\"{}\" and date=\"{}\";".format(state,date)
        results = conn.execute(query)
        return render_template("index.html",date=results)
    else:
        return redirect('/')

@app.route('/update_case',methods=['GET','POST'])
def update_case():
    if request.method == 'POST':
        state = request.form['state']
        date = request.form['date']
        case = request.form['case']
        case = int(case)
        conn = db.connect()
        query = "UPDATE State SET cases={} where state=\"{}\" and date=\"{}\";".format(case,state,date)
        results = conn.execute(query)
        return render_template("index.html",date=results)
    else:
        return redirect('/')

@app.route('/update_death',methods=['GET','POST'])
def update_death():
    if request.method == 'POST':
        state = request.form['state']
        date = request.form['date']
        death = request.form['death']
        death = int(death)
        conn = db.connect()
        query = "UPDATE State SET deaths={} where state=\"{}\" and date=\"{}\";".format(death,state,date)
        results = conn.execute(query)
        return render_template("index.html",date=results)
    else:
        return redirect('/')


"""
CREATE TRIGGER InsertBeforeUpdate
  BEFORE UPDATE ON State
   IF NOT EXISTS (SELECT * FROM STATE WHERE state=new.state AND date=new.date) THEN
        INSERT INTO STATE State(date, state, fips, cases, deaths)
        VALUES (new.date, new.state, new.fips, new.cases, new.deaths);
   END IF;
  END;"""

@app.route('/group_by', methods=['GET','POST'])
def group_by():
    if request.method == 'POST':
        date = request.form['date']
        conn = db.connect()
        query = "SELECT date, avg(cases) from State group by date having date = \"{}\";".format(date)
        results = conn.execute(query)
        return render_template("index.html",data2=results)
    else:
        return redirect('/')

@app.route('/max_county',methods=['GET','POST'])
def max_county():
    if request.method == 'POST':
        date = request.form['date']
        state = request.form['state']
        conn = db.connect()
        query = "select County.county, County.state, County.cases from (select date,state, avg(cases) as avg_cases from County group by date, state) as temp, County where temp.date = County.date and temp.state=County.state and County.cases >= temp.avg_cases and temp.date=\"{}\" and temp.state=\"{}\" order by County.state, County.cases desc, County.county;".format(date,state)
        results = conn.execute(query)
        return render_template("index.html",data3=results)
    else:
        return redirect('/')



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