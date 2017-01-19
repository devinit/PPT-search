from xml.dom import minidom
from SPARQLWrapper import SPARQLWrapper, XML
from xml.etree.ElementTree import fromstring, ElementTree
import re

 ### Functions clean_variables  and translations deal with searching and translating a term; clean_variables2 and translations2 deal with searching and translating a code ####

def clean_variables(source, match, term):
### This function cleans the variables that were selected by the user, such as source, match and term. This function cleans variables that deal with the translator handling "search term option" ##
### This functions uses the variables selected to build SPARQL query that in turn retrieves information from PoolParty ###

	if source=="er":
	###	here user did not specified which project they want to search, in this case all project endpoints will be called ###
	## Build URLs used to call the right SPARQL endpoint. Here we call three endpoints for three projects: sectors, surveys and indicators ##
		URL1=[]
		URL2=[]
		URL3=[]
		baseURL1=URL1.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL1=URL1.append('Sectors')		
		sourceURL1=URL1.append('')
		sourceURL1=''.join(URL1)
		sourceURL1=str(sourceURL1)
		baseURL2=URL2.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL2=URL2.append('Surveys')		
		sourceURL2=URL2.append('')
		sourceURL2=''.join(URL2)
		sourceURL2=str(sourceURL2)
		baseURL3=URL3.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL3=URL3.append('Indicators')		
		sourceURL3=URL3.append('')
		sourceURL3=''.join(URL3)
		sourceURL3=str(sourceURL3)
	## Build SPARQL query 
		SPARQLQuery=[]
		start=SPARQLQuery.append('')
		prefix=SPARQLQuery.append('PREFIX skos:<http://www.w3.org/2004/02/skos/core#>')
		nextline=SPARQLQuery.append('\n')
	## Choose what you are looking for depending on user selection ##
		if match=='any':
	## Return all possible matches i.e. exact, close, broad and narrow ## 
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?exactMatch ?closeMatch ?broadMatch ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='er':
	## Return only concepts. This is a part of a "simple search" in the translator ## 	
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')					
		if match=='skos:exact':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?exactMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:close':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?closeMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:narrower':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:broader':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?broadMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
	## Join the strings together to make a query that can be send to endpoints ##		
		QUERY=''.join(SPARQLQuery)
		QUERY=str(QUERY)
	## Run SPARQLwrapper for all projects endpoints	
	## Run search in SPARQL endpoint 1	
		sparql1 = SPARQLWrapper(sourceURL1, returnFormat=XML)
		setQuery1=sparql1.setQuery(QUERY)
		ret10 = sparql1.query()
		DownloadUrl=ret10.geturl()
	## Run search in SPARQL endpoint 2	
		sparql2 = SPARQLWrapper(sourceURL2, returnFormat=XML)
		setQuery2=sparql2.setQuery(QUERY)
		ret20 = sparql2.query()
		DownloadUrl=ret20.geturl()
	## Run search in SPARQL endpoint 3	
		sparql3 = SPARQLWrapper(sourceURL3, returnFormat=XML)
		setQuery3=sparql3.setQuery(QUERY)
		ret30 = sparql3.query()
	## Ask the endpoint to return the link to downloadable XML file. This is the url that goes into the "Download XML/RDF" accordion in the results section ## 	
		DownloadUrl=ret30.geturl()
	## Use url to download results with <a href=url> in XML format in utf-8. This is here repeated three times for the three endpoints	 ##
		ret1 = sparql1.query()
		sparql1.setReturnFormat(XML)
		results1 = ret10.convert()
		ret11=results1.toxml('utf-8')

		ret2 = sparql2.query()
		sparql2.setReturnFormat(XML)
		results2 = ret20.convert()
		ret22=results2.toxml('utf-8')

		ret3 = sparql3.query()
		sparql3.setReturnFormat(XML)
		results3 = ret30.convert()
		ret33=results3.toxml('utf-8')

	## Clean up xml results ##
		root1=fromstring(ret11)
		root2=fromstring(ret22)
		root3=fromstring(ret33)
		ret300=[]
		results_clean=[]
		
	## 	xml.etree.ElementTree is used for this as it nicely parses information from the XML tree. This is done three times for three projects' endpoints ##
		for bindings in root1.iter('{http://www.w3.org/2005/sparql-results#}binding'):
			name=bindings.get('name')
			if name=='Concept':
				conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Original search term: ' + conceptURI)
			if name=='exactMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Exact match: ' + matchURI)
			if name=='closeMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Closer match: ' + matchURI)
			if name=='broadMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Broader match: ' + matchURI)
			if name=='narrowMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Narrower match: ' + matchURI)
		for bindings in root2.iter('{http://www.w3.org/2005/sparql-results#}binding'):
			name=bindings.get('name')
			if name=='Concept':
				conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Original search term: ' + conceptURI)
			if name=='exactMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Exact match: ' + matchURI)
			if name=='closeMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Closer match: ' + matchURI)
			if name=='broadMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Broader match: ' + matchURI)
			if name=='narrowMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Narrower match: ' + matchURI)
		for bindings in root3.iter('{http://www.w3.org/2005/sparql-results#}binding'):
			name=bindings.get('name')
			if name=='Concept':
				conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Original search term: ' + conceptURI)
			if name=='exactMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Exact match: ' + matchURI)
			if name=='closeMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Closer match: ' + matchURI)
			if name=='broadMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Broader match: ' + matchURI)
			if name=='narrowMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret300.append('Narrower match: ' + matchURI)
	## Append the parsed results from the XML to a file ##			
		results_clean_1 = ret300
		for i in results_clean_1:
			   results_clean.append(i)
	else:
	## Else here refers to: if you only have one project to search through, rather than all of them ##
	## Build URLs used to call the right SPARQL endpoint. ##
		URL=[]
		baseURL=URL.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL=URL.append(source)
		sourceURL=URL.append('')
		sourceURL=''.join(URL)
		sourceURL=str(sourceURL)
	## Source defines which endpoint to search through	
		match=match.lower()
	## Build SPARQL query
		SPARQLQuery=[]
		start=SPARQLQuery.append('')
		prefix=SPARQLQuery.append('PREFIX skos:<http://www.w3.org/2004/02/skos/core#>')
		nextline=SPARQLQuery.append('\n')
		if match=='any':
	## Match== any means retrieving all the matches for a given concept	
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?exactMatch ?closeMatch ?broadMatch ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='er':
	## Match==er means no matches need to be returned and the user only wants to use a simple search 	
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')		
	## The following matches are SKOS terms that signify matches ##				
		if match=='skos:exact':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?exactMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:close':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?closeMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:narrower':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:broader':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?prefLabel ?broadMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			ADDterm= SPARQLQuery.append("{?Concept skos:prefLabel ?prefLabel . FILTER (regex(str(?prefLabel), '"+ term +"', 'i')) }")
			nextline=SPARQLQuery.append("\n")
			SKOS=SPARQLQuery.append("{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
	## Combine the Query		
		QUERY=''.join(SPARQLQuery)
		QUERY=str(QUERY)
	## Run SPARQLwrapper and send the query	
		sparql = SPARQLWrapper(sourceURL, returnFormat=XML)
		setQuery=sparql.setQuery(QUERY)
		ret = sparql.query()
		DownloadUrl=ret.geturl()
	## Use url to download results with <a href=url> in XML format. This is the link that is used for "Download XML/RDF" accordion in the results sections. 	
		ret = sparql.query()
		sparql.setReturnFormat(XML)
		results = ret.convert()
		ret2=results.toxml('utf-8')
	## Clean up xml results. We use XML Element Tree. 
		root=fromstring(ret2)
		ret3=[]
		results_clean=[]
	## Search through nodes of the XML tree for...	
		for bindings in root.iter('{http://www.w3.org/2005/sparql-results#}binding'):
			name=bindings.get('name')
			if name=='Concept':
	## The name of the concept
				conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Search term: ' + conceptURI)
	## And all the other SKOS matches
			if name=='exactMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Exact match: ' + matchURI)
			if name=='closeMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Closer match: ' + matchURI)
			if name=='broadMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Broader match: ' + matchURI)
			if name=='narrowMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Narrower match: ' + matchURI)				
	## Append the results to the list
		results_clean_1 = ret3
		for i in results_clean_1:
			results_clean.append(i)
	
	return  results_clean, DownloadUrl
	
