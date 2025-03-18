import openai
import random
import time
import csv
from io import StringIO
import os
from dotenv import load_dotenv

load_dotenv()

class QuizSolver:
    def __init__(self, navigator):
        self.navigator = navigator
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def solve_quiz(self, questions):
        for question in questions:
            print(f"Solving question: {question['text']}")
            prompt = self.format_prompt(question)
            response = self.ask_gpt(prompt)
            reasoning, csv_list = self.parse_response(response)
            correct_option_numbers = self.parse_csv(csv_list)
            self.fill_answers(question, correct_option_numbers)
            delay = random.uniform(5, 10)
            print(f"Waiting {delay:.2f} seconds before next question...")
            time.sleep(delay)
        print("Quiz completed successfully.")

    def ask_gpt(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500
        )
        return response.choices[0].message['content'].strip()

    def format_prompt(self, question):
        options_text = "\n".join([f"{idx+1}. {opt['text']}" for idx, opt in enumerate(question['options'])])
        prompt = (
            f"Question:\n{question['text']}\n\n"
            f"Answer Options:\n{options_text}\n\n"
            "Respond with 100 WORDS OF REASONING AND a CSV list containing the correct answer option numbers. "
            "REASONING AND CSV LIST SHOULD BE SEPARATE BY THE '***' DELIMITER. "
            "For example, '<sample_reasoning>' *** '1,3,4' or '2'"
        )
        return prompt

    def parse_response(self, response):
        try:
            reasoning, csv_list = response.split('***')
            return reasoning.strip(), csv_list.strip()
        except ValueError:
            print("Error: Response format is incorrect. Ensure the '***' delimiter is present.")
            return "", ""

    def parse_csv(self, csv_string):
        reader = csv.reader(StringIO(csv_string))
        answers = next(reader)
        return [int(a.strip()) for a in answers if a.strip().isdigit()]

    def fill_answers(self, question, correct_option_numbers):
        for option_number in correct_option_numbers:
            if 1 <= option_number <= len(question['options']):
                option = question['options'][option_number - 1]
                self.navigator.select_option_by_id(option['id'])
                print(f"Selected option: {option['text']}")
            else:
                print(f"Option number {option_number} out of range for question: {question['text']}")
