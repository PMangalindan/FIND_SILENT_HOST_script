## REMINDER! THIS SCRIPT USES os.chdir()
import os
import re
import textfsm
import pandas as pd
from datetime import datetime
import tkinter as tk
def get_value(key):
	''' gets variable values from settings file.
		MAKE SURE TO PUT THE RIGHT SETTINGS FILE PATH '''
	key = key
	with open("settings.txt") as settings_file:
			settings_file = settings_file.read()
	if '#' in settings_file.split(key)[0].split("\n")[-1]:
		msg = 'value is commented out'
		#plog(root,msg)
		return None
	else:
		#var = settings_file.split(key)[1].split("\n")[0].strip(" ").strip("\"").strip("\'")
		#plog(root,key)
		unstriped = settings_file.split(key)[1].split("\n")[0].strip()
		#plog(root,unstriped[0])
		if unstriped.lower()[0] ==  '[' and unstriped.lower()[-1] == ']':
			var1 = unstriped.strip('[').strip(']').split(',')
			var = [e.strip().strip("'").strip('"') for e in var1]
			return var
		elif '"' == unstriped[0]  or '"' == unstriped[-1] or "'" == unstriped[0]  or "'" == unstriped[-1]:
			#plog(root,"is string")
			var = unstriped.strip("\"").strip("\'")
			return var
		elif  unstriped.isnumeric():
			var = int(unstriped)
			return var
		elif unstriped.lower() == 'true':
			var = True
			return var
		elif unstriped.lower() ==  'false':
			var = False
			return var
		else:
			plog(root,f"{unstriped} -invalid variable set in settings") 
def pull_hostname(data):
	try:
		data = data
		hostname2 = data.split("#")
		hostname3 = hostname2[0].split("\n")
		hostname_fin = hostname3[-1]
		hostname_fin = hostname_fin.strip()
		plog(root,f" hostname ({hostname_fin})")
		return hostname_fin
	except:
		plog(root,f"ERROR!!! -pull_hostname()- ADVANCE Contact Purple")
def initializ_spliter():
	#para_fname 
	try:
		inpt_path = sys.argv[1]	  #path=
		if inpt_path == '-f':
			inpt_path = get_value('inpt_path=')
			inpt_path = F'path={inpt_path}'
		plog(root,'________')
		#plog(root,inpt_path)
		####################################################################################
		if "path=" in inpt_path:
			path= inpt_path.split("path=")
		else:
			inpt_path = get_value('inpt_path=')
			path = ["", inpt_path]
			plog(root,"""--[path] argument issue. this should point to the files inside the folder.
			make sure the format is [name_edit.py path="{path}" replace="{word_to_find_in_file_name}" with="{new_word_to_place}"--
			""")
	except:
		try:
			plog(root,'getting input(s) path from settings.txt')
			inpt_path = get_value('inpt_path=')
			path = ["", inpt_path] # DELETE
		except: 
			plog(root,"""--CHECK settings.txt if path is a correct format.""")
	return path
def list_file_names():
	try:
		directory = path[1].strip("\"")
		#plog(root,directory)
		file_list = []
		for filename in os.scandir(directory):
			if filename.is_file():
				filename_str = r"{}".format(filename)
				file_list.append(filename_str.split("'")[1])
		return file_list
	except:
		plog(root,"ERROR -list_file_names()-")
def plog(root, string, log_only=False):
	"""prints and logs string"""
	global session_id #so it wont have to create multiple text file for every plog call. this will ensure that only one text file will be generated for every session.
	string = str(string)
	if log_only == False: #prints if log_only is false default is false
		print(string)
	try:
		session_id = session_id # checks if session_id is defined 
	except:
		from datetime import datetime
		date_now = datetime.now().strftime("%m-%d-%y_%H%M%S")  # defines the session id
		session_id = str(date_now)
	output_folder_log = fr'{root}\\print_log\\'	# this is the log folder path
	try:
		if os.path.exists(output_folder_log): # checks if folder already exist, if not the it will create one
			pass
		else:	
			os.mkdir(output_folder_log)
	except:
		import os
		if os.path.exists(output_folder_log): 
			pass
		else:	
			os.mkdir(output_folder_log)
	with open(f'{output_folder_log}\\plog_{session_id}.txt', 'a') as f: #saves the string in the text file 
		f.write(string)
		f.write('\n')
	return