def translations(results_clean, source, starting_classification, destination_classification):	
 	##### This function chooses the right translations from the list of results #####
	##### This function has a few options. Depending on the user behaviour, the translations can either return direct translations, translations from one standards to all or translations from all standards to one ######

	translations=[]
	prev_line = next_line=''
	l = len(results_clean)
	for index, line in enumerate(results_clean):
	### User chose both standards to translate from and to 	###
		if starting_classification !='er' and destination_classification !='er':
			a=line.split('/')
			bb=line.split(":")
			bbb=bb[1]+':'+bb[2]
			if a[3]=='Surveys':
				b=a[4]
				b=b.split('_')
				d=b[2]
				if d=='u5':
					d='mics5'
				if a[0]=='Search term: http:':
					if a[3]==source:
						if starting_classification==b[2]:
  							next_line = results_clean[index + 1]
  							next_lineB=next_line.split('/')
  							next_lineB=next_lineB[4].split('_')
  							next_lineB=next_lineB[2]
 							if next_lineB==destination_classification:
 								translations.append(line)
 								translations.append(next_line)	
			else:
				if a[0]=='Search term: http:':
					if a[3]==source:
						if starting_classification==a[4]:
  							next_line = results_clean[index + 1]
  							next_lineB=next_line.split('/')
  							next_lineB=next_lineB[4]
 							if next_lineB==destination_classification:
 								translations.append(line)
 								translations.append(next_line)	
 	### User only chose the data standard to translate from and not where to translate to ###											
		if starting_classification !='er' and destination_classification =='er':
			a=line.split('/')
			bb=line.split(":")
			bbb=bb[1]+':'+bb[2]
			if a[3]=='Surveys':
				b=a[4]
				b=b.split('_')
				d=b[2]
				if d=='u5':
 					d='mics5'
 				if a[0]=='Search term: http:':
					if a[3]==source:
						if starting_classification==b[2]:
  							next_line = results_clean[index + 1]
							translations.append(line)
							translations.append(next_line)
			else:
				if a[0]=='Search term: http:':
					if a[3]==source:
						if starting_classification==a[4]:
  							next_line = results_clean[index + 1]
							translations.append(line)
							translations.append(next_line)		
	### User did not specify where to the translation should be done from but did specify which data standards it should translate to						
		if starting_classification =='er' and destination_classification !='er':
			a=line.split('/')
			bb=line.split(":")
			bbb=bb[1]+':'+bb[2]
			if a[3]=='Surveys':
 				b=a[4]
 				b=b.split('_')
 				d=b[2]
				if d=='u5':
					d='mics5'
				if a[0]=='Search term: http:':
					if a[3]==source:
						next_line = results_clean[index + 1]
						next_lineB=next_line.split('/')
						next_lineB=next_lineB[4]
						if next_lineB==destination_classification:
							translations.append(line)
							translations.append(next_line)	
			else:
				if a[0]=='Search term: http:':
					if a[3]==source:
						next_line = results_clean[index + 1]
						next_lineB=next_line.split('/')
						next_lineB=next_lineB[4]
						if next_lineB==destination_classification:
							translations.append(line)
							translations.append(next_line)			
	translations_final=[]
	### Append to lists
	for i in translations:
		translations_final.append(i)
	return translations_final
	
