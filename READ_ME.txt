Hi Epic Allan, 
Thank you for making the developers dreams come true.
The files you have now with you show are written in html, java and python.
Please do ask me if you have any problems. 

The jobs:

1) Make sure that the files sit well with the rest of the PPT package.
2) Adjust css accordingly to make sure that it does not mess the layout of the original thesaurus.
For example the page like this one: http://joinedupdata.org/Indicators/mdg/achieve-universal-primary-education_mdg.html.
3) The functions for the "translator"(translator2.html) are written in Python and they use a package called SPARQLWrapper (https://rdflib.github.io/sparqlwrapper/), which I think must be incorporated into our server.
4) The APIcall.txt gives you API calls that must be send to the server to get information for filling the lists on projects_page(1-4).html and data_standards_index.html.
Use the "AltLabel" to display names, use a href="" to make sure that they link to the right page in the thesaurus.
For example: AltLabel: "Achieve universal primary education" a href="http://joinedupdata.org/Indicators/mdg/achieve-universal-primary-education_mdg.html".
5) For the translator2.html the additional information currently displayed as 1,2,3,4 in "advanced filters".
Such as: "1 You can discover different relationships to your search term/code. You can choose to view all the relationships to your search term/code or a specific one. We use Simple Knowledge Organisation System (SKOS) to map data standards; a practical example of mapping approach can be found here." 
Should be only visible when the user hovers over the "What translation would you like to be returned?".
It should look something like this: http://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_popup
6) Currently the left handside menu displays hyperlinks as: http://127.0.0.1:5000/projects_page4.
The "127.0.0.1:5000" must be changed accordingly everywhere in the hyperlinked text and point to the "joinedupdata.org" once you implement it.
7) I am sure that some of the formatting of the css needs a little bit of tweaking to make sure that for example if you make the window smaller,
the left-hand side menu does not cover the main window.
Or that the bottom and top panels (the black stripes at the top and bottom are always kept in their place).
8) If you have time: div="sidebar-left" has a link to "Contact us" at the moment it point to juds.joinedupdata.org/about.
Can we have it point to juds.joinedupdata.org/about#contact?
I have some problems to point that to that specific place (probably should use anchor on the wordpress).
9) At the risk of being patronising (which I don't want to be):
check that the files are compatible with the new version of the PPT (5.5 which is available for download now) and
make sure that the old login page custumisation for the PPT (that is not currently implemented) is also compatible with the new PPT version on your dev server. 
10) Simple search window is the same search window that is a built-in feature on top of: http://joinedupdata.org/Indicators.html.
If you wish/have time you can plug that into the API to get all the concepts from the thesaurus repository using API calls in APIcall.txt 

Additional info:
1) All the pictures that I used are in the "static" folder.
2) The .js code is in the "static" folder. The .js code was used for the expandable lists.
3) Main.3.py calls Flask and generates the html pages on your local host: http://127.0.0.1:5000.
4) MainFunctions3.py are used for the translator2.html, the functions are commented to tell you what each part of the code does. 
5) All the screenshots of the pages can be found in: the "Screenshots" folder.

Timeline: 
This should be done by the 27th of October however it might be pushed to the 3rd&4th of November as DDW has some other work that needs to be done asap for another project. 
At the same time as we implement the changes, DDW will have to upgrade to the new version of the PPT (5.5), upload the old login page customisation and install SPARQLwrapper.
