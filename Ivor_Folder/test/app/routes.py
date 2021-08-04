from flask import render_template, request, jsonify, redirect
from sqlalchemy.exc import StatementError
from app import app
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib.backends.backend_agg import FigureCanvasAgg as Canvas
from matplotlib.figure import Figure
import pandas as pd
import mpld3 as mpld3
import io
import base64
import datetime
# from app import database as db_helper
from app import db

@app.route('/wear_mask',methods = ['GET','POST'])
def wear_mask():
    if request.method == 'POST':
        user_input = request.form['state'].lower()
        query = "select distinct County.county as county_name, Mask.never+Mask.rarely as noMask, temp.final_death_count from County, Mask, (select fips, max(deaths) as final_death_count from County group by fips) as temp where County.state = \"{}\" and Mask.countyfips = County.fips and County.fips = temp.fips;".format(user_input)
        conn = db.connect()
        results = conn.execute(query).fetchall()
        mask, death = [item[1] for item in results], [item[2] for item in results]
        ind = []
        for i in range(len(mask)):
            if mask[i] > 0.3:
                ind.append(i)
        count = 0
        for j in ind:
            mask.pop(j-count)
            death.pop(j-count)
            count += 1
        query1,query2,query3,query4,query5,query6 = 'set @name = \"{}\";'.format(user_input),'call DeathRate(@name,@death_corr,@vac_corr, @case_corr,@mask_vac);','select @death_corr;', 'select @vac_corr;', 'select @case_corr;','select @mask_vac;'
        conn.execute(query1)
        conn.execute(query2)
        corr_death = conn.execute(query3).fetchall()
        corr_vac = conn.execute(query4).fetchall()
        corr_case = conn.execute(query5).fetchall()
        corr_mask_vac = conn.execute(query6).fetchall()
        query = "select distinct County.county as county_name, Mask.never+Mask.rarely as noMask, temp.final_death_count from County, Mask, (select fips, max(cases) as final_death_count from County group by fips) as temp where County.state = \"{}\" and Mask.countyfips = County.fips and County.fips = temp.fips;".format(user_input)
        conn = db.connect()
        results = conn.execute(query).fetchall()
        mask, case = [item[1] for item in results], [item[2] for item in results]
        ind = []
        for i in range(len(mask)):
            if mask[i] > 0.3:
                ind.append(i)
        count = 0
        for j in ind:
            mask.pop(j-count)
            case.pop(j-count)
            count += 1
        query = "select distinct State.state as state_, Vac.dose as dose, Mask_State.outcome as withMask from (select County.state as state, avg(Mask.frequently)+avg(Mask.always) as outcome from Mask, County where Mask.countyfips = County.fips group by County.state) as Mask_State, (select State_FIPS, max(Doses_Administrated) as dose from Vaccine group by State_FIPS) as Vac, State where State.fips = Vac.State_FIPS and State.state = Mask_State.state;"
        results = conn.execute(query).fetchall()
        vac, with_mask = [item[1] for item in results],[item[2] for item in results]
        with plt.style.context('ggplot'):
                fig,ax = plt.subplots(3,1,figsize=(5,20))
                fig.autofmt_xdate()
                ax[0].scatter(mask,death)
                ax[0].set_xlabel('Percentage of Non-Mask Wearer')
                ax[0].set_ylabel('Death')
                ax[0].set_title('Correlation: {}'.format(corr_death[0][0]))
                ax[1].scatter(mask,case)
                ax[1].set_xlabel('Percentage of Non-Mask Wearer')
                ax[1].set_ylabel('Case')
                ax[1].set_title('Correlation: {}'.format(corr_case[0][0]))
                ax[2].scatter(with_mask, vac)
                ax[2].set_xlabel('Percentage of Mask Wearer')
                ax[2].set_ylabel('Vaccination Count')
                ax[2].set_title('Correlation: {} Across US'.format(corr_mask_vac[0][0]))
        pngImage = io.BytesIO()
        Canvas(fig).print_png(pngImage)
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return render_template('index.html',image=pngImageB64String)
    else:
        return redirect('/')


