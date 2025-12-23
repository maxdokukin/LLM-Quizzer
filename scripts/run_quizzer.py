from src.classes.CanvasNavigator import CanvasNavigator
from src.classes.QuizSolver import QuizSolver




if __name__ == "__main__":
    navigator = CanvasNavigator()

    quiz_data = [
        # ("Intro", "https://sjsu.instructure.com/courses/1606720/quizzes/1831910/", "../data/raw/Intro.txt"),
        # ("Recognition Status", "https://sjsu.instructure.com/courses/1606720/quizzes/1831911", "../data/raw/Rerecognition.txt"),
        ("Community Expectations", "https://sjsu.instructure.com/courses/1606720/quizzes/1831912", "../data/raw/Community Expectations.txt"),
        # 100% ("Club Officers and Club Members", "https://sjsu.instructure.com/courses/1606720/quizzes/1831915", "../data/raw/Club Officers and Club Members.txt"),
        # 100% ("T9", "https://sjsu.instructure.com/courses/1606720/quizzes/1831906", "../data/raw/T9.txt"),
        # 100% ("Hazing", "https://sjsu.instructure.com/courses/1606720/quizzes/1831914", "../data/raw/Hazing.txt"),
        ("Events and Spaces on Campus", "https://sjsu.instructure.com/courses/1606720/quizzes/1831918", "../data/raw/Events and Spaces on Campus.txt"),
        # 100% ("Finance and Bank Accounts", "https://sjsu.instructure.com/courses/1606720/quizzes/1831909", "../data/raw/Finance and Bank Accounts.txt"),
        ("Funding Sources", "https://sjsu.instructure.com/courses/1606720/quizzes/1831907", "../data/raw/Funding Sources.txt"),
        # 100% ("Marketing Basics", "https://sjsu.instructure.com/courses/1606720/quizzes/1831908", "../data/raw/Marketing Basics.txt"),
        # 100% ("Alcohol Basics", "https://sjsu.instructure.com/courses/1606720/quizzes/1831919", "../data/raw/Alcohol Basics.txt"),
        ("Event Planning", "https://sjsu.instructure.com/courses/1606720/quizzes/1831916", "../data/raw/Event Planning.txt"),
        # ("", "", "../data/raw/.txt"),
    ]
    for name, link, relevant_info in quiz_data:
        navigator.navigate_to_quiz(link)
        navigator.click_start_or_resume_quiz()

        questions = navigator.scrape_questions()

        quiz_solver = QuizSolver(navigator)
        quiz_solver.solve_quiz(questions, relevant_info)

        navigator.submit_quiz()

    navigator.terminate()
