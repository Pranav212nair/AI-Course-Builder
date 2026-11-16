"""
Agent 4: Quiz Generation Agent.

Generates a module's quiz from its lessons' content, adjusting overall
difficulty based on the learner's most recent quiz performance (if any).
"""
from app.core.ai_client import call_structured
from app.agents.ai_schemas import QuizQuestionSet, QuizQuestionOut
from app.models.enums import Difficulty, QuestionType


def generate_quiz(
    *,
    module_title: str,
    lesson_summaries: list[str],
    recent_avg_score: float | None,
) -> QuizQuestionSet:
    if recent_avg_score is None:
        difficulty_hint = "Use a mix of easy and medium questions — this is the learner's first quiz."
    elif recent_avg_score >= 85:
        difficulty_hint = "The learner has been scoring well; lean toward medium/hard questions."
    elif recent_avg_score < 60:
        difficulty_hint = "The learner has been struggling; lean toward easy/medium questions."
    else:
        difficulty_hint = "Use a balanced mix of easy, medium, and hard questions."

    return call_structured(
        system_prompt=(
            "You are the Quiz Generation Agent. Write quiz questions based "
            "strictly on the given lesson summaries for one module. Prefer "
            "multiple_choice; use 'descriptive' only for a question that "
            "genuinely needs a short written answer. Tag each question with the "
            "specific subtopic it tests so weak areas can be identified later."
        ),
        user_prompt=(
            f"Module: {module_title}\n"
            f"Lesson summaries covered: {lesson_summaries}\n"
            f"{difficulty_hint}\n"
            "Generate 5 questions."
        ),
        response_model=QuizQuestionSet,
        mock_fn=lambda: _mock_quiz(module_title, lesson_summaries, recent_avg_score),
    )


def _mock_quiz(module_title: str, lesson_summaries: list[str], recent_avg_score: float | None) -> QuizQuestionSet:
    difficulty = Difficulty.medium
    if recent_avg_score is not None:
        difficulty = Difficulty.hard if recent_avg_score >= 85 else (
            Difficulty.easy if recent_avg_score < 60 else Difficulty.medium
        )

    questions = [
        QuizQuestionOut(
            question=f"Which statement best summarizes this module's main idea?",
            question_type=QuestionType.multiple_choice,
            options=[
                "It should be understood and applied in a small example",
                "It should be memorized without practice",
                "It is unrelated to the lessons",
                "It can only be used in advanced projects",
            ],
            correct_answer="It should be understood and applied in a small example",
            topic=module_title,
            difficulty=difficulty,
        ),
        QuizQuestionOut(
            question="What is the best first step when applying a new concept?",
            question_type=QuestionType.multiple_choice,
            options=[
                "Start with a small, testable example",
                "Skip directly to the hardest problem",
                "Avoid checking the result",
                "Copy a solution without understanding it",
            ],
            correct_answer="Start with a small, testable example",
            topic=f"{module_title} — application",
            difficulty=difficulty,
        ),
        QuizQuestionOut(
            question="How should you respond when an example produces an unexpected result?",
            question_type=QuestionType.multiple_choice,
            options=[
                "Inspect the steps, isolate the issue, and test a correction",
                "Ignore the result",
                "Delete the entire project",
                "Assume every result is correct",
            ],
            correct_answer="Inspect the steps, isolate the issue, and test a correction",
            topic=f"{module_title} — debugging",
            difficulty=difficulty,
        ),
    ]
    return QuizQuestionSet(questions=questions)
