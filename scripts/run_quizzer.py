from src.classes.CanvasNavigator import CanvasNavigator
from src.classes.QuizSolver import QuizSolver




if __name__ == "__main__":
    navigator = CanvasNavigator()

    quiz_data = [
        # ("Student Organization Basics", "https://sjsu.instructure.com/courses/1588185/quizzes/1760127", "Student Organization Basics.txt"),
        # ("Student Organization Basics", "https://sjsu.instructure.com/courses/1588185/quizzes/1760137?module_item_id=15535888", "../data/raw/Student Organization Basics.txt"),
        # ("Community Standards", "https://sjsu.instructure.com/courses/1588185/quizzes/1760139?module_item_id=15535889", "../data/raw/Community Standards.txt"),
        # ("Club Officers", "https://sjsu.instructure.com/courses/1588185/quizzes/1760130?module_item_id=15535890", "../data/raw/Club Officers.txt"),
        # ("Title IX ", "https://sjsu.instructure.com/courses/1588185/quizzes/1760132?module_item_id=15535891", "../data/raw/T9.txt"),
        # ("Hazing", "https://sjsu.instructure.com/courses/1588185/quizzes/1760138?module_item_id=15535892", "../data/raw/Hazing.txt"),
        # ("Events and Spaces on Campus", "https://sjsu.instructure.com/courses/1588185/quizzes/1760133?module_item_id=15564493", "../data/raw/Events and Spaces on Campus.txt"),
        # ("Funding", "https://sjsu.instructure.com/courses/1588185/quizzes/1760131?module_item_id=15539316", "../data/raw/Funding.txt"),
        # ("Marketing, Advertising", "https://sjsu.instructure.com/courses/1588185/quizzes/1760136?module_item_id=15539317", "../data/raw/Marketing, Advertising.txt"),
        # ("Alcohol", "https://sjsu.instructure.com/courses/1588185/quizzes/1760128?module_item_id=15539318", "../data/raw/Alcohol.txt"),
        ("Event Planning", "https://sjsu.instructure.com/courses/1588185/quizzes/1760848?module_item_id=15539326", "../data/raw/Event Planning.txt"),
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
