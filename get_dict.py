from bs4 import BeautifulSoup
from difflib import unified_diff
import diff_match_patch as dmp_module

import re
import requests
import aiohttp
import asyncio
import difflib

def align_documents(doc1, doc2):

    # Get the common and new headings in both documents
    common_headings = list(set(doc1.keys()) & set(doc2.keys()))
    new_headings1 = list(set(doc1.keys()) - set(doc2.keys()))
    new_headings2 = list(set(doc2.keys()) - set(doc1.keys()))

    # Align the content associated with each common heading
    aligned_content = {}
    for heading in common_headings:
        print(heading)
        content1 = doc1[heading]
        content2 = doc2[heading]
        dmp = dmp_module.diff_match_patch()
        # dmp.Diff_Timeout = 2000
        diff = dmp.diff_main(content1,content2)
        dmp.diff_cleanupEfficiency(diff)
        x = dmp.diff_prettyHtml(diff)
        aligned_content[heading] = (content1, content2, diff)
        print()


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

dic1 = parse_html_to_dict("2022-15372")

dic2 = parse_html_to_dict("2022-23918")

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

# print(result_dic1,result_dic2)

aligned_changes = (align_documents(result_dic1,result_dic2))
print('checkpoint 3')

# print(aligned_changes)
with open('UGH.html', 'w', encoding='utf-8') as f:
    f.write('<html>\n<head>\n<link rel="stylesheet" href="styles.css">\n<title>'+"My Dictionary"+'</title>\n</head>\n<body>\n')
    f.write('<h2>Changes</h2>\n')
    f.write('<div class="dictionary">\n')
    for key, value in aligned_changes.items():
        f.write(f'<h3><span class="key">{key} </span></h3>')
        if value[2]:
            f.write('<span class="para changes">\n')
            for line in value[2]:
                if line[0]==0:
                    f.write(f'<p>{line[1]}</p>')
                elif line[0]==-1:
                    f.write(f'\n<p class="red">{line[1]}</p>')
                elif line[0]==1:
                    f.write(f'\n<p class="green">{line[1]}</p>')
            f.write('</span>')
    f.write('</div>\n</body>\n</html>')


      
    #   for table

# with open('UGHttable.html', 'w', encoding='utf-8') as f:
#     f.write('<html>\n<head>\n<link rel="stylesheet" href="styles.css">\n<title>'+"My Dictionary"+'</title>\n</head>\n<body>\n')
#     f.write('<h2>Changes</h2>\n')
#     f.write('<div class="dictionary">\n')
#     for key, value in aligned_changes.items():
#         f.write(f'<h3><span class="key">{key} </span></h3>')
#         if value[2]:
#             f.write('<table border="1">\n<tr>\n<td>'+'old'+'</td>\n<td>'+'new'+'</td>\n</tr>\n')
#             for line in value[2]:
#                 if line[0]==0:
#                     f.write(f'<tr><td>{line[1]}</td><td>{line[1]}</td></tr>\n')
#                 elif line[0]==-1:
#                     f.write(f'<tr><td class="red">{line[1]}</td><td></td></tr>\n')
#                 elif line[0]==1:
#                     f.write(f'<tr><td></td><td class="green">{line[1]}</td></tr>\n')
#             f.write('</table>\n')
#     f.write('</div>\n</body>\n</html>')