def clean_variables2(source, match, code):
### This function cleans the variables that were selected by the user, such as source, match and code. This function cleans variables that deal with the translator handling "search code" option ###
### This functions cleans the user input such as source, match and code and uses it to build SPARQL query that in turn retrieves information from PoolParty ###
	if source=="er": 
	### This route is used when user does not specify which project HSI would like to search. In this option all PoolParty projects' SPARQL endpoints are used ###
		URL4=[]
		URL5=[]
		URL6=[]
	### Build urls that call the endpoints x3 for three endpoints: sectors, surveys and indicators	
		baseURL4=URL4.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL4=URL4.append('Sectors')
		sourceURL4=URL4.append('')
		sourceURL4=''.join(URL4)
		sourceURL4=str(sourceURL4)
		baseURL5=URL5.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL5=URL5.append('Surveys')
		sourceURL5=URL5.append('')
		sourceURL5=''.join(URL5)
		sourceURL5=str(sourceURL5)
		baseURL6=URL6.append('http://joinedupdata.org/PoolParty/sparql/')
		sourceURL6=URL6.append('Indicators')
		sourceURL6=URL6.append('')
		sourceURL6=''.join(URL6)
		sourceURL6=str(sourceURL6)
	### Build SPARQL queries
		SPARQLQuery=[]
		start=SPARQLQuery.append('')
		prefix=SPARQLQuery.append('PREFIX skos:<http://www.w3.org/2004/02/skos/core#>')
		nextline=SPARQLQuery.append('\n')
		if match=='any':
	###	Search for all matches, such as exact, close, narrow or broad
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation ?exactMatch ?closeMatch ?broadMatch ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation), '"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='er':
	### Search only for a code and forget about the matches. This is for "simple search" option	
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')					
		if match=='skos:exact':
	### Individual calls for specific SKOS matches	###
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?exactMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:close':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?closeMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:narrower':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?narrowMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:broader':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?broadMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')	
	### Patch the query all together		
		QUERY=''.join(SPARQLQuery)
		QUERY=str(QUERY)
	### Run SPARQLwrapper for endpoint A
		sparql5 = SPARQLWrapper(sourceURL5, returnFormat=XML)
		setQuery5=sparql5.setQuery(QUERY)
		ret50 = sparql5.query()
		DownloadUrl=ret50.geturl()
	### Run SPARQLwrapper for endpoint B
		sparql6 = SPARQLWrapper(sourceURL6, returnFormat=XML)
		setQuery6=sparql6.setQuery(QUERY)
		ret60 = sparql6.query()
		DownloadUrl=ret60.geturl()
	### Run SPARQLwrapper for endpoint C
		sparql4 = SPARQLWrapper(sourceURL4, returnFormat=XML)
		setQuery4=sparql4.setQuery(QUERY)
		ret40= sparql4.query()
		DownloadUrl=ret40.geturl()
	### Use url to download results with <a href=url> in XML format	
		ret5= sparql5.query()
		sparql5.setReturnFormat(XML)
		results5 = ret5.convert()
		ret55=results5.toxml('utf-8')
		
		ret6= sparql6.query()
		sparql6.setReturnFormat(XML)
		results6 = ret6.convert()
		ret66=results6.toxml('utf-8')
		
		ret4= sparql4.query()
		sparql4.setReturnFormat(XML)
		results4= ret4.convert()
		ret44=results4.toxml('utf-8')
	### Cleaning up xml results, using XML Element Tree
		root5=fromstring(ret55)
		root6=fromstring(ret66)
		root4=fromstring(ret44)
		ret800=[]
		results_clean=[]
	### Iterate through tree branches x3 for three XML results trees returned by three endpoints.
	### Tree A
		for bindings in root5.iter('{http://www.w3.org/2005/sparql-results#}binding'):
			name=bindings.get('name')
	### Get concept name		
			if name=='Concept':
				conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Search term: ' + conceptURI)
	### Get the individual matches			
			if name=='exactMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Exact match: ' + matchURI)
			if name=='closeMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Closer match: ' + matchURI)
			if name=='broadMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Broader match: ' + matchURI)
			if name=='narrowMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Narrower match: ' + matchURI)
			if name=='notation':
				conceptNotation=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
				ret800.append('Search code: ' + conceptNotation)
			if name=='notation2':
				conceptNotation2=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
				ret800.append('Translated code: ' + conceptNotation2)	
	### Tree B				
		for bindings in root6.iter('{http://www.w3.org/2005/sparql-results#}binding'):
			name=bindings.get('name')
			if name=='Concept':
				conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('search term: ' + conceptURI)
			if name=='exactMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Exact match: ' + matchURI)
			if name=='closeMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Closer match: ' + matchURI)
			if name=='broadMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Broader match: ' + matchURI)
			if name=='narrowMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Narrower match: ' + matchURI)
			if name=='notation':
				conceptNotation=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
				ret800.append('Search code: ' + conceptNotation)
			if name=='notation2':
				conceptNotation2=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
				ret800.append('Translated code: ' + conceptNotation2)	
	### Tree C			
		for bindings in root4.iter('{http://www.w3.org/2005/sparql-results#}binding'):
			name=bindings.get('name')
			if name=='Concept':
				conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Search term: ' + conceptURI)
			if name=='exactMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Exact match: ' + matchURI)
			if name=='closeMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Closer match: ' + matchURI)
			if name=='broadMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Broader match: ' + matchURI)
			if name=='narrowMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret800.append('Narrower match: ' + matchURI)
			if name=='notation':
				conceptNotation=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
				ret800.append('Search code: ' + conceptNotation)
			if name=='notation2':
				conceptNotation2=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
				ret800.append('Translated code: ' + conceptNotation2)	
		results_clean_1 = ret800
		for i in results_clean_1:
			results_clean.append(i)
	else:
	### What we mean by "else" in here is that here we can look through individual project, specified by the user as "source"
		URL=[]
		baseURL=URL.append('http://joinedupdata.org/PoolParty/sparql/')
	### Create calling URLs based on the source project	
		sourceURL=URL.append(source)
		sourceURL=URL.append('')
		sourceURL=''.join(URL)
		sourceURL=str(sourceURL)
		match=match.lower()
	### Build SPARQL query 
		SPARQLQuery=[]
		start=SPARQLQuery.append('')
		prefix=SPARQLQuery.append('PREFIX skos:<http://www.w3.org/2004/02/skos/core#>')
		nextline=SPARQLQuery.append('\n')
		if match=='any':
	### Search for all SKOS matches
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation ?exactMatch ?closeMatch ?broadMatch ?narrowMatch')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation), '"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("OPTIONAL{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='er':
	### Search only for concepts -> "simple search" on the thesaurus	
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')					
		if match=='skos:exact':
	### Specific SKOS searches	
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?exactMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:exactMatch ?exactMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:close':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?closeMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:closeMatch ?closeMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:narrower':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?narrowMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:narrowMatch ?narrowMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')
		if match=='skos:broader':
			Select=SPARQLQuery.append('SELECT DISTINCT ?Concept ?notation  ?broadMatch ?notation2')
			nextline=SPARQLQuery.append('\n')
			WHERE=SPARQLQuery.append("WHERE{?Concept ?x skos:Concept")
			SKOS=SPARQLQuery.append("{?Concept skos:notation ?notation . Filter (regex(str(?notation),'"+ code +"', 'i'))}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?Concept skos:broadMatch ?broadMatch .}")
			nextline=SPARQLQuery.append('\n')
			SKOS=SPARQLQuery.append("{?exactMatch skos:notation ?notation2 .}")
			nextline=SPARQLQuery.append('\n')
			ORDER=SPARQLQuery.append("}ORDER BY ?prefLabel LIMIT 500 OFFSET 0")
			end=SPARQLQuery.append('')	
	###	Join the Query together
		QUERY=''.join(SPARQLQuery)
		QUERY=str(QUERY)
	### Run SPARQLwrapper
		sparql = SPARQLWrapper(sourceURL, returnFormat=XML)
		setQuery=sparql.setQuery(QUERY)
		ret = sparql.query()
		DownloadUrl=ret.geturl()
	### Use url to download results with <a href=url> in XML format. This is what goes into the "Download RDF/XML" accordion in the results sections. 
		ret = sparql.query()
		sparql.setReturnFormat(XML)
		results = ret.convert()
		ret2=results.toxml('utf-8')
	### Clean up xml results using XML Tree Element 
		root=fromstring(ret2)
		ret3=[]
		results_clean=[]
	### Iterate through the tree	
		for bindings in root.iter('{http://www.w3.org/2005/sparql-results#}binding'):
			name=bindings.get('name')
	### Find concept name 		
			if name=='Concept':
				conceptURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Search term: ' + conceptURI)
	### Find right matches			
			if name=='exactMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Exact match: ' + matchURI)
			if name=='closeMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Closer match: ' + matchURI)
			if name=='broadMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Broader match: ' + matchURI)
			if name=='narrowMatch':
				matchURI=bindings.find('{http://www.w3.org/2005/sparql-results#}uri').text
				ret3.append('Narrower match: ' + matchURI)
			if name=='notation':
				conceptNotation=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
				ret3.append('Search code: ' + conceptNotation)
			if name=='notation2':
				conceptNotation2=bindings.find('{http://www.w3.org/2005/sparql-results#}literal').text
				ret3.append('Translated code: ' + conceptNotation2)			
	### Append results to the list									
		results_clean_1 = ret3
		for i in results_clean_1:
		   results_clean.append(i)
		  
	return  results_clean, DownloadUrl
	
