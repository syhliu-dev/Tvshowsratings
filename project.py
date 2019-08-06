from bs4 import BeautifulSoup
import json
import urllib2
from time import sleep
import csv


#step 1
response = urllib2.urlopen('http://www.imdb.com/chart/toptv/?sort=nv,desc&mode=simple&page=1')
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, "html.parser")
output = open('top250_tvshows.html','w')
output.write(html.encode('utf-8'))
output.close()

# step 2

imdb_data = []
imdbids = []
titles = []
input_file = open('top250_tvshows.html', 'rU')
html_doc = input_file.read().decode('utf-8')
soup = BeautifulSoup(html_doc, 'html.parser') 
tables = soup.find('tbody', class_= "lister-list")
for row in tables.find_all('tr'):
	title_row = row.find('td', class_='titleColumn')
	movie_id = title_row.find('a').get('href')
	imdb_id = movie_id.split('/')[2]
	title = title_row.find('a').string
	rating_row = row.find('strong')
	if rating_row:
		rating = rating_row.string
		#print rating


	imdb_data.append((title,imdb_id,rating))
	titles.append(title.encode('utf-8'))


input_file.close()

output = open('top250_tvshows_output.tsv', 'w')
output.write('Title\tIMDB ID\tRating\n')
for t in imdb_data:
	line = '\t'.join(list(t)) + '\n'
	output.write(line.encode('utf8'))

output.close()

output_file = open('netflix_id.tsv','w')


for t in titles:
	netflix_api = t.replace(' ','%20')
	request_url = 'http://netflixroulette.net/api/api.php?title='+netflix_api
	#print request_url
	try:
		response = urllib2.urlopen(request_url)
	except urllib2.HTTPError:
		continue
	data = response.read().decode('utf-8')
	output_line = t+'\t'+data+'\n'
	output_file.write(output_line.encode('utf-8'))
output_file.close()

	

# Step 4
netflix_rating = []
rating_netflix = []
input = open('netflix_id.tsv', 'rU')
output = open('netflix.tsv','w')
output.write('Title,rating\n')
data_dict = {}
for l in input:
	(imdb_id, data) = l.split('\t')
	row = json.loads(data)
	rating = row['rating']
	title = row['show_title']
	if rating:
		output.write(title+','+rating+'\n')
		data_dict[title] = rating
		#print title
		#print data_dict[title]

		
		data_dict[title] = float(data_dict[title].encode('utf-8'))*2
		


final_results = [] 
outfile = open('final_output.csv', 'w')

for t in imdb_data:
	title = t[0].encode('utf-8')
	if title in data_dict:
		l = (title, t[2].encode('utf-8'), data_dict[title])
		final_results.append(l)



csvwriter = csv.writer(outfile)
# writes the header
csvwriter.writerow(['Title','IMDB Rating', 'Netflix Rating'])
# writes the data
csvwriter.writerows(final_results)

outfile.close()

