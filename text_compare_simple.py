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

doc_number1 = "2022-15372"
doc_number2 = "2022-23918"


def get_content(heading, all_headings, all_content):
    content = []
    h = ""
    for element in all_headings:
        if heading in element:
            h = element
    if (h != ""):
        index = all_headings.index(h)
        content.append((heading, content1[index]))


async def main():

    op = []

    url1 = "https://www.federalregister.gov/api/v1/documents/" + \
        doc_number1+".json?fields[]=body_html_url"
    url2 = "https://www.federalregister.gov/api/v1/documents/" + \
        doc_number2+".json?fields[]=body_html_url"
    async with aiohttp.ClientSession() as session:
        async with session.get(url1) as resp:
            response = await resp.json()
            op.append(response['body_html_url'])

    async with aiohttp.ClientSession() as session:
        async with session.get(url2) as resp:
            response = await resp.json()
            op.append(response['body_html_url'])
    return op

# html1URL,html2URL = asyncio.run(main())

# html1 = requests.get(html1URL).text
# html2 = requests.get(html2URL).text

# # with open('page1.html') as f1, open('page2.html') as f2:
# #     html1 = f1.read()
# #     html2 = f2.read()

# # Parse the HTML files
# soup1 = BeautifulSoup(html1, 'html.parser')
# soup2 = BeautifulSoup(html2, 'html.parser')

# ##########################################

# # Extract the headings and content from both documents
# headings1 = [h.text for h in soup1.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
# content1 = [c for c in soup1.find_all(['p', 'ul', 'ol'])]
# headings2 = [h.text for h in soup2.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
# content2 = [c for c in soup2.find_all(['p', 'ul', 'ol'])]

# common_headings = [h for h in headings1 if h in headings2]
# new_headings1 = [h for h in headings1 if h not in headings2]
# new_headings2 = [h for h in headings2 if h not in headings1]


# # heading="Direct Supervision of Certain Cardiac and Pulmonary Rehabilitation Services by Interactive Communications Technology"

# # heading = "Supervision by Nonphysician Practitioners of Hospital and CAH Diagnostic Services Furnished to Outpatients"

# # heading ="SUPPLEMENTARY MEDICAL INSURANCE (SMI) BENEFITS"

# # heading='Proposed Language Changes'

# # heading="Request for Public Comment"

# # heading = "Therapeutic outpatient hospital or CAH services"

# # March 3
# heading = "Summary of the Major Provisions"

# doc1_text=""

# doc2_text=""

# print(heading)

# for element in common_headings:
#     print(element)
#     if heading in element:
#         print(f"{heading} is a substring of {element} in common_headings")

#         head1 = soup1.find(['h1','h2', 'h3','h4'],string=element)
#         head2 = soup2.find(['h1','h2', 'h3','h4'],string=element)

#         # Find all content after Heading 1 until the next heading
#         content = head1.find_next_siblings(['p','h2', 'h3','h4','h5','h6'])
#         for tag in content:
#             if tag.name.startswith('h3'):
#                 break  # Stop if a new heading is encountered
#             doc1_text+=(tag.get_text())

#         # Find all content after Heading 1 until the next heading
#         content = head2.find_next_siblings(['p','h2','h3','h4','h5','h6'])
#         for tag in content:
#             if tag.name.startswith('h3'):
#                 break  # Stop if a new heading is encountered
#             doc2_text+=(tag.get_text())

# for element in new_headings1:
#      if heading in element:
#         #   do it
#         print(f"{heading} is a substring of {element} in 1st doc only")
#         head1 = soup1.find(['h1','h2', 'h3'],string=element)

#         # Find all content after Heading 1 until the next heading
#         content = head1.find_next_siblings(['p','h2', 'h3','h4','h5','h6'])
#         for tag in content:
#             if tag.name.startswith('h'):
#                 break  # Stop if a new heading is encountered
#             doc1_text+=(tag.get_text())


