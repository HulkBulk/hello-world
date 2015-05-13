import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
plt.show()



def splitDataPerMatch(file='PremierLeague2011-12MatchbyMatch.csv')
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
	#op = df.groupby('Date')
	group = dict(list(op))
	#small = pd.DataFrame(df[['Shots On Target inc goals','Goals','Right Foot Shots On Target']])
	#scatter_matrix(small, alpha=0.2, figsize=(6, 6), diagonal='kde')
	plt.show()
	match_stat = {}
	for key in group:
		df_tmp = pd.DataFrame(group[key])
		if key not in match_stat:
			match_stat[key] = {}
		tmp_match_dict = {}
		all_players = {}
		currentposPlayer = {}
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
		match_stat[key] = all_players
	return match_stat
