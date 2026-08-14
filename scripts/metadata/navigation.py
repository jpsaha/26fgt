def sort_lectures(lectures):
    """Sort lectures by lecture number."""

    lectures.sort(
        key=lambda lecture: (
            str(
                lecture.get(
                    "category",
                    "Uncategorized",
                )
            ).casefold(),

            lecture.get("number") is None,

            lecture.get("number")
            if lecture.get("number") is not None
            else 10**9,

            lecture.get("file"),
        )
    )


def add_navigation(lectures):
    """
    Add previous/next links within each category.
    Add previous/next links to numbered lectures.

    Non-numbered pages are not included.

    Lecture numbers are category-local and therefore
    navigation never crosses category boundaries.
    """

    categories = {}

    for lecture in lectures:

        if lecture.get("number") is None:
            continue

        category = lecture.get(
            "category",
            "Uncategorized",
        )

        categories.setdefault(
            category,
            [],
        ).append(
            lecture
        )

    for category_lectures in categories.values():

        category_lectures.sort(
            key=lambda lecture: (
                lecture.get("number"),
                lecture.get("file"),
            )
        )

        for index, lecture in enumerate(
            category_lectures
        ):

            if index > 0:

                previous = category_lectures[
                    index - 1
                ]

                lecture["previous"] = {
                    "title": previous["title"],
                    "html": (
                        previous["file"]
                        + ".html"
                    ),
                }

            else:

                lecture["previous"] = None

            if index < len(category_lectures) - 1:

                next_lecture = category_lectures[
                    index + 1
                ]

                lecture["next"] = {
                    "title": next_lecture["title"],
                    "html": (
                        next_lecture["file"]
                        + ".html"
                    ),
                }

            else:

                lecture["next"] = None


def add_page_navigation(pages):
    """
    Pages currently do not participate
    in lecture navigation.
    """

    for page in pages:

        page["previous"] = None
        page["next"] = None
