import os
import pickle
import sqlite3
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, render_template

from .graph import create_plot
from flaskapp import app,db
from .models import User
from .mlpmodel import extract_feature,loaded_model,LE
from .help_functions import allowed_file

STATE = False

con = sqlite3.connect("flaskapp/emotions.db")
df = pd.read_sql_query("SELECT * FROM user ORDER BY id DESC LIMIT 5", con)
df['emotion_code'] = df.emotion.map({'happy':'&#128513;','angry':'&#128544;','surprised':'&#128550;'})
con.close()


# home display tabel and countplot
@app.route('/')
def home():
	"""
	home()
	Home page 
	return table of users' data predictions
	and a 
	"""
	global STATE
	if STATE:
		global df
		con = sqlite3.connect("flaskapp/emotions.db")
		df = pd.read_sql_query("SELECT * FROM user ORDER BY id DESC LIMIT 5", con)
		df['emotion_code'] = df.emotion.map({'happy':'&#128513;','angry':'&#128544;','surprised':'&#128550;'})
		con.close()
	STATE = False
	s = df.emotion.value_counts()
	x = s.index.values
	y = s.values
	bar = create_plot(x,y)
	return render_template('home.html',column_names=df.columns.values, row_data=list(df.values.tolist()),
							link_column="emotion_code", zip=zip,title='Home',plot=bar)

# Preddiction page
@app.route('/predict', methods=['POST','GET'])
def upload_file():
	"""
	"""
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			features_extracted = extract_feature(os.path.join(app.config['UPLOAD_FOLDER'], filename), mfcc=True, chroma=True, mel=True)
			y_pred = loaded_model.predict([features_extracted])
			emotion = LE.inverse_transform(y_pred)[0]
			flash(f'{emotion}')
			global STATE
			STATE = True
			u = User(username=request.form.get('fullname'),filename=filename,emotion=emotion)
			db.session.add(u)
			db.session.commit()
			return redirect('/')
		else:
			flash('Allowed file types are wav')
			return redirect(request.url)
	
	return render_template('predict.html',title='Predict')

# about page
@app.route('/about')
def about():
	"""
	about():
	it's used for get request to return page describe project and a brief about developers
	"""
	return render_template('about.html',title='About')
