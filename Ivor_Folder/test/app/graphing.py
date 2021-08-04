# from flask import render_template, request, jsonify, redirect
# from app import app
# # from app import database as db_helper
# from app import db

import matplotlib.pyplot as plt
import base64
from io import BytesIO


def html_for_matplotlib_img(x_data, y_data):
	fig, ax = plt.subplots()
	ax.plot(x_data, y_data)


	tmpfile = BytesIO()
	fig.savefig(tmpfile, format='png')
	encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

	html = 'Some html head' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + 'Some more html'

	with open('test.html','w') as f:
	    f.write(html)