import re

import openai
import random
import time
import csv
from io import StringIO
import os
from dotenv import load_dotenv
from src.classes.GPT import GPT


class QuizSolver:
    def __init__(self, navigator):
        self.navigator = navigator
        self.gpt = GPT()

    def solve_quiz(self, questions, relevant_info):
        for question in questions:
            print(f"Solving question: {question['text']}")
            prompt = self.format_prompt(question, relevant_info)
            response = self.gpt.ask_gpt(prompt)
            reasoning, correct_option_numbers = self.parse_response(response)
            print("reasoning:", reasoning, "\ncsv_list:", correct_option_numbers)
            self.fill_answers(question, correct_option_numbers)
            delay = random.uniform(5, 10)
            print(f"Waiting {delay:.2f} seconds before next question...")
            time.sleep(delay)
        print("Quiz completed successfully.")

    def ask_gpt(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=500
        )
        return response.choices[0].message['content'].strip()

    def format_prompt(self, question, relevant_info):

        with open(relevant_info) as f:
            relevant_data = f.readlines()
        options_text = "\n".join([f"{idx+1}. {opt['text']}" for idx, opt in enumerate(question['options'])])
        prompt = (
            f"Question:\n{question['text']}\n\n"
            f"Answer Options:\n{options_text}\n\n"
            "Respond with 100 WORDS OF REASONING AND a CSV list containing the correct correct_answers=[correct option numbers]."
            f"REASONING SHOULD BE FIRST, AND THEN THE LAST LINE OF THE OUTPUT IS ALWAYS correct_answers=[correct option numbers] VARIABLE"
            f"SAMPLE OUTPUT:"
            f"<sample_reasoning>"
            f"correct_answers=[1,3,4]"
            f"HERE IS THE RELEVANT INFORMATION TO HELP YOU ANSWER. USE IT TO ANSWER THE QUESTION: {relevant_data}"
        )
        return prompt

    def parse_response(self, output):
        """
        Parses the ChatGPT output to extract the reasoning and the list of correct answers.

        Parameters:
            output (str): The response from ChatGPT.

        Returns:
            tuple: (reasoning (str), correct_answers (list of int))
        """
        # Split the output by lines
        lines = output.strip().split("\n")

        # Extract reasoning (all lines except the last one)
        reasoning = "\n".join(lines[:-1]).strip()

        # Extract the correct_answers list using regex
        match = re.search(r"correct_answers=\[([\d,\s]*)\]", lines[-1])

        if match:
            # Convert the extracted numbers into a list of integers
            correct_answers = [int(num) for num in match.group(1).split(",") if num.strip().isdigit()]
        else:
            correct_answers = []

        return reasoning, correct_answers

    def parse_csv(self, csv_string):
        answers = csv_string.replace("'", "").split(",")
        return [int(a.strip()) for a in answers]

    def fill_answers(self, question, correct_option_numbers):
        for option_number in correct_option_numbers:
            if 1 <= option_number <= len(question['options']):
                option = question['options'][option_number - 1]
                self.navigator.select_option_by_id(option['id'])
                print(f"Selected option: {option['text']}")
            else:
                print(f"Option number {option_number} out of range for question: {question['text']}")
