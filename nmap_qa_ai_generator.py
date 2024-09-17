import os
from openai import OpenAI
import json
# from dotenv import load_dotenv
# load_dotenv()

api_key = 'api_key'
client = OpenAI(api_key=api_key)

def generate_qa(num_questions):
    questions = []
    qa_pairs = []
    qa_pairs_json = []

    for i in range(num_questions):
        question_prompt = f"Create a question about Nmap. Question #{i+1}"
        question_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question_prompt}]
        )
        question = question_response.choices[0].message.content.strip()
        questions.append(question)

        answer_prompt = f"Provide a brief answer (up to 10 sentences) to the following Nmap question: {question}"
        answer_response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": answer_prompt}]
        )
        answer = answer_response.choices[0].message.content.strip()
        qa_pairs.append(f"Question: {question}\n\nAnswer: {answer}\n\n")
        qa_pairs_json.append({"question": question, "answer": answer})


    return questions, qa_pairs, qa_pairs_json

def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def save_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    num_questions = 5
    questions, qa_pairs, qa_pairs_2json = generate_qa(num_questions)

    save_to_file('nmap_ai_questions.txt', questions)
    save_to_file('nmap_ai_qa.txt', qa_pairs)
    save_to_json(qa_pairs_2json, 'nmap_qa_ai_dataset.json')

    print("Files successfully created: nmap_ai_questions.txt and nmap_ai_qa.txt")

