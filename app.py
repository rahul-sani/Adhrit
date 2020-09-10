from adhrit.adhrit import main
from flask import Flask, json, jsonify, render_template, request
from threading import Thread
from http import HTTPStatus
import os, configparser, time
from adhrit.recons.dbaccess import dbconnection, select_query
from adhrit.recons.reset import reset_scanid, reset_db
import sqlite3


ALLOWED_EXTENSIONS = {'apk'}

app = Flask(__name__)



def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_config_data(key):
	check_deps = configparser.ConfigParser()
	check_deps.read('adhrit/config')                                         ####
	return check_deps.get('config-data', str(key))

def update_scanid():

	# Updating config data

	update_config = configparser.ConfigParser()
	update_config.read('adhrit/config')
	thescanid = update_config.get('config-data', 'scan_id')
	thescanid = int(thescanid) + 1 

	update_config.set('config-data', 'scan_id', str(thescanid))
	with open('adhrit/config', 'w') as updatedconf:
			update_config.write(updatedconf)



@app.route('/scan',  methods=['POST'])
def scan():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')
			return HTTPStatus.NO_CONTENT

		uploaded_files = request.files["file"]
		if uploaded_files and allowed_file(uploaded_files.filename):
			uploaded_files.save(uploaded_files.filename)
			# Renaming to app.apk
			source =  uploaded_files.filename
			dest = 'app.apk'
			os.rename(source, dest)
			
		  
			# main()
			thesid = get_config_data('scan_id')
			rows = getreport(thesid)
			print(rows)
			response = rows, {'Access-Control-Allow-Origin': '*'}  
			# update_scanid()
			return  response
	return jsonify(status_msg="apk not sent properly")


def getreport(scan_id):
	sid = scan_id
	query = "SELECT * FROM `DataDB` WHERE `ScanId` = '%s'" % sid
	rows = select_query(query)
	rowarray_list = []
	for row in rows:
		d = dict(zip(row.keys(), row))   # a dict with column names as keys
		rowarray_list.append(d)
	# json_data = json.dumps(rowarray_list)
	# data = json.loads(json_data)
	data = rowarray_list[0]

	null_key_list = []
	for key, value in data.items():
		val_list = eval(value)
		if not val_list:
			# print(key)
			null_key_list.append(key)

	# removing all unused components
	for key in null_key_list:
		del data[key]

	response = {}
	for key, value in data.items():
		val_list = eval(value)
		if key == 'Activity':
			response.__setitem__(key, val_list)
		if key == 'ExportedActivity':
			response.__setitem__(key, val_list)
		if key == 'BroadcastReceiver':
			response.__setitem__(key, val_list)
		if key == 'ExportedReceiver':
			response.__setitem__(key, val_list)
		if key == 'Permission':
			response.__setitem__(key, val_list)
		if key == 'CriticalPerm':
			response.__setitem__(key, val_list)
		if key == 'CustomPerm':
			response.__setitem__(key, val_list)
		if key == 'Deeplinks':
			response.__setitem__(key, val_list)
		if key == 'Service':
			response.__setitem__(key, val_list)
		if key == 'ExportedService':
			response.__setitem__(key, val_list)
		if key == 'Taskaffinity':
			response.__setitem__(key, val_list)
		if key == 'ImplicitIntent':
			tmp_imp_intents = []
			for key in val_list.keys():
				tmp_imp_intents.extend(val_list[key])
			key = 'ImplicitIntent'
			response.__setitem__(key, tmp_imp_intents)
		if key == 'Provider':
			tmp_providers = []
			provider_obj_list = []	
			for key_parent,value_parent in val_list.items():
				for key, value in value_parent.items():
					if key == 'name':
						temp = key + ' : ' + value
						provider_obj_list.insert(0, temp)
					else:
						temp = key + ' : ' + value
					provider_obj_list.append(temp)
				provider_obj_list.append("")
				tmp_providers.extend(provider_obj_list)
				provider_obj_list = []
			key = 'Provider'
			response.__setitem__(key, tmp_providers)

	return response

@app.route("/testbed")
def test():
	sid = 1
	query = "SELECT * FROM `DataDB` WHERE `ScanId` = '%s'" % sid
	rows = select_query(query)
	rowarray_list = []
	for row in rows:
		d = dict(zip(row.keys(), row))   
		rowarray_list.append(d)
	json_data = rowarray_list
	data = json_data[0]
	

	null_key_list = []
	for key, value in data.items():
		val_list = eval(value)
		if not val_list:
			# print(key)
			null_key_list.append(key)
	
	# print(null_key_list)

	# removing all unused components
	for key in null_key_list:
		del data[key]
		
	response = {}
	for key, value in data.items():
		val_list = eval(value)
		if key == 'Activity':
			response.__setitem__(key, val_list)
			
		if key == 'ExportedActivity':
			response.__setitem__(key, val_list)
		if key == 'BroadcastReceiver':
			response.__setitem__(key, val_list)
		if key == 'ExportedReceiver':
			response.__setitem__(key, val_list)
		if key == 'Permission':
			response.__setitem__(key, val_list)
		if key == 'CriticalPerm':
			response.__setitem__(key, val_list)
		if key == 'CustomPerm':
			response.__setitem__(key, val_list)
		if key == 'Deeplinks':
			response.__setitem__(key, val_list)
		if key == 'Service':
			response.__setitem__(key, val_list)
		if key == 'ExportedService':
			response.__setitem__(key, val_list)
		if key == 'Taskaffinity':
			response.__setitem__(key, val_list)
		if key == 'ImplicitIntent':
			tmp_imp_intents = []
			for key in val_list.keys():
				tmp_imp_intents.extend(val_list[key])
			key = 'ImplicitIntent'
			response.__setitem__(key, tmp_imp_intents)
		if key == 'Provider':
			tmp_providers = []
			provider_obj_list = []	
			for key_parent,value_parent in val_list.items():
				for key, value in value_parent.items():
					if key == 'name':
						temp = key + ' : ' + value
						provider_obj_list.insert(0, temp)
					else:
						temp = key + ' : ' + value
						provider_obj_list.append(temp)
				provider_obj_list.append("")
				tmp_providers.extend(provider_obj_list)
				provider_obj_list = []
			key = 'Provider'
			response.__setitem__(key, tmp_providers)



	# for key, value in data.items():
	# 	if key == 'Activity':
	# 		val_list = eval(value)
	# 		j=[]
	# 		for i in val_list:
	# 			j.append(i)



	return response






@app.route('/')
def func():
	return "Adhrt up and flying hiGh *-*"




@app.route("/reset")
def reset():
	reset_db()
	reset_scanid
	return jsonify(sts_msg = "Resetted db and Scan Id!")

	
if __name__ == '__main__':
	app.run(debug=True, use_reloader=False)


# curl -X POST -F file=@app.apk http://localhost:5000/scan
