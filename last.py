from bs4 import BeautifulSoup
from difflib import unified_diff
import diff_match_patch as dmp_module

import re
import requests
import aiohttp
import asyncio
import difflib


async def main(doc_number):

    url1 = "https://www.federalregister.gov/api/v1/documents/"+doc_number+".json?fields[]=body_html_url"
    async with aiohttp.ClientSession() as session:
            async with session.get(url1) as resp:
                response = await resp.json()
                return response['body_html_url']


def parse_html_to_dict(doc_num):

        html1URL = asyncio.run(main(doc_num))

        html1 = requests.get(html1URL).text

        soup = BeautifulSoup(html1, 'html.parser')

        # Find all the headings and paragraphs
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraphs = soup.find_all('p')

        # Initialize the dictionary
        html_dict = {}

        # Loop through the headings and paragraphs
        for heading in headings:
            # Get the heading text
            heading_text = heading.text.strip()

            # Find all the paragraphs under this heading
            current_node = heading.next_sibling
            content = []
            while current_node and current_node.name != heading.name:
                if current_node.name == 'p':
                    content.append(current_node.text.strip())
                current_node = current_node.next_sibling

            # Add the heading and its associated content to the dictionary
            html_dict[heading_text] = content

        return html_dict

# 2022-15372
# 2022-23918

docNumber1 = "2022-15372"
docNumber2 = "2022-23918"

dic1 = parse_html_to_dict(docNumber1)

dic2 = parse_html_to_dict(docNumber2)

print('checkpoint 1')
# dic1={'A':['a','a','a'], 'B':['b','b']}

# dic2={'A':['a','a','c'], 'B':['1','b']}

result_dic1 = {}

for key, value in dic1.items():
    result_dic1[key] = ' '.join(value)

result_dic2 = {}

for key, value in dic2.items():
    result_dic2[key] = ' '.join(value)
print('checkpoint 2')

headings1 = list(result_dic1.keys())
content1 = list(result_dic1.values())

headings2 = list(result_dic2.keys())
content2 = list(result_dic2.values())

common_headings = [h for h in headings1 if h in headings2]
new_headings1 = [h for h in headings1 if h not in headings2]
new_headings2 = [h for h in headings2 if h not in headings1]

changes = []
for heading in common_headings:
    index1 = headings1.index(heading)
    index2 = headings2.index(heading)
     # If content is a list, concatenate the text of all paragraphs
    content1_text = content1[index1].strip()
    content2_text = content2[index2].strip()

    diff = list(unified_diff(content1[index1].splitlines(), content2[index2].splitlines()))
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
with open(docNumber1+'_'+docNumber2+'.html', 'w', encoding='utf-8') as f:
    f.write('<html>\n<head>\n<title>Aligned Changes</title>\n<style>\n.green {color: green;}\n.red {color: red;}\n</style>\n</head>\n<body>\n')
    f.write('<h1>Comparing '+docNumber1+' and '+docNumber2+'</h1>')
    for heading, content1, content2, diff in aligned_changes:
        f.write(f'<h2>{heading}</h2>\n')
        f.write('<table border="1">\n<tr>\n<td>'+docNumber1+'</td>\n<td>'+docNumber2+'</td>\n</tr>\n')
        for line in diff:
            if line.startswith(' '):
                f.write(f'<tr><td>{line[2:]}</td><td>{line[1:]}</td></tr>\n')
            elif line.startswith('-'):
                f.write(f'<tr><td class="red">{line[1:]}</td><td></td></tr>\n')
            elif line.startswith('+'):
                f.write(f'<tr><td></td><td class="green">{line[1:]}</td></tr>\n')
        f.write('</table>\n')
    f.write('</body>\n</html>')
