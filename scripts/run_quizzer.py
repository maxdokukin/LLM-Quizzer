from src.classes.CanvasNavigator import CanvasNavigator
from src.classes.QuizSolver import QuizSolver




if __name__ == "__main__":
    navigator = CanvasNavigator()
    navigator.navigate_to_quiz()
    navigator.click_start_or_resume_quiz()

    questions = navigator.scrape_questions()

    quiz_solver = QuizSolver(navigator)
    quiz_solver.solve_quiz(questions)

    navigator.terminate()
