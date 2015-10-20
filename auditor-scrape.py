#auditor-scrape.py

#fill the toolbox
import mechanize, csv

from bs4 import BeautifulSoup

#tell mechanize how to deal with the anonymous form
def select_form(form) : 
	return form.attrs.get('id', None) == 'Form1'

#have mechanize go get that website
br = mechanize.Browser()
br.open('http://enrarchives.sos.mo.gov/enrnet/PickaRace.aspx')

#look at that form and tell it what you want
br.select_form(predicate=select_form)
br.form['ctl00$MainContent$cboElectionNames'] = ['750003143']
br.form['ctl00$MainContent$cboRaces'] = ['460006719']

# Submit the form
br.submit(id="MainContent_btnCountyChange")

# Get the post-submission HTML
html = br.response().read()

# Create a BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

# Find the table
table = soup.find('table', id = 'MainContent_dgrdCountyRaceResults')

# wait for it
output = []

# get headers, no commas...couldn't figure out regular expressions by now
for row in table.find_all('tr'):
	output_header = []
	header = [str(cell.text).replace(',','').replace("\r\n", "").upper() for cell in row.find_all('th')]
	output_header.append(str(header).strip('[]').replace("'","").replace('"',''))
	break

# Get that data, no commas
for row in table.find_all('tr')[2:]:
	output_row = []
	data = [cell.text.replace(',','').upper() for cell in row.find_all('td')]
	output_row.append(str(data).strip('[]').replace("'","").replace('u','').strip("''"))
	output.append(output_row)

##Optional output
#print str(output_header).strip('[]') + "\n"
#print str(output)

with open('output.csv', 'wb') as csvfile:
	writer = csv.writer(csvfile, escapechar='\t', quoting=csv.QUOTE_NONE)
	writer.writerow(output_header)
	writer.writerows(output)
#escape set as tab, ugly, but it seemed to work