# for element in new_headings2:
#      if heading in element:
#         #   do it
#         print(f"{heading} is a substring of {element} in 2nd doc only")

#         head2 = soup2.find(['h1','h2', 'h3'],string=element)

#         # Find all content after Heading 1 until the next heading
#         content = head2.find_next_siblings(['p','h2', 'h3','h4','h5','h6'])
#         for tag in content:
#             if tag.name.startswith('h'):
#                 break  # Stop if a new heading is encountered
#             doc2_text+=(tag.get_text())


changes = []

doc1_text = "A. Background Established in rulemaking as part of the initial implementation of the OPPS, the inpatient only (IPO) list identifies services for which Medicare will only make payment when the services are furnished in the inpatient hospital setting because of the nature of the procedure, the underlying physical condition of the patient, or the need for at least 24 hours of postoperative recovery time or monitoring before the patient can be safely discharged (70 FR 68695). The IPO list was created based on the premise (rooted in the practice of medicine at that time), that Medicare should not pay for procedures furnished as outpatient services that are performed on an inpatient basis virtually all of the time for the Medicare population, either because of the invasive nature of the procedures, the need for postoperative care, or the underlying physical condition of the patient who would require such surgery, because performing these procedures on an outpatient basis would not be safe or appropriate, and therefore not reasonable and necessary under Medicare rules (63 FR 47571). Services included on the IPO list were those determined to require inpatient care, such as those that are highly invasive, result in major blood loss or temporary deficits of organ systems (such as neurological impairment or respiratory insufficiency), or otherwise require intensive or extensive postoperative care (65 FR 67826). There are some services designated as inpatient only that, given their clinical intensity, would not be expected to be performed in the hospital outpatient setting. For example, we have traditionally considered certain surgically invasive procedures on the brain, heart, and abdomen, such as craniotomies, coronary-artery bypass grafting, and laparotomies, to require inpatient care (65 FR 18456). Designation of a service as inpatient-only does not preclude the service from being furnished in a hospital outpatient setting, but means that Medicare will not make payment for the service if it is furnished to a Medicare beneficiary in the hospital outpatient setting (65 FR 18443). Conversely, the absence of a procedure from the list should not be interpreted as identifying those procedures as appropriately performed only in the hospital outpatient setting (70 FR 68696) As part of the annual update process, we have historically worked with interested stakeholders, including professional societies, hospitals, surgeons, hospital associations, and beneficiary advocacy groups, to evaluate the IPO list and to determine whether services should be added to or removed from the list. Stakeholders were encouraged to request reviews for a particular code or group of codes; and we have asked that their requests include evidence that demonstrates that the procedure was performed on an outpatient basis in a safe and appropriate manner in a variety of different types of hospitals—including but not limited to—operative reports of actual cases, peer-reviewed medical literature, community medical standards and practice, physician comments, outcome data, and post-procedure care data (67 FR 66740) Prior to CY 2021, we traditionally used five criteria to determine whether a procedure should be removed from the IPO list (65 FR 18455). As noted in the CY 2012 OPPS/ASC final rule with comment period (76 FR 74353), we assessed whether a procedure or service met these criteria to determine whether or not it should be removed from the IPO list and assigned to an APC group for payment under the OPPS when provided in the hospital outpatient setting. We have explained that a procedure is not required to meet all of the established criteria to be removed from the IPO list. The criteria for assessing procedures for removal from the IPO list prior to CY 2021 are the following Most outpatient departments are equipped to provide the services to the Medicare population The simplest procedure described by the code may be furnished in most outpatient departments The procedure is related to codes that we have already removed from the IPO list A determination is made that the procedure is being furnished in numerous hospitals on an outpatient basis A determination is made that the procedure can be appropriately and safely furnished in an ASC and is on the list of approved ASC services or has been proposed by us for addition to the ASC list In the past, we have requested that stakeholders submit corresponding evidence in support of their claims that a code or group of codes met the longstanding criteria for removal from the IPO list and was safe to perform on the Medicare population in the hospital outpatient setting—including, but not limited to case reports, operative reports of actual cases, peer-reviewed medical literature, medical professional analysis, clinical criteria sets, and patient selection protocols. Our clinicians thoroughly reviewed all information submitted within the context of the established criteria and if, following this review, we determined that there was sufficient evidence to confirm that the code could be safely and appropriately performed on an outpatient basis, we assigned the service to an APC and included it as a payable procedure under OPPS (67 FR 66740) We stated in prior rulemaking that, over time, given advances in technology and surgical technique, we would continue to evaluate services to determine whether they should be removed from the IPO list. Our goal is to ensure that inpatient only designations are consistent with current standards of practice. We have asserted in prior rulemaking that, insofar as advances in medical practice mitigate concerns about these procedures being performed on an outpatient basis, we would be prepared to remove procedures from the IPO list and provide for payment for them under the OPPS (65 FR 18443). Prior to CY 2021, changes to the IPO list have been gradual. Further, CMS has at times had to reclassify codes as inpatient only services with the emergence of new information We refer readers to the CY 2012 OPPS/ASC final rule with comment period (76 FR 74352 through 74353) for a full discussion of our historic policies for identifying services that are typically provided only in an inpatient setting and, therefore, that will not be paid by Medicare under the OPPS, as well as the criteria we have used to review the IPO list to determine whether or not any services should be removed In the CY 2021 OPPS/ASC final rule with comment period (85 FR 86084 through 86088), we significantly adjusted our approach to the IPO list. As we stated in that final rule, we no longer saw the need for CMS to restrict payment for certain procedures by maintaining the IPO list to identify services that require inpatient care. In that final rule, we acknowledged the seriousness of the concerns regarding patient safety and quality of care that various stakeholders expressed regarding removing procedures from the IPO list or eliminating the IPO list altogether. But we stated that we believed that the developments in surgical technique and technological advances in the practice of medicine, as well as various safeguards, including, but not limited to, physician clinical judgment, state and local regulations, accreditation requirements, medical malpractice laws, hospital conditions of participation, CMS quality and monitoring initiatives and programs and other CMS initiatives would continue to ensure that procedures removed from the IPO list and provided in the hospital outpatient setting could be performed safely on appropriately selected beneficiaries. We also stated that given our increasing ability to measure the safety of procedures performed in the hospital outpatient setting and to monitor the quality of care, in addition to the other safeguards detailed above, we believed that quality of care was unlikely to be affected by the elimination of the IPO list. We noted that we do not require services that are not included on the IPO list to be performed solely in the hospital outpatient setting and that services that were previously identified as inpatient only can continue to be performed in the inpatient setting. We emphasized that physicians should use their clinical knowledge and judgment, together with consideration of the beneficiary's specific needs, to determine whether a procedure can be performed appropriately in a hospital outpatient setting or whether inpatient care is required for the beneficiary, subject to the general coverage rules requiring that any procedure be reasonable and necessary. We also stated that the elimination of the IPO list would ensure maximum availability of services to beneficiaries in the hospital outpatient setting. Finally, we stressed that as medical practice continues to develop, we believed that the difference between the need for inpatient care and the appropriateness of outpatient care has become less distinct for many services Accordingly, in the CY 2021 OPPS/ASC final rule with comment period (85 FR 86084 through 86088), we finalized, with modification, our proposal to eliminate the IPO list over the course of three years (85 FR 86093). We revised our regulation at § 419.22(n) to state that, effective on January 1, 2021, the Secretary shall eliminate the list of services and procedures designated as requiring inpatient care through a 3-year transition. As part of the first phase of this elimination of the IPO list, we removed 298 codes, including 266 musculoskeletal-related services, from the list beginning in CY 2021 and, because we proposed to eliminate the IPO list entirely, the removed procedures were not assessed against our longstanding criteria for removal (85 FR 86094)."
doc2_text = "A. Background Established in rulemaking as part of the initial implementation of the OPPS, the inpatient only (IPO) list identifies services for which Medicare will only make payment when the services are furnished in the inpatient hospital setting because of the invasive nature of the procedure, the underlying physical condition of the patient, or the need for at least 24 hours of postoperative recovery time or monitoring before the patient can be safely discharged (70 FR 68695). The IPO list was created based on the premise (rooted in the practice of medicine at that time), that Medicare should not pay for procedures furnished as outpatient services that are performed on an inpatient basis virtually all of the time for the Medicare population, for the reasons described above, because performing these procedures on an outpatient basis would not be safe or appropriate, and therefore not reasonable and necessary under Medicare rules (63 FR 47571). Services included on the IPO list were those determined to require inpatient care, such as those that are highly invasive, result in major blood loss or temporary deficits of organ systems (such as neurological impairment or respiratory insufficiency), or otherwise require intensive or extensive postoperative care (65 FR 67826). There are some services designated as inpatient only that, given their clinical intensity, would not be expected to be performed in the hospital outpatient setting. For example, we have traditionally considered certain surgically invasive procedures on the brain, heart, and abdomen, such as craniotomies, coronary-artery bypass grafting, and laparotomies, to require inpatient care (65 FR 18456). Designation of a service as inpatient only does not preclude the service from being furnished in a hospital outpatient setting but means that Medicare will not make payment for the service if it is furnished to a Medicare beneficiary in the hospital outpatient setting (65 FR 18443). Conversely, the absence of a procedure from the list should not be interpreted as identifying that procedure as appropriately performed only in the hospital outpatient setting (70 FR 68696) As part of the annual update process, we have historically worked with interested parties, including professional societies, hospitals, surgeons, hospital associations, and beneficiary advocacy groups, to evaluate the IPO list and to determine whether services should be added to or removed from the list. Interested parties are encouraged to request reviews for a particular code or group of codes; and we have asked that their requests include evidence that demonstrates that the procedure was performed on an outpatient basis in a safe and appropriate manner in a variety of different types of hospitals—including but not limited to—operative reports of actual cases, peer-reviewed medical literature, community medical standards and practice, physician comments, outcome data, and post-procedure care data (67 FR 66740) We traditionally have used five longstanding criteria to determine whether a procedure should be removed from the IPO list. As noted in the CY 2012 OPPS/ASC final rule with comment period (76 FR 74353), we assessed whether a procedure or service met these criteria to determine whether it should be removed from the IPO list and assigned to an APC group for payment under the OPPS when provided in the hospital outpatient setting. We have explained that while we only require a service to meet one criterion to be considered for removal, satisfying only one criterion does not guarantee that the service will be removed; instead, the case for removal is strengthened with the more criteria the service meets. The criteria for assessing procedures for removal from the IPO list are the following 1. Most outpatient departments are equipped to provide the services to the Medicare population 2. The simplest procedure described by the code may be furnished in most outpatient departments 3. The procedure is related to codes that we have already removed from the IPO list 4. A determination is made that the procedure is being furnished in numerous hospitals on an outpatient basis 5. A determination is made that the procedure can be appropriately and safely furnished in an ASC and is on the list of approved ASC services or has been proposed by us for addition to the ASC covered procedures list In the past, we have requested that interested parties submit corresponding evidence in support of their claims that a code or group of codes met the longstanding criteria for removal from the IPO list and was safe to perform on the Medicare population in the hospital outpatient setting—including, but not limited to case reports, operative reports of actual cases, peer-reviewed medical literature, medical professional analysis, clinical criteria sets, and patient selection protocols. Our clinicians thoroughly reviewed all information submitted within the context of the established criteria and if, following this review, we determined that there was sufficient evidence to confirm that the code could be safely and appropriately performed on an outpatient basis, we assigned the service to an APC and included it as a payable procedure under the OPPS (67 FR 66740). We determine the APC assignment for services removed from the IPO list by evaluating the clinical similarity and resource costs of the service compared to other services paid under the OPPS and review the Medicare Severity Diagnosis Related Groups (MS-DRG) rate for the service under the IPPS, though we note we would generally expect the cost to provide a service in the outpatient setting to be less than the cost to provide the service in the inpatient setting We stated in prior rulemaking that, over time, given advances in technology and surgical technique, we would continue to evaluate services to determine whether they should be removed from the IPO list. Our goal is to ensure that inpatient only designations are consistent with the current standards of practice. We have asserted in prior rulemaking that, insofar as advances in medical practice mitigate concerns about these procedures being performed on an outpatient basis, we would be prepared to remove procedures from the IPO list and provide for payment for them under the OPPS (65 FR 18443). Further, CMS has at times had to reclassify codes as inpatient only services with the emergence of new information We refer readers to the CY 2012 OPPS/ASC final rule with comment period (76 FR 74352 through 74353) for a full discussion of our historic policies for identifying services that are typically provided only in an inpatient setting and that, therefore, will not be paid by Medicare under the OPPS, as well as the criteria we have used to review the IPO list to determine whether any services should be removed In the CY 2021 OPPS/ASC final rule with comment period (85 FR 86084 through 86088) we finalized a policy to eliminate the IPO list over the course of 3 years (85 FR 86093). We revised our regulation at § 419.22(n) to state that, effective on January 1, 2021, the Secretary shall eliminate the list of services and procedures designated as requiring inpatient care through a 3-year transition. As part of the first phase of this elimination of the IPO list, we removed 298 codes, including 266 musculoskeletal-related services, from the list beginning in CY 2021 In the CY 2022 OPPS/ASC final rule with comment period, we halted the elimination of the IPO list and, after clinical review of the services removed from the IPO list in CY 2021 as part of the first phase of eliminating the IPO list using the above five criteria, we returned most services removed from the IPO list in CY 2021 back to the IPO list beginning in CY 2022 (86 FR 63671 through 63736). We also amended the regulation at § 419.22(n) to remove the reference to the elimination of the list of services and procedures designated as requiring inpatient care through a 3-year transition. We also finalized our proposal to codify the five longstanding criteria for determining whether a service or procedure should be removed from the IPO list in the regulation in a new § 419.23 (86 FR 63678)."

