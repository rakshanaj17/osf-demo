# importing re module
import re
import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import difflib

from difflib import SequenceMatcher
from termcolor import colored

def diff_strings(text1, text2):

    matcher = SequenceMatcher(None, text1, text2)

# Get the list of opcodes
    opcodes = matcher.get_opcodes()
    # print(opcodes)
    op=''

    # Iterate over the opcodes and print the differences
    for opcode in opcodes:
        tag, i1, i2, j1, j2 = opcode
        if tag == 'equal':
            op+=text1[i1:i2]
        if tag == 'replace':
            op+=colored(text1[i1:i2],'red')
            # print('Replace from %d to %d in text1 with %s' % (i1, i2, text2[j1:j2]))
            op+=colored(text2[j1:j2],'green')
        elif tag == 'delete':
            # print('Delete from %d to %d in text1' % (i1, i2))
            op+=colored(text1[i1:i2],'red')
        elif tag == 'insert':
            # print('Insert %s at %d in text1' % (text2[j1:j2], i1))
            op+=colored(text2[j1:j2],'green')

    return op


def get_string_changes(s1, s2):
    ans = []
    
    if type(s1) == str and type(s2) == str:
        n = 3
        s1 = [" ".join(s1.lower().split()[i:i+n]) for i in range(0, len(s1.split()), n)]
        s2 = [" ".join(s2.lower().split()[i:i+n]) for i in range(0, len(s2.split()), n)]

    diff = difflib.unified_diff(s1, s2, fromfile='Text 1', tofile='Text 2', lineterm='')
    for idx, line in enumerate(diff):
        if idx<3: continue
        ans.append(line)
            
    return ans

def getChanges(a,b):
    url = "https://text-diff.p.rapidapi.com/diff"

    payload = {
        "text1": a,
        "text2": b
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "25711ed42fmsh972b785ee849dc3p1f1799jsnfb9f2fb98f69",
        "X-RapidAPI-Host": "text-diff.p.rapidapi.com"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    return (response.text)

async def main():

    op=[]
    doc_number1="2022-15372"
    doc_number2="2022-23918"
    
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

full_text_xml_url1,full_text_xml_url2=asyncio.run(main())

xml_data1 = requests.get(full_text_xml_url1)
# print(xml_data1.text[:500])
soup1=BeautifulSoup(xml_data1.text,'html.parser')  

xml_data2 = requests.get(full_text_xml_url2)
# print(xml_data2.text[:500])
soup2=BeautifulSoup(xml_data2.text,'html.parser')  


doc1_heading=soup1.find('h3', id='h-204')
doc1_text=soup1.find('p', id='p-1267').text+soup1.find('p', id='p-1268').text+soup1.find('p', id='p-1269').text

doc2_heading=soup2.find('h3', id='h-257')
doc2_text=soup2.find('p', id='p-2148').text+soup2.find('p', id='p-2149').text+soup2.find('p', id='p-2150').text+soup2.find('p', id='p-2151').text+soup2.find('p', id='p-2152').text
  
# # printing result
# print("extracted doc1_heading : " + str(doc1_heading.text))
# print("extracted doc1_text : " + str(doc1_text))
# print("extracted doc2_heading : " + str(doc2_heading.text))
# print("extracted doc1_text : " + str(doc2_text))

a=doc1_text
b=doc2_text

x=diff_strings(a,b)

print(str(doc1_heading.text))
print(x)

# with open('changes1.txt', 'w') as f:
#     f.write(x)