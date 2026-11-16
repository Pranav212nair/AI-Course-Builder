"""
Agent 3: Content Generation Agent.

Generates a single lesson's full content, adapted to the learner's level
and preferred learning style. Called lazily the first time a lesson is
opened (see api/lessons.py), not upfront for the whole roadmap.
"""
from app.core.ai_client import call_structured
from app.agents.ai_schemas import LessonContentOut
from app.models.enums import LearningStyle, SkillLevel


def generate_lesson_content(
    *,
    course_topic: str,
    module_title: str,
    lesson_title: str,
    skill_level: SkillLevel,
    learning_style: LearningStyle,
) -> LessonContentOut:
    style_hint = {
        LearningStyle.visual: "Lean on described diagrams/visual mental models and illustrated examples.",
        LearningStyle.reading_writing: "Lean on clear written explanations and structured notes.",
        LearningStyle.hands_on: "Lean on a practical, exercise-first framing — get the learner typing/doing quickly.",
        LearningStyle.mixed: "Blend explanation, a visual analogy, and a hands-on exercise.",
    }[learning_style]

    return call_structured(
        system_prompt=(
            "You are the Content Generation Agent. Write one self-contained "
            "lesson: clear learning objectives, a simple-language explanation, "
            "concrete examples, one practical exercise, and a short summary. "
            f"{style_hint}"
        ),
        user_prompt=(
            f"Course topic: {course_topic}\n"
            f"Module: {module_title}\n"
            f"Lesson: {lesson_title}\n"
            f"Learner's current skill level: {skill_level.value}\n"
            "Keep the explanation appropriately paced for that level — don't "
            "over-explain for advanced learners or skip basics for beginners."
        ),
        response_model=LessonContentOut,
        mock_fn=lambda: _mock_content(
            course_topic, module_title, lesson_title, skill_level
        ),
    )


def _mock_content(
    course_topic: str,
    module_title: str,
    lesson_title: str,
    skill_level: SkillLevel,
) -> LessonContentOut:
    topic = course_topic.strip().lower()
    lesson = lesson_title.strip().lower()

    if "java" in topic:
        content = {
            "getting set up": (
                ["Install a JDK and verify it with `java --version`",
                 "Compile and run a small Java class"],
                "A Java program is compiled by the JDK and then run by the JVM. "
                "The JDK includes tools such as `javac`, while the JVM executes "
                "the compiled bytecode.",
                ["Run `java --version`.", "Create `Hello.java` with a main method and run it."],
                "Create a small Java program that prints your name and confirm it runs from the command line.",
                "You learned how the JDK, compiler, and JVM fit together.",
            ),
            "core concepts": (
                ["Declare variables with appropriate Java types",
                 "Explain the difference between primitive values and objects"],
                "Java is statically typed, so each variable has a declared type. "
                "Primitive types store simple values, while reference variables "
                "refer to objects.",
                ["int age =  twentyFive;".replace("twentyFive", "25"),
                 "String name = \"Ada\";"],
                "Declare variables for a person's name, age, and whether they are enrolled.",
                "You practiced Java variables and the distinction between values and objects.",
            ),
            "your first exercise": (
                ["Write a class with a clear main method",
                 "Use variables and output to solve a small problem"],
                "A useful first Java exercise combines a class, the `main` method, "
                "variables, and `System.out.println`.",
                ["int width = 4;", "int height = 6;", "System.out.println(width * height);"],
                "Write a program that calculates and prints the area of a rectangle.",
                "You combined Java syntax into a small working program.",
            ),
        }.get(lesson)
        if content:
            objectives, explanation, examples, exercise, summary = content
            return LessonContentOut(
                objectives=objectives,
                explanation=explanation,
                examples=examples,
                exercise=exercise,
                summary=summary,
            )

    return LessonContentOut(
        objectives=[
            f"Explain {lesson_title} in the context of {module_title}",
            f"Apply {lesson_title} to a {course_topic} exercise",
        ],
        explanation=(
            f"This lesson covers {lesson_title}, part of {module_title} in {course_topic}. "
            f"At a {skill_level.value} level, focus on building an accurate mental "
            "model before optimizing for speed or edge cases. Start from a concrete "
            "example, then generalize the pattern."
        ),
        examples=[
            f"Example 1: identify {lesson_title} in a small {course_topic} example.",
            f"Example 2: combine {lesson_title} with a concept from {module_title}.",
        ],
        exercise=(
            f"Try it yourself: create a small {course_topic} example using "
            f"{lesson_title}, then explain why each step is needed."
        ),
        summary=f"You practiced {lesson_title} in the context of {course_topic}.",
    )