@app.route('/keyword_search', methods = ['GET',"POST"])
def keyword_search():
    if request.method == 'POST':
        user_input = request.form['state']
        conn = db.connect()
        query1, query2, query3, query4 = "SELECT DISTINCT state from State", "SELECT DISTINCT county from County", "SELECT DISTINCT date from State", "SELECT DISTINCT Date from Vaccine"
        results1,results2,results3, results4 = conn.execute(query1).fetchall(),conn.execute(query2).fetchall(),conn.execute(query3).fetchall(),conn.execute(query4).fetchall()
        state_list, county_list, date_list, vac_date_list = [state[0].lower() for state in results1], [county[0].lower() for county in results2], [str(date[0]) for date in results3], [str(date[0]) for date in results4]
        if str(user_input).lower() in state_list:
            query = "SELECT date, cases from State where state=\"{}\";".format(user_input)
            results = conn.execute(query).fetchall()
            data = dict(results)
            date, cases = list(data.keys()), list(data.values())
            cases_diff = [cases[i]-cases[i-1] for i in range(1,len(cases))]
            query = "SELECT date, deaths from State where state=\"{}\";".format(user_input)
            results = conn.execute(query).fetchall()
            data = dict(results)
            date, death = list(data.keys()), list(data.values())
            death_diff = [death[i]-death[i-1] for i in range(1,len(death))]
            query = "SELECT Vaccine.Date, Vaccine.Doses_Administrated from Vaccine, State where Vaccine.State_FIPS = State.fips and State.state = \"{}\" and Vaccine.Vaccine_Type = 'ALL';".format(user_input)
            results = conn.execute(query).fetchall()
            data = dict(results)
            vac_date, doses = list(data.keys()),list(data.values())
            doses_diff = [doses[i]-doses[i-1] for i in range(1,len(doses))]
            query = "SELECT Vaccine.Date, Vaccine.Stage_1_Dose from Vaccine, State where Vaccine.State_FIPS = State.fips and State.state = \"{}\" and Vaccine.Vaccine_Type = 'ALL';".format(user_input)
            results = conn.execute(query).fetchall()
            data = dict(results)
            vac_date, stage1 = list(data.keys()),list(data.values())
            query = "SELECT Vaccine.Date, Vaccine.Stage_2_Dose from Vaccine, State where Vaccine.State_FIPS = State.fips and State.state = \"{}\" and Vaccine.Vaccine_Type = 'ALL';".format(user_input)
            results = conn.execute(query).fetchall()
            data = dict(results)
            vac_date, stage2 = list(data.keys()),list(data.values())
            with plt.style.context('ggplot'):
                fig,ax = plt.subplots(4,1,figsize=(7,15))
                fig.autofmt_xdate()
                ax[0].set_title(str(user_input).upper())
                ax[0].set_ylabel('Case Number')
                ax[0].plot(date,cases, "-", linewidth = 1, color='r')
                ax[1].set_ylabel('Death')
                ax[1].plot(date,death, "-", linewidth = 1, color='r')
                ax[2].plot(date[:-1],cases_diff,'-', linewidth = 1, color='r')
                ax[2].set_title('Daily Increment of Case Number')
                ax[3].plot(date[:-1],death_diff,"-",linewidth=1,color='r')
                ax[3].set_title('Daily Increment of Death Number')
            pngImage = io.BytesIO()
            Canvas(fig).print_png(pngImage)
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            with plt.style.context('ggplot'):
                fig,ax = plt.subplots(2,1,figsize=(7,10))
                fig.autofmt_xdate()
                ax[0].plot(vac_date,doses,"-",linewidth=1,color='r',label="Total Doses")
                ax[0].plot(vac_date,stage1,"--",linewidth=1,color='g',label="Stage 1")
                ax[0].plot(vac_date,stage2,"-.",linewidth=1, color='y',label="Stage 2")
                ax[0].set_title('Vaccine Administrated')
                ax[0].legend()
                ax[1].plot(vac_date[:-1],doses_diff,"-",linewidth=1,color='r')
                ax[1].set_title('Daily Increment of Doses Administrated')
            pngImage2 = io.BytesIO()
            Canvas(fig).print_png(pngImage2)
            pngImageB64String2 = "data:image/png;base64,"
            pngImageB64String2 += base64.b64encode(pngImage2.getvalue()).decode('utf8')
            return render_template('index.html',image1=pngImageB64String, image2=pngImageB64String2)
        elif str(user_input).lower() in county_list:
            query = "SELECT date, cases from County where county=\"{}\";".format(user_input)
            results = conn.execute(query).fetchall()
            data = dict(results)
            date, cases = list(data.keys()), list(data.values())
            cases_diff = [cases[i]-cases[i-1] for i in range(1,len(cases))]
            query = "SELECT date, deaths from County where county=\"{}\";".format(user_input)
            results = conn.execute(query).fetchall()
            data = dict(results)
            date, death = list(data.keys()), list(data.values())
            death_diff = [death[i]-death[i-1] for i in range(1,len(death))]
            with plt.style.context('ggplot'):
                fig,ax = plt.subplots(4,1,figsize=(7,10))
                fig.autofmt_xdate()
                ax[0].set_title(str(user_input).upper())
                ax[0].set_ylabel('Case Number')
                ax[0].plot(date,cases, "-", linewidth = 1, color='r')
                ax[1].set_ylabel('Death')
                ax[1].plot(date,death, "-", linewidth = 1, color='r')
                ax[2].plot(date[:-1],cases_diff,'-', linewidth = 1, color='r')
                ax[2].set_title('Daily Increment of Case Number')
                ax[3].plot(date[:-1],death_diff,"-",linewidth=1,color='r')
                ax[3].set_title('Daily Increment of Death Number')
            pngImage = io.BytesIO()
            Canvas(fig).print_png(pngImage)
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            return render_template('index.html',image1=pngImageB64String)
        elif str(user_input).lower() in date_list:
            query = "SELECT date, cases from County where date=\"{}\";".format(user_input)
            query_state = "SELECT date, cases from State where date = \"{}\";".format(user_input)
            results = conn.execute(query).fetchall()
            results2 = conn.execute(query_state).fetchall()
            date, cases_county = [item[0] for item in results], [item[1] for item in results]
            date, cases_state = [item[0] for item in results2], [item[1] for item in results2]
            query = "SELECT date, deaths from County where date=\"{}\";".format(user_input)
            query_state = "SELECT date, deaths from State where date=\"{}\";".format(user_input)
            results = conn.execute(query).fetchall()
            results2 = conn.execute(query_state).fetchall()
            date, death_county = [item[0] for item in results], [item[1] for item in results]
            date, death_state = [item[0] for item in results2], [item[1] for item in results2]
            query = "SELECT Date, Doses_Administrated, Doses_Allocated, Stage_1_Dose, Stage_2_Dose from Vaccine where Date = \"{}\";".format(user_input)
            results = conn.execute(query).fetchall()
            vac_date, dose, dose_alloc, stage1, stage2 = [item[0] for item in results],[item[1] for item in results],[item[2] for item in results],[item[3] for item in results], [item[4] for item in results]
            with plt.style.context('ggplot'):
                fig,ax = plt.subplots(2,2,figsize=(10,10))
                ax[0][0].set_title(str(user_input).upper()+' Statewise')
                ax[0][0].set_ylabel('Case Number')
                ax[0][0].hist(cases_state, bins = 20)
                ax[0][1].set_title(str(user_input).upper()+' Countywise')
                ax[0][1].set_ylabel('Case Number')
                ax[0][1].set_xlim(xmin = 0, xmax = 150000)
                ax[0][1].hist(cases_county, bins = 70)
                ax[1][0].set_title(str(user_input).upper()+' Statewise')
                ax[1][0].set_ylabel('Death')
                ax[1][0].hist(death_state, bins = 20)
                ax[1][1].set_title(str(user_input).upper()+' Countywise')
                ax[1][1].set_ylabel('Death')
                ax[1][1].hist(death_county, bins = 70)
                ax[1][1].set_xlim(xmin = 0, xmax=5000)
            pngImage = io.BytesIO()
            Canvas(fig).print_png(pngImage)
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            with plt.style.context('ggplot'):
                fig,ax = plt.subplots(2,1,figsize=(5,10))
                ax[0].set_title(str(user_input).upper()+' Nation-Wide Vaccine Distribution')
                ax[0].hist(dose, bins = 20, alpha = 0.5, label = 'Doses Administrated')
                ax[0].hist(dose_alloc, bins = 20, alpha = 0.5, label="Doses Allocated")
                ax[0].legend()
                ax[1].hist(stage1, bins = 20, alpha = 0.5, label="Stage 1 Vaccine Administrated")
                ax[1].hist(stage2, bins = 20, alpha = 0.5, label="Stage 2 Vaccine Administrated")
                ax[1].legend()
            pngImage2 = io.BytesIO()
            Canvas(fig).print_png(pngImage2)
            pngImageB64String2 = "data:image/png;base64,"
            pngImageB64String2 += base64.b64encode(pngImage2.getvalue()).decode('utf8')
            return render_template('index.html',image1=pngImageB64String, image2=pngImageB64String2)
        else:
            query = "SELECT date, sum(cases), sum(deaths) from State group by date;"
            conn = db.connect()
            results = conn.execute(query).fetchall()
            date, cases, death = [item[0] for item in results],[int(item[1]) for item in results],[int(item[2]) for item in results]
            data = {'Date':date, 'Cases':cases, 'Deaths':death}
            df = pd.DataFrame(data)
            df.iloc[0,0],df.iloc[0,1],df.iloc[0,2] = datetime.date(2020, 1, 22),1,0
            df = df.sort_values(by = ['Date'])
            plot = df.plot(x = 'Date', title = 'Covid-19 Historic Date: US')
            fig = plot.get_figure()
            fig.autofmt_xdate()
            pngImage = io.BytesIO()
            Canvas(fig).print_png(pngImage)
            pngImageB64String = "data:image/png;base64,"
            pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
            query = "SELECT date, sum(Doses_Administrated), sum(Doses_Allocated), sum(Stage_1_Dose), sum(Stage_2_Dose) from Vaccine where Vaccine_Type = 'ALL' group by Date;"
            conn = db.connect()
            results = conn.execute(query).fetchall()
            date, dose, dose_alloc, stage1, stage2 = [item[0] for item in results], [int(item[1]) for item in results], [int(item[2]) for item in results], [int(item[3]) for item in results], [int(item[4]) for item in results]
            data = {'Date':date, 'Does Administrated':dose, "Dose Allocated":dose_alloc,'Stage 1':stage1,'Stage 2':stage2}
            df = pd.DataFrame(data)
            df = df.sort_values(by = ['Date'])
            plot = df.plot(x = 'Date', title = 'Covid-19 Vaccination Data: US')
            fig = plot.get_figure()
            pngImage2 = io.BytesIO()
            Canvas(fig).print_png(pngImage2)
            pngImageB64String2 = "data:image/png;base64,"
            pngImageB64String2 += base64.b64encode(pngImage2.getvalue()).decode('utf8')
            return render_template('index.html', image1 = pngImageB64String, image2 = pngImageB64String2)
    else:
        return redirect('/')

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

@app.route('/group_by',methods=['GET','POST'])
def group_by():
    if request.method == 'POST':
        date = request.form['date']
        conn = db.connect()
        query = "SELECT date, avg(cases) from State group by date having date = \"{}\";".format(date)
        results = conn.execute(query)
        return render_template("average.html",data2=results)
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
    

@app.route("/")
def homepage():
    return render_template("index.html")