def calc_depth(root):
	root = root
	master_lst = []
	master_lst.append(root)
	for path in master_lst:
		for e in os.listdir(path):
			p = f'{path}\\{e}'
			if os.path.isdir(p):
				#plog(root,p)
				master_lst.append(p)
	return len(master_lst[-1].split(root)[1].split('\\')) 
def main():
	ignore_uplinks = get_value("ignore_uplinks=")
	ignore_list = get_value("switch_ignore_list=")
	try:
		os.chdir(root)
	except:
		pass
	root = os.getcwd()
	#root = os.getcwd()
	try:
		path = initializ_spliter()
	except:
		#plog(root,"--error initializ_spliter()")
		plog(root,"--error initializ_spliter()")
		##update_log()
	try:
		f_lst = list_file_names()
	except:
		#plog(root,"--error list_file_names()")
		plog(root,"--error list_file_names()")
		##update_log()
	'''with open(f'oui.txt',  encoding="utf8") as f:
		oui_data = f.read()'''
	levels_list = []
	first_level = []
	branches_found_list = []
	plog(root,path[1])
	path_fix = path[1].strip('"')
	first_level.append(path_fix)
	levels_list = {}
	for ctr in range(calc_depth(path[1])):
		plog(root,ctr+1)
		levels_list[str(ctr+1)] = []
	levels_list['1'].append(first_level)
	mac_ip_map_list = []
	######################################################################################
	final_output_list = []
	sma_data_lsit = []
	silent_ports = []
	summary_silent_ports_data = []
	
	#final_output_list.append(f"IGNORE THE FOLLOWING SWITCHES: {ignore_list}")
	
	
	for i, level_lst in levels_list.items():		
		#i = i + 1
		plog(root,f"(splitter_key_1)------------------------------DIRECTORY LEVEL-{i}-------------------------------------------------")
		plog(root,f'-------------------------------------------------------------------------------- LEVEL {i}')
		for level_lst in level_lst:
			plog(root,'-------')
			for path_fix in level_lst:
				plog(root,f"DIR-----{path_fix}")
				##update_log()
				path_fix_temp = f"{path_fix}"
				path_fix = path_fix_temp
				dir_list = os.chdir(f"{path_fix}")
				if len(os.listdir(dir_list)) > 0:
					for f_name in os.listdir(dir_list):
						skip = 0
						try:
							if os.path.isdir(f_name):
								gate = 0
							else:
								gate = 1
						except:
							plog(root,f"error-- gate_var - {f_name}")
							plog(root,f"error-- gate_var - {f_name}")
							##update_log()
						if gate == 1:
							####################################################################### regex area
							host_nam = ""
							plog(root,f"--PROCESSING [{f_name}]")
							##update_log()
							try:
								if ".txt" in f_name or ".log" in f_name:
									try:
										txt_file = open(f_name, "r")
										plog(root,f"----opening [{f_name}]")
										plog(root,f"----opening [{f_name}]")
										##update_log()
										text = txt_file.read()
										txt_file.close()
									except:
										plog(root,"error opening file-- it expects .txt or .log---- saving this file name")
										plog(root,"error opening file-- it expects .txt or .log---- saving this file name")
										##update_log()
										plog(root,f" BAD file --{f_name}")
										##update_log()
									host_nam = pull_hostname(text) ############################# !!!!!!!!!!! HOSTNAME !!!!!!!!!!
									######################################
									plog(root,"pulling data..")
							except Exception as e:
								plog(root,'something is wrong with the file')
								plog(root,e)
								
							if host_nam == "":
								skip = 1
							if host_nam in ignore_list:
								skip = 1
								
							if skip == 0:
							############################################################## here we pull the data from the txt
								comnd = 0
								patt = "#*\s*[sS][hH]\S*\s+[cC][oO][nN]\S*\s*\n" #<<<<< ReGEX for all shortcut of show connection
								match = re.findall(patt , text)
								try:
									sis_patt = "#*\s*show interface status" #<<<<< ReGEX for all shortcut of show arp
									sis_match = re.findall(sis_patt , text)
									sis_data = text.split(sis_match[0])[1].split(host_nam)[0]
									final_output_list.append("_"*80)
									final_output_list.append(host_nam)
									final_output_list.append(sis_match[0] + sis_data)
									sis_text = final_output_list[-1]
								except:
									final_output_list.append(fr"failed-possible that command with pattern'{sis_patt}'is not in the file.")
								try:
									sma_data_list = []
									sma_patt = "#*\s*show mac address-table" #<<<<< ReGEX for all shortcut of show arp
									sma_match = re.findall(sma_patt , text)
									sma_data = text.split(sma_match[0])[1].split(host_nam)[0]
									final_output_list.append(sma_match[0] + sma_data)
									sma_text = final_output_list[-1]
								except:
									final_output_list.append(fr"failed-possible that command with pattern'{sma_patt}'is not in the file.")
								################################################################################################################ data processing
								with open(fr"{root}\\textfsm_files\\cisco_ios_show_interface_status.textfsm") as template: 
									re_table = textfsm.TextFSM(template)
									#print(re_table)
								sis_extract = re_table.ParseText(sis_text)
								connected_ports = []
								
								for interf in sis_extract:
									plog(root,interf[0], log_only = True)
									if 'routed' in interf[0] and ignore_uplinks == True:
										plog(root, "IGNORING this uplink! (go to settings.txt to change this policy)")
										#ignore bcause uplink
										
										pass
									else:
										port = interf[0].split()[0]
										connected_ports.append(port)
								silent_ports.append(host_nam)
								silent_ports.append("This switch potentially has silent hosts on the following ports:")
								
								
								
								
								#if ignore_uplinks == True:
									#silent_ports.append("IGNORING uplinks! (go to settings.txt to change this policy)")
									
									
									
								temp_list = []
								port_count = 0
								for port in connected_ports:
									if port not in sma_text:
										silent_ports.append(port)
										
										temp_list.append(port)
										port_count = port_count  + 1
										
										
								
								if len(temp_list) == 0:
									summary_silent_ports_data.append([host_nam, "-----------", str(ignore_uplinks)]) # this is for the summary tab
								else:
									summary_silent_ports_data.append([host_nam, "SILENT HOSTS", str(ignore_uplinks)]) # this is for the summary tab
									
									
								if port_count == 0:
									
									del silent_ports[-1]
									del silent_ports[-1]
									
								else:	
									silent_ports.append("_"*80)
								silent_ports_text = "\n".join(silent_ports)
								#plog(silent_ports_text)
								######################################################################################################################################
								i = 0
						else:
							if os.path.isdir(f_name):
								plog(root,f"--(NEW PATH FoUND!) -- recording path [{f_name}]")
								##update_log()
								plog(root,f"""((SKIPED))-- "{f_name}" this is a [FOLDER]""")
								branch = os.getcwd().split("\\")
								ii = len(root) - len(branch)
								num = ii * -1
								current_branch = branch[num:]   ### temp value ##################################
								current_branch = "\\".join(current_branch)
								current_branch_temp =   fr"{current_branch}"
								current_branch =   current_branch_temp
								found_branch_dir  = f"{current_branch}\\{f_name}"
								branches_found_list.append(found_branch_dir)
							else:
								plog(root,f"""SHOULD BE IMPOSSIBLE TO GET HERE""")
					try:			
						key = len(branches_found_list[0].split(path[1])[1].split('\\'))
						levels_list[f'{key}'].append(branches_found_list)   
						branches_found_list = [] #to empty the list
					except:
						pass
					'''for lev in levels_list:
						if len(lev) == 0:
							indx = levels_list.index(lev)
							del levels_list[indx]'''
					branches_found_list = [] #to empty the list
				os.chdir(root)
				#plog(root,os.getcwd())
				#plog(root,levels_list)
		plog(root,"_"*80)
	os.chdir(root)
	##update_log()
	plog(root,'\n\n')
	plog(root,"_"*80)
	plog(root,'saving..')
	final_arp_output = '\n'.join(final_output_list)
	plog(root,"_"*80)
	plog(root, "SILENT PORTS FOUND")
	plog(root, silent_ports_text)
	plog(root,"_"*80)
	#plog(root,final_arp_output)
	date_now = datetime.now().strftime("%m-%d-%y_%H-%M-%S")
	global out_file_name
	out_file_name = f'find_silent_host_DATA_{date_now}'
	
	
	from tabulate import tabulate
	
	
	
	
	display_blank_results=get_value('display_blank_results=')
	
	if display_blank_results:
		pass
	else:	
		summary_silent_ports_data = [data for data in summary_silent_ports_data if data[1] != '-----------']
		
	summary = tabulate(summary_silent_ports_data, headers = ["HOSTNAME", 'STATUS', "IGNORE UPLINKS POLICY"], tablefmt= "orgtbl")	
	
	policy_msg = "\n"
	if ignore_uplinks:
		policy_msg = "IGNORING uplinks! (go to settings.txt to change this policy)"
	
	with open(f'{out_file_name}.txt', 'w') as f:
		f.write("\n".join([f"IGNORE THE FOLLOWING SWITCHES: {ignore_list}",policy_msg, summary,"_"*80, silent_ports_text, "_"*80]))
	plog(root,'saved..')
	plog(root,out_file_name)
	
	with open(f'temp_file_name.txt', 'w') as f:
		f.write(out_file_name)
	
	plog(root, summary)
	
	

