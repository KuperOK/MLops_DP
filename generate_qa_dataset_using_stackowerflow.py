import requests
from bs4 import BeautifulSoup
import time
from tqdm import tqdm
import json

########### QUESTIONS GATHERING #############

TOPIC = 'nmap'
urlq = "https://api.stackexchange.com/2.3/questions"
paramsq = {    
    'order': 'asc',
    'fromdate': '1199145600',
    'site': 'stackoverflow',
    'tagged': [TOPIC],
    'filter': 'withbody',
    
}
pages = 25
cleaned_questions = []
questions_id = []
titles_q = []
bodies_q = []
for page in range(1, pages+1):
  paramsq['page'] = page
  response = requests.get(urlq, params=paramsq)
  data = response.json()

  for question in data['items']:
    if question['is_answered']:
      soup = BeautifulSoup(question['body'], 'html.parser')
      title = question['title']
      titles_q.append(title)
      body = soup.get_text().strip()
      bodies_q.append(body)
      clean_text = title + '\n' + body
      cleaned_questions.append(clean_text)
      questions_id.append(question['question_id'])

print(f'Collected {len(cleaned_questions)} nmap questions')


########### ANSWERS GATHERING #############

cleaned_answ_list = []

try:
  for qid in tqdm(questions_id):
    
    url = f'https://api.stackexchange.com/2.3/questions/{qid}/answers'
    params = {
      'order': 'desc',
      'sort': 'votes',    
      'site': 'stackoverflow',       
      'filter': 'withbody',    
    }
    response = requests.get(url, params=params)

    answers = response.json()

    cleaned_answers = ''  
    for idx, answer in enumerate(answers['items']):
      if answer['score'] > 0:
        soup = BeautifulSoup(answer['body'], 'html.parser')
        clean_text = soup.get_text()
        cleaned_answers += f'\nAnswer {idx+1}:\n' + clean_text.strip()
    cleaned_answ_list.append(cleaned_answers)
    time.sleep(2)
except KeyError:
  pass
finally:
  print(f'Collected {len(cleaned_answ_list)} nmap answers')

############### SAVE DATASET TO JSON #############

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

qa_pairs_json = [{'question': q, 'answer': a} for q, a in zip(cleaned_questions, cleaned_answ_list)]
empty_idx = []
for i, a in enumerate(cleaned_answ_list):
  if not a:
    empty_idx.append(i)

qa_pairs_json = []
for i in range(len(cleaned_answ_list)):
  if  i not in empty_idx:
    qa_pairs_json.append({'question': cleaned_questions[i], 'answer': cleaned_answ_list[i]})

print(f'Collected {len(qa_pairs_json)} nmap qa pairs')
save_to_json(qa_pairs_json, 'nmap_qa_dataset.json')