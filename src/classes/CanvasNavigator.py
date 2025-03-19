# canvas_navigator.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv
from src.functions.utils import print_verbose

load_dotenv()

class CanvasNavigator:
    def __init__(self):
        self.canvas_link = os.getenv('CANVAS_LINK')
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.verbose = os.getenv('VERBOSE', 'True') == 'True'
        self.verbose_color = os.getenv('VERBOSE_COLOR', 'green')
        self.verbose_label = os.getenv('VERBOSE_LABEL', 'CANVAS')

        self.driver = webdriver.Chrome()

        try:
            self.login_to_canvas()
        except Exception as e:
            self.print_verbose(f"An error occurred: {e}")

    def print_verbose(self, text):
        print_verbose(
            text,
            self.verbose,
            self.verbose_color,
            self.verbose_label
        )

    def login_to_canvas(self):
        self.print_verbose("Function: login_to_canvas")
        self.driver.get(self.canvas_link)
        self.print_verbose("Navigated to login page.")

        wait = WebDriverWait(self.driver, 30)

        try:
            username_field = wait.until(EC.presence_of_element_located((By.NAME, 'identifier')))
            password_field = wait.until(EC.presence_of_element_located((By.NAME, 'credentials.passcode')))
            self.print_verbose("Located username and password fields.")
        except Exception as e:
            self.print_verbose(f"Unable to locate fields: {e}")
            self.driver.quit()
            return

        username_field.send_keys(self.username)
        self.print_verbose("Entered username.")
        password_field.send_keys(self.password)
        self.print_verbose("Entered password.")

        try:
            sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@type="submit" and @value="Sign in"]')))
            sign_in_button.click()
            self.print_verbose("Clicked the Sign In button.")
        except Exception as e:
            self.print_verbose(f"Unable to click Sign In: {e}")
            self.driver.quit()
            return

        try:
            dashboard_element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="hidden-phone" and text()="Dashboard"]')))
            self.print_verbose("Login successful.")
        except Exception as e:
            self.print_verbose(f"Login verification failed: {e}")
            self.driver.quit()

    def navigate_to_quiz(self, quiz_link):
        self.driver.get(quiz_link)
        self.print_verbose("Navigated to quiz.")
        time.sleep(5)


    def select_answer(self, question_element, answer_text):
        options = question_element.find_all('label')
        for option in options:
            option_text = option.get_text(separator=' ', strip=True)
            if answer_text.lower() in option_text.lower():
                option_input = option.find('input')
                option_id = option_input.get('id')
                self.driver.execute_script(f"document.getElementById('{option_id}').click();")
                break

    def go_to_next_page(self):
        try:
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Next"]'))
            )
            next_button.click()
            time.sleep(3)
            return True
        except:
            return False

    def terminate(self):
        self.driver.quit()
        self.print_verbose("Browser driver quit.")

    def click_start_or_resume_quiz(self):
        self.print_verbose("Function: click_start_or_resume_quiz")
        try:
            wait = WebDriverWait(self.driver, 10)
            quiz_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                 '//div[@class="take_quiz_button"]/a[contains(text(), "Take the Quiz") or contains(text(), "Resume Quiz")]')))
            quiz_button.click()
            self.print_verbose("Clicked 'Take the Quiz' or 'Resume Quiz' button.")
            time.sleep(3)
        except Exception as e:
            self.print_verbose(f"Unable to click quiz button: {e}")
            self.driver.quit()

    def scrape_questions(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        question_containers = soup.find_all('div', class_='display_question')

        questions_data = []

        for container in question_containers:
            question_id = container.get('id')

            # Extract question text
            question_text_div = container.find('div', class_='question_text')
            question_text = question_text_div.get_text(strip=True)

            # Determine question type
            classes = container.get('class', [])
            if 'multiple_answers_question' in classes:
                q_type = 'multiple_choice'
            elif 'true_false_question' in classes or 'multiple_choice_question' in classes:
                q_type = 'single_choice'
            elif 'short_answer_question' in classes or 'essay_question' in classes:
                q_type = 'text_entry'
            else:
                q_type = 'unknown'

            # Extract options
            options = []
            answers_div = container.find('div', class_='answers')
            if answers_div:
                answer_divs = answers_div.find_all('div', class_='answer')
                for ans_div in answer_divs:
                    input_tag = ans_div.find('input', class_='question_input')
                    option_id = input_tag.get('id') if input_tag else None
                    label_div = ans_div.find('div', class_='answer_label')
                    option_text = label_div.get_text(strip=True) if label_div else ''
                    if option_id and option_text:
                        options.append({'id': option_id, 'text': option_text})

            questions_data.append({
                'id': question_id,
                'type': q_type,
                'text': question_text,
                'options': options
            })

        return questions_data

    def select_option_by_id(self, option_id):
        try:
            self.driver.execute_script(f"document.getElementById('{option_id}').click();")
            self.print_verbose(f"Clicked option with ID {option_id}.")
        except Exception as e:
            self.print_verbose(f"Failed to click option {option_id}: {e}")


    def submit_quiz(self):
        """
        Clicks the 'Submit Quiz' button on a Canvas quiz page.
        """
        self.print_verbose("Function: submit_quiz")

        try:
            # Wait until the 'Submit Quiz' button is clickable
            submit_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "submit_quiz_button"))
            )

            # Click the 'Submit Quiz' button
            submit_button.click()
            self.print_verbose("Clicked the 'Submit Quiz' button.")

            # Optional: Wait for confirmation of submission (modify selector based on UI behavior)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "quiz_submission_confirmation"))
            )
            self.print_verbose("Quiz submission confirmed.")

        except Exception as e:
            self.print_verbose(f"Error clicking the 'Submit Quiz' button: {e}")
