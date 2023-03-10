from bs4 import BeautifulSoup
from difflib import unified_diff
from difflib import context_diff
import diff_match_patch as dmp_module
import re
import requests
import aiohttp
import asyncio
import difflib

from difflib import SequenceMatcher
from termcolor import colored

doc_number1="2022-15372"
doc_number2="2022-23918"

def get_content(heading, all_headings, all_content):
    content = []
    h=""
    for element in all_headings:
        if heading in element:
             h = element
    if(h!=""):
        index = all_headings.index(h)
        content.append((heading, content1[index]))
     

async def main():

    op=[]
    
    
    url1 = "https://www.federalregister.gov/api/v1/documents/"+doc_number1+".json?fields[]=body_html_url"
    url2 = "https://www.federalregister.gov/api/v1/documents/"+doc_number2+".json?fields[]=body_html_url"
    async with aiohttp.ClientSession() as session:
            async with session.get(url1) as resp:
                response = await resp.json()
                op.append(response['body_html_url'])

    async with aiohttp.ClientSession() as session:
            async with session.get(url2) as resp:
                response = await resp.json()
                op.append(response['body_html_url'])
    return op

html1URL,html2URL = asyncio.run(main())

html1 = requests.get(html1URL).text
html2 = requests.get(html2URL).text

# with open('page1.html') as f1, open('page2.html') as f2:
#     html1 = f1.read()
#     html2 = f2.read()

# Parse the HTML files
soup1 = BeautifulSoup(html1, 'html.parser')
soup2 = BeautifulSoup(html2, 'html.parser')

##########################################

# Extract the headings and content from both documents
headings1 = [h.text for h in soup1.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
content1 = [c for c in soup1.find_all(['p', 'ul', 'ol'])]
headings2 = [h.text for h in soup2.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
content2 = [c for c in soup2.find_all(['p', 'ul', 'ol'])]

common_headings = [h for h in headings1 if h in headings2]
new_headings1 = [h for h in headings1 if h not in headings2]
new_headings2 = [h for h in headings2 if h not in headings1]


# heading="Direct Supervision of Certain Cardiac and Pulmonary Rehabilitation Services by Interactive Communications Technology"

# heading = "Supervision by Nonphysician Practitioners of Hospital and CAH Diagnostic Services Furnished to Outpatients"

heading ="SUPPLEMENTARY MEDICAL INSURANCE (SMI) BENEFITS"

# heading='Proposed Language Changes'

# heading="Request for Public Comment"

# heading = "Therapeutic outpatient hospital or CAH services"
doc1_text=""

doc2_text=""

print(heading)

for element in common_headings:
    print(element)
    if heading in element:
        print(f"{heading} is a substring of {element} in common_headings")

        head1 = soup1.find(['h1','h2', 'h3'],string=element)
        head2 = soup2.find(['h1','h2', 'h3'],string=element)

        # Find all content after Heading 1 until the next heading
        content = head1.find_next_siblings(['p','h2', 'h3','h4','h5','h6'])
        for tag in content:
            if tag.name.startswith('h3'):
                break  # Stop if a new heading is encountered
            doc1_text+=(tag.get_text())

        # Find all content after Heading 1 until the next heading
        content = head2.find_next_siblings(['p','h2','h3','h4','h5','h6'])
        for tag in content:
            if tag.name.startswith('h3'):
                break  # Stop if a new heading is encountered
            doc2_text+=(tag.get_text())

for element in new_headings1:
     if heading in element:
        #   do it
        print(f"{heading} is a substring of {element} in 1st doc only")
        head1 = soup1.find(['h1','h2', 'h3'],string=element)

        # Find all content after Heading 1 until the next heading
        content = head1.find_next_siblings(['p','h2', 'h3','h4','h5','h6'])
        for tag in content:
            if tag.name.startswith('h'):
                break  # Stop if a new heading is encountered
            doc1_text+=(tag.get_text())


for element in new_headings2:
     if heading in element:
        #   do it
        print(f"{heading} is a substring of {element} in 2nd doc only")

        head2 = soup2.find(['h1','h2', 'h3'],string=element)

        # Find all content after Heading 1 until the next heading
        content = head2.find_next_siblings(['p','h2', 'h3','h4','h5','h6'])
        for tag in content:
            if tag.name.startswith('h'):
                break  # Stop if a new heading is encountered
            doc2_text+=(tag.get_text())


changes=[]

dmp = dmp_module.diff_match_patch()
dmp.Diff_Timeout = 2000
diff = dmp.diff_main(doc1_text,doc2_text)
# print("DIFF",diff)
# dmp.diff_cleanupSemantic(diff)
dmp.diff_cleanupEfficiency(diff)

x = dmp.diff_prettyHtml(diff)
print('###########################################################')

print(x)
print('###########################################################')


# print(doc1_text)

# print(doc2_text)




with open('xdbgs.html', 'w', encoding='utf-8') as f:
    # f.write(x)
    f.write('<html>\n<head>\n<link rel="stylesheet" href="styles.css">\n<title>'+"res3"+'</title>\n</head>\n<body>\n')
    f.write(f'<h2>{heading}</h2>\n')
    f.write('<div class="para changes">\n')
    for line in diff:
        print(line)
        if line[0]==0:
            f.write(f'<p>{line[1]}</p>')
        elif line[0]==-1:
            f.write(f'\n<p class="red">{line[1]}</p>')
        elif line[0]==1:
            f.write(f'\n<p class="green">{line[1]}</p>')
    f.write('</div>\n')
    f.write('</body>\n</html>')