def translations2(results_clean, source, starting_classification, destination_classification):	
	prev_line = ''
	next_line=''
	l = len(results_clean)
	translations=[]
 	##### This function chooses the right translations from the list of results #####
	##### This function has a few options. Depending on the user behaviour, the translations can either return direct translations, translations from one standards to all or translations from all standards to one ######
	
 	notations=[]
 	prev_line=next_line=prev_prev_line=''
 	for index, line in enumerate(results_clean):
 		### User chose to specify both the starting data standard and the destination data standard ###
		if starting_classification !='er' and destination_classification !='er':
			a=line.split(':')
			b=line.split('/')
			if a[0]=='Search term':
				if b[3]=='Surveys':
					b=a[4]
					b=b.split('_')
					d=b[2]
					if d=='u5':
						d='mics5'
					if b[3]==source:
						if starting_classification==b[2] and index < (l-1):
							next_line = results_clean[index + 1]
							check_line=next_line.split(':')
							if check_line[0]=='Search term ' or check_line[0]=='Exact match' or check_line[0]=='Closer match' or check_line[0]=='Broader match' or check_line[0]=='Narrower match':
								next_lineB=next_line.split('/')
								next_lineC=next_lineB[4]
								if next_lineC==destination_classification:
									translations.append(line)
									translations.append(next_line)	
				else:
					if b[3]==source:
						b1=b[4]
						if starting_classification==b1 and index < (l-1):
							next_line = results_clean[index + 1]
							check_line=next_line.split(':')
							if check_line[0]=='Search term ' or check_line[0]=='Exact match' or check_line[0]=='Closer match' or check_line[0]=='Broader match' or check_line[0]=='Narrower match':
								next_lineB=next_line.split('/')
								next_lineC=next_lineB[4]
								if next_lineC==destination_classification:
									translations.append(line)
									translations.append(next_line)	
			if a[0]=='Search code' and index > 0:
				prev_prev_line=results_clean[index -2]
				search_term_standard=prev_prev_line.split('/')
				search_term_standard=search_term_standard[4]
				prev_line2=results_clean[index -1]
				prev_line=prev_line2.split(':')
				if starting_classification==search_term_standard:
					if prev_line[0]=='Exact match' or prev_line[0]=='Closer match' or prev_line[0]=='Broader match' or prev_line[0]=='Narrower match':
						notation1=line
						trans_term_standard=prev_line2.split('/')
						trans_term_standard=trans_term_standard[4]
						next_line=results_clean[index+1]
						next_lineB=next_line.split(":")
						next_lineC=next_line.split("/")
						next_lineB=next_lineB[0]
						if destination_classification==trans_term_standard:						
							if next_lineB=='Translated code'and index > 0:
								notation2=next_line
								translations.append(notation1)
								translations.append(notation2)																																			
 		### User chose to specify only the starting data standard and NOT the destination data standard ###
		if starting_classification !='er' and destination_classification =='er':
			a=line.split(':')
			b=line.split('/')
			if a[0]=='Search term':
				if b[3]=='Surveys':
					b=a[4]
					b=b.split('_')
					d=b[2]
					if d=='u5':
						d='mics5'
					if b[3]==source:
						if starting_classification==b[2] and index < (l-1):
							next_line = results_clean[index + 1]
							check_line=next_line.split(':')
							if check_line[0]=='Search term ' or check_line[0]=='Exact match' or check_line[0]=='Closer match' or check_line[0]=='Broader match' or check_line[0]=='Narrower match':
								next_lineB=next_line.split('/')
								next_lineC=next_lineB[4]
								translations.append(line)
								translations.append(next_line)	
				else:
					if b[3]==source:				
						b1=b[4]
						if starting_classification==b1 and index < (l-1):
							next_line = results_clean[index + 1]
							check_line=next_line.split(':')
							if check_line[0]=='Search term ' or check_line[0]=='Exact match' or check_line[0]=='Closer match' or check_line[0]=='Broader match' or check_line[0]=='Narrower match':
								next_lineB=next_line.split('/')
								next_lineC=next_lineB[4]
								translations.append(line)
								translations.append(next_line)		
			if a[0]=='Search code' and index > 0:
				prev_prev_line=results_clean[index -2]
				search_term_standard=prev_prev_line.split('/')
				search_term_standard=search_term_standard[4]
				prev_line2=results_clean[index -1]
				prev_line=prev_line2.split(':')
				if starting_classification==search_term_standard:
					if prev_line[0]=='Exact match' or prev_line[0]=='Closer match' or prev_line[0]=='Broader match' or prev_line[0]=='Narrower match':
						notation1=line
						trans_term_standard=prev_line2.split('/')
						trans_term_standard=trans_term_standard[4]
						next_line=results_clean[index+1]
						next_lineB=next_line.split(":")
						next_lineC=next_line.split("/")
						next_lineB=next_lineB[0]
						if destination_classification==trans_term_standard:						
							if next_lineB=='Translated code'and index > 0:
								notation2=next_line
								translations.append(notation1)
								translations.append(notation2)	
 		### User chose NOT to specify the starting data standard BUT chose the destination data standard ###
		if starting_classification =='er' and destination_classification !='er':
			a=line.split(':')
			b=line.split('/')
			if a[0]=='Search term':
				if b[3]=='Surveys':
					b=a[4]
					b=b.split('_')
					d=b[2]
					if d=='u5':
						d='mics5'
					if b[3]==source:
						if index < (l-1):
							next_line = results_clean[index + 1]
							check_line=next_line.split(':')
							if check_line[0]=='Search term ' or check_line[0]=='Exact match' or check_line[0]=='Closer match' or check_line[0]=='Broader match' or check_line[0]=='Narrower match':
								next_lineB=next_line.split('/')
								next_lineC=next_lineB[4]
								if next_lineC==destination_classification:
									translations.append(line)
									translations.append(next_line)	
				else:
					if b[3]==source:
						b1=b[4]
						if index < (l-1):
							next_line = results_clean[index + 1]
							check_line=next_line.split(':')
							if check_line[0]=='Search term ' or check_line[0]=='Exact match' or check_line[0]=='Closer match' or check_line[0]=='Broader match' or check_line[0]=='Narrower match':
								next_lineB=next_line.split('/')
								next_lineC=next_lineB[4]
								if next_lineC==destination_classification:
									translations.append(line)
									translations.append(next_line)	
			if a[0]=='Search code' and index > 0:
				prev_prev_line=results_clean[index -2]
				search_term_standard=prev_prev_line.split('/')
				search_term_standard=search_term_standard[4]
				prev_line2=results_clean[index -1]
				prev_line=prev_line2.split(':')
				if starting_classification==search_term_standard:
					if prev_line[0]=='Exact match' or prev_line[0]=='Closer match' or prev_line[0]=='Broader match' or prev_line[0]=='Narrower match':
						notation1=line
						trans_term_standard=prev_line2.split('/')
						trans_term_standard=trans_term_standard[4]
						next_line=results_clean[index+1]
						next_lineB=next_line.split(":")
						next_lineC=next_line.split("/")
						next_lineB=next_lineB[0]
						if destination_classification==trans_term_standard:						
							if next_lineB=='Translated code'and index > 0:
								notation2=next_line
								translations.append(notation1)
								translations.append(notation2)	
 ### Append the correct translations to a list
	translations_final=[]
	for i in translations:
		translations_final.append(i)
	return translations_final