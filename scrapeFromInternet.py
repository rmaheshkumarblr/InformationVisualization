from bs4 import BeautifulSoup
import urllib
import sys
import csv
import time
reload(sys)  
sys.setdefaultencoding('utf8')


content = ""
years = ["1920","1921","1922","1923","1924","1925","1926","1927","1928","1929","1930","1931","1932","1933","1934","1935","1936","1937","1938","1939","1940","1941","1942","1943","1944","1945","1946","1947","1948","1949","1950","1951","1952","1953","1954","1955","1956","1957","1958","1959","1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016"]
years = ["1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016"]

# years = ["1995"]

#years = ["1958"]
for year in years:
  #time.sleep(120)
  yearHtmlContent = urllib.urlopen("http://www.planecrashinfo.com/" + year + "/" + year + ".htm").read()
  soup = BeautifulSoup(yearHtmlContent)
  getATags = soup.find_all("a")
  pagesToCheck = []
  for element in getATags:
    if element["href"] != "http://www.planecrashinfo.com/index.html" :
      pagesToCheck.append(element["href"]);
  for page in pagesToCheck:
    print "Year: " , year , " Article: " , page
    subPage = urllib.urlopen("http://www.planecrashinfo.com/" + year + "/" + page).read()
    soupSub = BeautifulSoup(subPage)
    td = soupSub.find_all("td",{'align': 'left'})
    count = 0 
    for element in td:
      if element.get_text().strip() == "-" and count == 0:
        pass
      elif element.get_text().strip() == "ACCIDENT DETAILS" :
        content.strip("_")
        if content != "":
          content += "\n"
      else:
        count += 1
        if "\xc2" in str(element.get_text()):
          content += str(element.get_text()).split("\xc2")[0].strip() 
        else:
          content += str(element.get_text()).strip().replace('\n', '')
        if count % 13 != 0 :
          content += "_"
  csvOutput=csv.reader(content.split("\n"), delimiter='_')
  with open( year + ".csv", 'w') as mycsvfile:
    thedatawriter = csv.writer(mycsvfile)
    thedatawriter.writerow(["Date", "Time", "Location","Operator", "Flight No", "Route","AC Type", "Registration", "CN / LM","Aboard", "Fatalities", "Ground", "Summary"])
    for row in csvOutput:
        thedatawriter.writerow(row)
