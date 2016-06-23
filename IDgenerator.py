# id generator

# id is in the form of 'journal_articleID'. This serves as input to the reader app

import os, csv

dir_name = 'ScienceDirect'
output_name = './'+dir_name+'_id_list.csv'
wd = './'+dir_name

papers = os.listdir(wd)
writer=csv.writer(open(output_name,'wb'))
for paper in papers:
	ID = dir_name+'_'+paper
	writer.writerow([ID])