dmp = dmp_module.diff_match_patch()
dmp.Diff_Timeout = 2000
diff = dmp.diff_main(doc1_text, doc2_text)
dmp.diff_cleanupSemantic(diff)
# dmp.diff_cleanupEfficiency(diff)

x = dmp.diff_prettyHtml(diff)
print('###########################################################')

# print(x)
print('###########################################################')


# print(doc1_text)

# print(doc2_text)
# \for each heading:


def add_line_break(paragraph):
    new_paragraph = ""
    for i in range(len(paragraph)):
        if paragraph[i] == 'Comment:' or paragraph[i] == 'Response:':
            new_paragraph += '<br> <br>' + paragraph[i]
        else:
            new_paragraph += paragraph[i]
    return new_paragraph

def add_line_break2(x):
    y = x.replace("Comment:", "</br> </br> <em> Comment: </em>")
    z = y.replace("Response:", "</br> </br> <em> Response: </em>")
    return z


with open('TEXT2.html', 'w', encoding='utf-8') as f:
    # f.write(x)
    f.write('<html>\n<head>\n<link rel="stylesheet" href="styles.css">\n<title>' +
            "res3"+'</title>\n</head>\n<body>\n')
    f.write('<div class="para changes">\n')
    for line in diff:
        x = add_line_break2(line[1])
        # x=line[1]
        if line[0] == 0:
            f.write(f'<p class="no_change">{x}</p>')
        elif line[0] == -1:
            f.write(f'\n<p class="red">{x}</p>')
        elif line[0] == 1:
            f.write(f'\n<p class="green">{x}</p>')
    f.write('</div>\n')
    f.write('</body>\n</html>')
