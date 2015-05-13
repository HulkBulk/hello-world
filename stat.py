import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
plt.show()
def splitDataPerMatch(file='PremierLeague2011-12MatchbyMatch.csv'):
	"""Split all data per match and date
		@params: file path to analys football stats
		-------
		
		@return: match statistic into a dictianary , key=(team1,team2,Date of match), value=players stats into a dictionary
	"""
	# Load Premier League 2011/2012 data
	df = pd.read_csv(file,sep=';')

	# Useless columns for first analysis
	columnNotUsed = ['Player ID','Team Id']

	# Drop all useless data
	df = df.drop(columnNotUsed,axis=1)

	# Group by match (You see only two team per 'Opposition Id')
	op= df.groupby(['Team','Opposition','Date'])

	group = dict(list(op))

	# Match statistics per date
	match_stat = {}
	
	for key in group:
		df_tmp = pd.DataFrame(group[key])
		key1 = str(key).replace(',',' ').replace(')',' ').replace('(',' ').replace("'",' ').strip()
		if key1 not in match_stat:
			match_stat[key1] = {}
		tmp_match_dict = {}
		
		#All player into the current match (See key)
		all_players = {}
		currentposPlayer = {}

		# Fullname definition
		forename = list(group[key]['Player Forename'])
		surname  = list(group[key]['Player Surname']) 

		for i in xrange(len(forename)):
			fullname = str(forename[i])+' '+str(surname[i])
			all_players[fullname] = {}
			currentposPlayer[i] = fullname
		for key_group in group[key]:
			grou = list(group[key][key_group])
			for i in xrange(len(grou)):
				all_players[currentposPlayer[i]][key_group] = grou[i]
		match_stat[key1] = all_players
	return match_stat
def forceGraph(match_stat):
	allnodes = {'nodes':[]}
	links = {'links':[]}
	primaryNodes = []
	nodesHash = {}
	linksArray = []
	nodesArray = []
	#structure { "nodes": [ {"name":"p1"}
	counter = 0
	for key in match_stat:
		node = { 'label' : key, 'id' : counter, 'color' : "green", 'textcolor' : "black", 'size' : 20, 'desc' : "" }
		if node['label'] not in nodesHash:
			allnodes['nodes'].append(node)
			nodesArray.append(node)
			nodesHash[node['label']] = counter
			counter += 1
		for player in match_stat[key]:
			stats = match_stat[key][player]
			nodeplayer = { 'label' : player, 'id' : counter, 'color' : "red", 'textcolor' : "black", 'size' : 5, 'desc' : "" }
			if nodeplayer['label']  not in nodesHash:
				allnodes['nodes'].append(nodeplayer)
				nodesArray.append(nodeplayer)
				nodesHash[nodeplayer['label']] = counter
				counter += 1
			participation = 0.0
			stats_weight = {}
			#json.dumps(stats_weight,'weigthedmeta.json')
			#for key in stats.keys():
			#	print key
			#	stats_weight[key] = raw_input()
			#json.dumps(stats_weight,'weigthedmeta.json')
			#raw_input()
			denom = 0.0
			for keystat in stats:
				try:
					if 'unsucess' in keystat.lower():
						participation += float(stats[keystat])*(-1)
						denom += -1
					elif 'sucessful' in keystat.lower():
						participation += float(stats[keystat])*1
						denom += 1
					else:
						participation += float(stats[keystat])
						denom += 1
				except:
					print 'No float in to ',keystat
					
			participation = np.log(participation/denom+1)
			if participation >0:
				link = { 'desc' : "RAS", 'source' : nodesHash[nodeplayer['label']], 'target' : nodesHash[node['label']], 'weight' : participation, 'color' : "grey" } 
				linksArray.append(link)
			#links['links'].append({'source':player,'target':key,'weight':participation})
	return nodesHash,linksArray,nodesArray
def writefile(nodesHash,linksArray,nodesArray):
	with open('Levenshtein.js','wb') as f:
		f.write('var nodesArray = [\n')
		for node in nodesArray[:-1]:
			f.write(str(node)+',\n')
		f.write(str(nodesArray[-1])+'\n')
		f.write('];\n')
		f.write('var nodesHash = [];')
		for key in nodesHash:
			f.write('nodesHash["'+str(key)+'"]='+str(nodesHash[key])+';\n')
		f.write('var linksArray = [\n')
		for links in linksArray[:-1]:
			f.write(str(links)+',\n')
		f.write(str(linksArray[-1])+'\n')
		f.write('];')
match_stat = splitDataPerMatch()
nodesHash,linksArray,nodesArray = forceGraph(match_stat)
writefile(nodesHash,linksArray,nodesArray)
