# https://ibegin.tcs.com/iBegin/jobs/search

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from pymongo import MongoClient
import csv

def remove_non_ascii(string):
    return ''.join(i for i in string if ord(i)<128)

csv_file = open('TCS_Jobs.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Job ID', 'Job Title', 'URL', 'Job Description', 'Job Function', 'Job Role', 'Desired Skills', 'Qualifications', 'Experience', 'Apply By', 'Location', 'Country'])

s = requests.Session()

req_payload = {'pageNumber': '1', 'regular': 'true', 'walkin': 'true'}
source_response = s.post('https://ibegin.tcs.com/iBegin/api/v1/jobs/searchJ?', json=req_payload)
print(source_response)

total_jobs = source_response.json()['data']['totalJobs']
pages = total_jobs//10
if total_jobs%10 != 0:
    pages = pages + 1
# print(pages)

job_ids = []

for page in range(1,pages+1):
    req_payload = {'pageNumber': f'{page}', 'regular': 'true', 'walkin': 'true'}
    source_response = s.post('https://ibegin.tcs.com/iBegin/api/v1/jobs/searchJ?', json=req_payload)
#     print(source_response)

    jobs = source_response.json()['data']['jobs']
    for job in jobs:
        job_id = job['id']
        job_ids.append(job_id)
        
print(len(job_ids))


for job in job_ids:
    job_url = f'https://ibegin.tcs.com/iBegin/jobs/{job}'
#     print(job_url)
    
    job_id = job[0:-1]
#     print(job_id)
    
    req_payload = {'jobId': f'{job_id}'}
    response = s.post('https://ibegin.tcs.com/iBegin/api/v1/job/desc?', json=req_payload)
#     print(response)

    job_data = response.json()['data']
    
    job_title = job_data['title'].strip()
    job_title = remove_non_ascii(job_title)
#     print(job_title)
    
    location = job_data['location'].strip()
#     print(location)
    
    experience = job_data['experience'].strip()
#     print(experience)
    
    date = job_data['applyby'].strip().split(' ')[0]
    date = date.split('-')
    parts = []
    for i in date:
        i = int(i)
        parts.append(i)
    date = datetime(parts[0], parts[1], parts[2])
    date = date.strftime("%d-%b-%Y")
    apply_by = date
#     print(apply_by)

    job_description = job_data['description'].strip()
    job_description = BeautifulSoup(job_description, 'lxml').text
    job_description = remove_non_ascii(job_description)
    job_description = " ".join(job_description.split())
#     print(job_description)

    job_function = job_data['functionName'].strip()
#     print(job_function)

    job_role = job_data['role'].strip()
#     print(job_role)

    skills = job_data['skilldetail']
#     print(skills)

    qualifications = job_data['qualifications'].strip()
#     print(qualifications)

    country = job_data['country'].strip()
#     print(country)
    
    csv_writer.writerow([job_id, job_title, job_url, job_description, job_function, job_role, skills, qualifications, experience, apply_by, location, country])



csv_file.close()

print('\nDone')












