from bs4 import BeautifulSoup
import requests
import os
import sys
import math


#____________________Getting zipcode for job search________________________#
lineBreak1 =  ('*---------------------------------------*')
lineBreak2 = ('*_______________________________________*')
print(lineBreak1)
startTitle = ('Job Search')
print(startTitle.center(len(lineBreak1)))
print(lineBreak2)
jobSearch = input("What type of job are you looking for?: ")
jobSearch = jobSearch.strip()
jobSearch = jobSearch.replace(' ','-')
mainUrl = 'https://www.indeed.com/q-' + jobSearch + '-l-'
while True:
	zipCode = input('Enter your zip code: ').strip()
	if zipCode.isnumeric() and len(str(zipCode)) == 5:
		url = mainUrl + zipCode + '-jobs.html'
		break
	else:
		print('You must type a valid zip-code!\n')
result = requests.get(url)
soup = BeautifulSoup(result.text, "lxml")

#___________________Getting all jobs in zipcode_____________________________#
jobName = []
jobCode = []
sjCode = []
for i in soup.find_all(class_ = 'slider_container'):
	for x in i.find_all('h2'):
		x = x.text
		x = x.replace('new','')
		jobName.append(x)
for jobID in soup.select('[data-jk]'):
	idNumber = "job_" + jobID['data-jk']
	sjNumber = "sj_" + jobID['data-jk']
	jobCode.append(idNumber)
	sjCode.append(sjNumber)
if len(jobCode) == 0:
	print('\nSorry, there are currently no', jobSearch, 'jobs near', zipCode + '.\n\n\n')
	os.execl(sys.executable, sys.executable, *sys.argv)

#___________________main function(choosing a job)____________________________#
def main():
	print('\n')
	print(lineBreak1)
	title = jobSearch + ' jobs near ' + zipCode
	print(title.center(len(lineBreak1)))
	print(lineBreak2)
	count = 1
	for i in jobName:
		print(str(count) + ') ' + i)
		count = count + 1
	print(lineBreak1)
	choice = input('Type a number to learn more about the job: ')
	print(lineBreak2)
	if choice.isnumeric() == True and 0 < int(choice) <= count-1:
		choice = choice.replace(" ","")
		print('\n\n\n\n\n\n\n\n\n\n\n')
		chosenJob(choice)
	else:
		print("You must type a valid number!")
		main()

#______________________Getting info on chosen job____________________________#
def chosenJob(choice):
	choiceIndex = int(choice) - 1
	findID = jobCode[choiceIndex]
	findSJ = sjCode[choiceIndex]
	for v in soup.find_all("a", id=findID):
		extension = v['href']
	for x in soup.find_all("a", id=findSJ):
		extension = x['href']
	jobLink = 'http://www.indeed.com' + extension
	#print(jobLink)
	jobRequest = requests.get(jobLink)
	jobSoup = BeautifulSoup(jobRequest.text, "lxml")
	#We now have the selected job singled out so we can extract info
	for i in jobSoup.find_all('h1'):
		jobTitle = i.text
	for i in jobSoup.find_all(class_ = 'icl-u-lg-mr--sm icl-u-xs-mr--xs'):
		companyName = i.text
	for i in jobSoup.find_all('meta',itemprop='ratingValue'):
		companyRatingNum = float(i['content'])
		companyRatingNumRounded = math.floor(companyRatingNum)
		companyRatingStars = '* ' * companyRatingNumRounded
		companyRatingDesc = str(companyRatingNum) + ' out of 5'
		companyRating = companyRatingStars + '| ' + companyRatingDesc
	for i in jobSoup.find_all(class_ = 'jobsearch-jobLocationHeader-location'):
		companyLocation = i.text
	for i in jobSoup.find_all(class_ = 'jobsearch-JobMetadataHeader-item'):
		jobType = i.text
	#Checking for NaN values
	try:
		jobType
	except NameError:
		jobType = 'N/A'
	try:
		companyLocation
	except NameError:
		for i in jobSoup.find_all(class_ = 'jobsearch-RelatedLinks-link'):
			companyLocation = i.text
			companyLocation = companyLocation[companyLocation.find('in '):]
			companyLocation = companyLocation.replace('in ','')
	try:
		companyRating
	except NameError:
		companyRating = 'N/A'

	displayJob(jobTitle,companyName,companyRating,companyLocation,
		jobType,jobLink)
#____________________Dispaying the job to user________________________________#

def displayJob(jobTitle,companyName,companyRating,companyLocation,
	jobType,jobLink):
	lineBreak1 =  ('*---------------------------------------*')
	lineBreak2 = ('*_______________________________________*')
	print(lineBreak1)
	print(jobTitle.center(len(lineBreak1)))
	print(lineBreak2)
	print('\n')
	print('  Job Type: ', jobType)
	print('\n')
	print('  Job Location: ', companyLocation)
	print('\n')
	print('  Company Name: ',companyName)
	print('\n')
	print('  Company Rating: ',companyRating)
	print('\n')
	print('  Would you like to learn more about this job?')
	learnMore = input('  Type 1 for Yes\n  Type 2 for no\n  ')
	learnMore = learnMore.strip()
	if learnMore.isnumeric() and 0 < int(learnMore) < 3:
		if int(learnMore) == 1:
			print('*---------------------------------------------------------*')
			print('Click the link below to learn more about this job: ')
			print(jobLink)
			print('*_________________________________________________________*')
		elif int(learnMore) == 2:
			main()
	else:
		print('You must type a valid number!')
		displayJob(jobTitle,companyName,companyRating,companyLocation,
			jobType,jobLink)
#____________________________________________________________________________#
if __name__ == "__main__":
	main()