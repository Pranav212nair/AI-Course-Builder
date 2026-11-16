"""
Agent 1: Skill Assessment Agent.

Generates assessment questions for a topic/level, and evaluates the
user's answers into a skill level + strengths/weaknesses.
"""

from app.agents.ai_schemas import (
    AssessmentQuestionOut,
    AssessmentQuestionSet,
    AssessmentResult,
)
from app.core.ai_client import call_structured
from app.models.enums import SkillLevel


def generate_assessment_questions(
    topic: str, current_level: SkillLevel
) -> AssessmentQuestionSet:
    return call_structured(
        system_prompt=(
            "You are the Skill Assessment Agent in an AI course builder. "
            "Generate multiple-choice questions that accurately probe whether "
            "a learner is at the level they claim, covering a spread of "
            "subtopics within the given topic."
        ),
        user_prompt=(
            f"Topic: {topic}\n"
            f"Learner's self-reported level: {current_level.value}\n"
            "Generate 5 multiple-choice questions, each with exactly 4 "
            "options and one correct_answer that matches one option exactly. "
            "Vary the subtopics covered."
        ),
        response_model=AssessmentQuestionSet,
        mock_fn=lambda: _mock_questions(topic, current_level),
    )


def evaluate_assessment(
    topic: str, current_level: SkillLevel, answered: list[dict]
) -> AssessmentResult:
    """
    `answered` is a list of dictionaries containing:
    question, topic, options, correct_answer, and selected_answer.
    """
    correct_count = sum(
        1
        for answer in answered
        if answer["selected_answer"] == answer["correct_answer"]
    )
    accuracy = correct_count / len(answered) if answered else 0

    return call_structured(
        system_prompt=(
            "You are the Skill Assessment Agent. Given a learner's answers "
            "to a diagnostic quiz, determine their real skill level and "
            "identify specific strengths and weaknesses by subtopic. "
            "Name the concepts instead of using vague labels such as "
            "'good' or 'bad'."
        ),
        user_prompt=(
            f"Topic: {topic}\n"
            f"Self-reported level: {current_level.value}\n"
            f"Accuracy: {correct_count}/{len(answered)} ({accuracy:.0%})\n"
            f"Answers: {answered}"
        ),
        response_model=AssessmentResult,
        mock_fn=lambda: _mock_result(current_level, accuracy, answered),
    )


# Mocks used when USE_MOCK_AI=true or no API key is configured.


def _mock_questions(
    topic: str, current_level: SkillLevel
) -> AssessmentQuestionSet:
    normalized_topic = topic.strip().lower()

    if "java" in normalized_topic:
        question_data = [
            (
                "What is the purpose of the main method in a Java application?",
                [
                    "It is the usual entry point for running the application",
                    "It creates a database connection",
                    "It compiles the Java source code",
                    "It always runs in a separate thread",
                ],
                "It is the usual entry point for running the application",
                "Java fundamentals",
            ),
            (
                "Which Java type stores a whole number such as 42?",
                ["double", "boolean", "int", "String"],
                "int",
                "Java types",
            ),
            (
                "Which keyword creates a new object in Java?",
                ["make", "new", "object", "create"],
                "new",
                "Object creation",
            ),
            (
                "What does a for loop commonly provide?",
                [
                    "Repeated execution while iterating over a range or collection",
                    "Automatic database backups",
                    "A way to define a class",
                    "A replacement for all methods",
                ],
                "Repeated execution while iterating over a range or collection",
                "Control flow",
            ),
            (
                "Which collection does not allow duplicate elements?",
                ["List", "Set", "ArrayList", "Vector"],
                "Set",
                "Collections",
            ),
        ]
    else:
        question_data = [
            (
                f"What is the main purpose of learning {topic} fundamentals?",
                [
                    "To build a reliable foundation for more advanced work",
                    "To avoid practicing the subject",
                    "To replace every other skill",
                    "To guarantee that no mistakes occur",
                ],
                "To build a reliable foundation for more advanced work",
                "Fundamentals",
            ),
            (
                f"Which approach is generally best when starting with {topic}?",
                [
                    "Practice small examples and build up gradually",
                    "Memorize everything without practice",
                    "Skip the basic concepts",
                    "Use the most complex solution first",
                ],
                "Practice small examples and build up gradually",
                "Learning approach",
            ),
            (
                f"Why should you break a {topic} problem into smaller parts?",
                [
                    "Smaller parts are easier to understand, test, and improve",
                    "It makes the problem impossible to solve",
                    "It removes the need to check results",
                    "It guarantees the shortest code",
                ],
                "Smaller parts are easier to understand, test, and improve",
                "Problem solving",
            ),
            (
                f"What is a useful way to check your progress in {topic}?",
                [
                    "Apply concepts in a small project or exercise",
                    "Avoid reviewing your work",
                    "Only read titles of lessons",
                    "Change topics after every question",
                ],
                "Apply concepts in a small project or exercise",
                "Practice",
            ),
            (
                f"What should you do when a {topic} solution does not work?",
                [
                    "Inspect the result, isolate the problem, and try a correction",
                    "Delete all your work immediately",
                    "Assume the problem cannot be solved",
                    "Ignore the result",
                ],
                "Inspect the result, isolate the problem, and try a correction",
                "Debugging",
            ),
        ]

    questions = [
        AssessmentQuestionOut(
            question=question,
            options=options,
            correct_answer=correct_answer,
            topic=subtopic,
        )
        for question, options, correct_answer, subtopic in question_data
    ]

    return AssessmentQuestionSet(questions=questions)


def _mock_result(
    current_level: SkillLevel,
    accuracy: float,
    answered: list[dict],
) -> AssessmentResult:
    levels = list(SkillLevel)
    current_index = levels.index(current_level)

    if accuracy >= 0.8 and current_index < len(levels) - 1:
        skill_level = levels[current_index + 1]
    elif accuracy < 0.4 and current_index > 0:
        skill_level = levels[current_index - 1]
    else:
        skill_level = current_level

    topics = [
        answer.get("topic", "General")
        for answer in answered
    ]

    correct_topics = [
        answer.get("topic", "General")
        for answer in answered
        if answer["selected_answer"] == answer["correct_answer"]
    ]

    incorrect_topics = [
        topic_name
        for topic_name in topics
        if topic_name not in correct_topics
    ] or ["Fundamentals"]

    return AssessmentResult(
        skill_level=skill_level,
        strengths=list(dict.fromkeys(correct_topics))[:5]
        or ["Getting started"],
        weaknesses=list(dict.fromkeys(incorrect_topics))[:5],
    )
