from bs4 import BeautifulSoup
from difflib import unified_diff

import re
import requests
import aiohttp
import asyncio
import difflib

from difflib import SequenceMatcher
from termcolor import colored

doc_number1="2022-15372"
doc_number2="2022-23918"

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

# Extract the headings and content from both documents
headings1 = [h.text for h in soup1.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
content1 = [c for c in soup1.find_all(['p', 'ul', 'ol'])]
headings2 = [h.text for h in soup2.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
content2 = [c for c in soup2.find_all(['p', 'ul', 'ol'])]

# Compare the headings in both documents
common_headings = [h for h in headings1 if h in headings2]
new_headings1 = [h for h in headings1 if h not in headings2]
new_headings2 = [h for h in headings2 if h not in headings1]

# print("common_headings : ",common_headings)
# print("new_headings1 : ",new_headings1)
# print("new_headings2 : ",new_headings2)

# print("content1: ",content1)
print('################################################################')
# print("content2: ",content2)

# IDEA? use table of contents to create common headings array?

# Extract the content associated with each common heading
changes = []
for heading in common_headings:
    index1 = headings1.index(heading)
    index2 = headings2.index(heading)
     # If content is a list, concatenate the text of all paragraphs
    if isinstance(content1[index1], list):
        content1_text = '\n'.join([c.text.strip() for c in content1[index1]])
    else:
        content1_text = content1[index1].text.strip()
    if isinstance(content2[index2], list):
        content2_text = '\n'.join([c.text.strip() for c in content2[index2]])
    else:
        content2_text = content2[index2].text.strip()

    diff = list(unified_diff(content1[index1].text.splitlines(), content2[index2].text.splitlines()))
    if diff:
        changes.append((heading, diff))


# Extract the content associated with each new or modified heading
new_content1 = []
for heading in new_headings1:
    index = headings1.index(heading)
    new_content1.append((heading, content1[index]))

new_content2 = []
for heading in new_headings2:
    index = headings2.index(heading)
    new_content2.append((heading, content2[index]))


# Align the changes and the content associated with the new or modified headings across both documents
aligned_changes = []
for heading, diff in changes:
    index1 = headings1.index(heading)
    index2 = headings2.index(heading)
    aligned_changes.append((heading, content1[index1], content2[index2], diff))

for heading, content in new_content1:
    aligned_changes.append((heading, content, BeautifulSoup('', 'html.parser'), []))

for heading, content in new_content2:
    aligned_changes.append((heading, BeautifulSoup('', 'html.parser'), content, []))


# print("aligned_changes : ",aligned_changes)

# Write the aligned changes to an HTML file
with open('aligned_changes_old.html', 'w', encoding='utf-8') as f:
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
