from bs4 import BeautifulSoup
from difflib import unified_diff
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

def align_documents(doc1, doc2):

    # Get the common and new headings in both documents
    common_headings = list(set(doc1.keys()) & set(doc2.keys()))
    new_headings1 = list(set(doc1.keys()) - set(doc2.keys()))
    new_headings2 = list(set(doc2.keys()) - set(doc1.keys()))

    # Align the content associated with each common heading
    aligned_content = {}
    for heading in common_headings:
        content1 = doc1[heading]
        content2 = doc2[heading]
        
        # diff = list(unified_diff(content1.splitlines(), content2.splitlines()))
        dmp = dmp_module.diff_match_patch()
        dmp.Diff_Timeout = 2000
        diff = dmp.diff_main(content1,content2)
        dmp.diff_cleanupEfficiency(diff)
        x = dmp.diff_prettyHtml(diff)
        aligned_content[heading] = (content1, content2, x)

    # Extract the content associated with each new or modified heading
    new_content1 = {}
    for heading in new_headings1:
        new_content1[heading] = doc1[heading]

    new_content2 = {}
    for heading in new_headings2:
        new_content2[heading] = doc2[heading]

    # Align the changes and the content associated with the new or modified headings across both documents
    aligned_changes = {}
    for heading, (content1, content2, diff) in aligned_content.items():
        aligned_changes[heading] = (content1, content2, diff)

    for heading, content in new_content1.items():
        aligned_changes[heading] = (content, '', [])

    for heading, content in new_content2.items():
        aligned_changes[heading] = ('', content, [])

    return aligned_changes

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

# Parse the HTML document using BeautifulSoup
soup1 = BeautifulSoup(html1, 'html.parser')
# Find all headings and paragraphs in the document
headings = soup1.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
paragraphs = soup1.find_all('p')
# Create a dictionary to store the content under each heading
content1 = {}
# Loop through each heading and find all the paragraphs under it
for heading in headings:

    # Find the next heading in the document
    next_heading = heading.find_next(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if next_heading:
        # If there's a next heading, find all the paragraphs between the current heading and the next heading
        content1[heading.text] = [p.text for p in heading.find_next_siblings(['p']) if p.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) == heading and p.find_next(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) == next_heading]
    else:
        # If there's no next heading, find all the paragraphs between the current heading and the end of the document
        content1[heading.text] = [p.text for p in heading.find_next_siblings(['p']) if p.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) == heading]
# Add any paragraphs that come before the first heading to the content of the first heading
if headings:
    content1[headings[0].text] = [p.text for p in soup1.find_all('p') if p.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) == None]


soup2 = BeautifulSoup(html2, 'html.parser')
# Find all headings and paragraphs in the document
headings = soup2.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
paragraphs = soup2.find_all('p')
# Create a dictionary to store the content under each heading
content2 = {}
# Loop through each heading and find all the paragraphs under it
for heading in headings:

    print("HEADING: ", heading)
    # Find the next heading in the document
    next_heading = heading.find_next(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if next_heading:
        # If there's a next heading, find all the paragraphs between the current heading and the next heading
        content2[heading.text] = [p.text for p in heading.find_next_siblings(['p']) if p.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) == heading and p.find_next(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) == next_heading]
    else:
        # If there's no next heading, find all the paragraphs between the current heading and the end of the document
        content2[heading.text] = [p.text for p in heading.find_next_siblings(['p']) if p.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) == heading]
# Add any paragraphs that come before the first heading to the content of the first heading
if headings:
    content2[headings[0].text] = [p.text for p in soup2.find_all('p') if p.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) == None]

aligned_changes= align_documents(content1,content2)


with open('aligned_changes2.html', 'w', encoding='utf-8') as f:
    f.write('<html>\n<head>\n<title>Aligned Changes</title>\n<style>\n.green {color: green;}\n.red {color: red;}\n</style>\n</head>\n<body>\n')
    for heading, content1, content2, diff in aligned_changes:
        f.write(f'<h2>{heading}</h2>\n')
        f.write('<table border="1">\n<tr>\n<td>'+doc_number1+'</td>\n<td>'+doc_number2+'</td>\n</tr>\n')
        for line in diff:
            if line.startswith(' '):
                f.write(f'<tr><td>{line[2:]}</td><td>{line[1:]}</td></tr>\n')
            elif line.startswith('-'):
                f.write(f'<tr><td class="red">{line[1:]}</td><td></td></tr>\n')
            elif line.startswith('+'):
                f.write(f'<tr><td></td><td class="green">{line[1:]}</td></tr>\n')
        f.write('</table>\n')
    f.write('</body>\n</html>')