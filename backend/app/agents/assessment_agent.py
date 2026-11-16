def _mock_questions(topic: str, current_level: SkillLevel) -> AssessmentQuestionSet:
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