def open_settings_file():
	#inputdir = r'C:\Users\Admin\Desktop\work\FIND_SILENT_HOST_TESTING_5_GUI\\settings.txt'
	#filepath = filedialog.askopenfilename(initialdir = inputdir, filetypes=[("text files", "*.txt")])
	file = inputdir.split('\\')[-1]
	os.chdir(inputdir.split(file)[0])
	os.startfile(file)
	#os.chdir(root)
	return
	
def open_report():
	#inputdir = r'C:\Users\Admin\Desktop\work\FIND_SILENT_HOST_TESTING_5_GUI\\settings.txt'
	#filepath = filedialog.askopenfilename(initialdir = inputdir, filetypes=[("text files", "*.txt")])
	with open('temp_file_name.txt', 'r') as f:
		# read the ignore list into a set
		out_file_name = f.read().strip()
	out_file_name = f'{root}\\{out_file_name}.txt'
	
	os.remove('temp_file_name.txt')
	
	file = out_file_name.split('\\')[-1]
	os.chdir(out_file_name.split(file)[0])
	os.startfile(file)
	#os.chdir(root)
	return


	
if __name__ == '__main__':
	root_dir = os.getcwd()
	inputdir = fr'{root_dir}\\settings.txt'
	
	#global out_file_name
	#out_file_name = ''
	
		
	try:
		root = tk.Tk()
		
		screen_loc_x = 750
		screen_loc_y = 350
		#global inputdir
		#inputdir = f'{root_dir}\\input_settings.txt'
		#global output_path
		
		
		
		root_geo  = f'1000x550+{screen_loc_x}+{screen_loc_y}'
		root.geometry(root_geo)
		root.title('FIND_SILENT_HOST_5')
		label1 = tk.Label(root, text = f'''open settings file-''', font= ('System', 12), bd= 12,  )
		label1.pack(padx='3', pady='3')
		button_fileEx = tk.Button(root, text = f'SETTINGS', bg='white', font= ('System', 8), bd= 12, command=open_settings_file)
		button_fileEx.pack(padx='3', pady='3')
		
		
		
		label1 = tk.Label(root, text = '''click RUN when ready..''', font= ('System', 12), bd= 12,  )
		label1.pack(padx='30', pady='30')
		buttonrun = tk.Button(root, text = 'RUN', bg='green', font= ('System', 17), bd= 12, command=main)
		buttonrun.pack(padx='3', pady='3')
		buttonrep = tk.Button(root, text = 'result', bg='white', activebackground= 'grey', font= ('System', 17), bd= 12, command=open_report)
		buttonrep.pack(padx='3', pady='3')
		
		
		
		
		root.mainloop()
		#time.sleep(5)
		#print(buttonrun.command)
		#root_b.destroy()
	except Exception as e:
		plog(root, e)