import bisect
import csv
import json
import time

####################################################
# Start taking time to measure performance of code #
####################################################
start_time = time.time()

####################################################
# First create the list with all the buckets in    #
# csv file, since the order of the buckets has to  #
# be the same as the one in the csv the execution  #
# of this line code is O(n) where n is the number  #
# of lines in the csv file.                        #
####################################################
with open('redshelf_challenge/purchase_buckets.csv', newline='') as buckets:
	bucketreader = csv.reader(buckets, delimiter='\n', quotechar='|')
	answer = []
	for row in bucketreader:
		values = [row[0],[]]
		####################################################
		# The list will contain dictionaries with 2 keys   #
		# "bucket" and "purchases"                         #
		####################################################
		answer.append(dict(zip(['bucket','purchases'],values)))

####################################################
# Next up we shall read the data from the other    #
# and sort it accordingly into the list "answer"   #
####################################################
with open('redshelf_challenge/purchase_data.csv', newline='') as datas:
	datareader = csv.reader(datas, delimiter='\n', quotechar='|')
	####################################################
	# The variable index_level stores the index and    #
	# level of priority of every match found in the    #
	# "answer" list	and is initiated with the lowest   #
	# level priority 0 on the last bucket which in     #
	# this case would be '*,*,*' that would match any  #
	# possible set 									   #
	####################################################
	index_level = [len(answer)-1,0]
	for rowdata in datareader:
		####################################################
		# In variable rowd we store the split string of    #
		# rowdata in order to get the values 			   #
		# 'publisher', 'duration' and 'price' and compare  #
		# them with the values from variable rowb which    #
		# contains these values for each bucket 		   #
		####################################################
		rowd = rowdata[0].split(',')
		for idx,rowbucket in enumerate(answer):
			rowb = rowbucket['bucket'].split(',')
			####################################################
			# According to the rules the level of importance   #
			# goes like this:								   #
			# -'publisher' HIGHEST							   #
			# -'duration'  MEDIUM							   #
			# -'price'     LOW 								   #
			# The number of values for each item is 2 which    #
			# can be either the current value or '*' and the   #
			# number of items is 3, which means that the       #
			# number of permutations is going to be equal to   #
			# 2**3 or 8 to be more precise.					   #
			# With this information we stablished the number   #
			# of level's of importance, from 0 to 7, 0 being   #
			# the lowest level and 7 the highest level.		   #
			# For each data element we evaluate each possible  #
			# combination starting from the highest one where  #
			# all the items of the data element matches the    #
			# items from the bucket. When a match is found we  #
			# then proceed to evaluate the 2nd value from the  #
			# variable index_level, if it's greater we replace #
			# the index and level with the current match, if   #
			# it's equal or lesser we ignore it.			   #
			####################################################
			if rowd[2].lower() == rowb[0].lower() and rowd[5] == rowb[2] and rowd[4] == rowb[1]:
				if index_level[1] < 7:
					index_level = [idx,7]

			elif rowd[2].lower() == rowb[0].lower() and rowd[5] == rowb[2] and rowb[1] == '*':
				if index_level[1] < 6:
					index_level = [idx,6]

			elif rowd[2].lower() == rowb[0].lower() and rowb[2] == '*' and rowd[4] == rowb[1]:
				if index_level[1] < 5:
					index_level = [idx,5]

			elif rowb[0] == '*' and rowd[5] == rowb[2] and rowd[4] == rowb[1]:
				if index_level[1] < 4:
					index_level = [idx,4]

			elif rowd[2].lower() == rowb[0].lower() and rowb[2] == '*' and rowb[1] == '*':
				if index_level[1] < 3:
					index_level = [idx,3]

			elif rowb[0] == '*' and rowd[5] == rowb[2] and rowb[1] == '*':
				if index_level[1] < 2:
					index_level = [idx,2]

			elif rowb[0] == '*' and rowb[2] == '*' and rowd[4] == rowb[1]:
				if index_level[1] < 1:
					index_level = [idx,1]

			else:
				pass
		####################################################
		# Finally we insert the data in the 'purcheses'    #
		# key of the 'answer' list where it will be sorted #
		# according to the 'order_id' and we also          #
		# reset the variable 'index_level' back to the     #
		# last bucket element '*,*,*' and the lowest       #
		# level 0.										   #
		####################################################
		bisect.insort(answer[index_level[0]]['purchases'], rowdata[0])
		index_level = [len(answer)-1,0]

print("--- %s seconds ---" % (time.time() - start_time))

####################################################
# Create and output the JSON file with the results.#
####################################################
with open('sorted_purchase_data.json', 'w') as outfile:
	json.dump(answer, outfile)