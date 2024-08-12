from typing import cast

import pytest

from reporter import Reporter, AssessmentComment


@pytest.fixture(scope="session")
def assessment_comment(rc: Reporter) -> AssessmentComment:
    client = rc.clients.create(
        {
            "name": "test_reaction",
            "description": "foo",
        }
    )
    assessment_template = rc.assessment_templates.list()[0]
    assessment = client.assessments.create(
        {
            "title": "test_reaction",
            "assessment_template_id": assessment_template.id,
        }
    )
    return cast(
        AssessmentComment,
        assessment.comments.create(
            {
                "body": "Hello world!",
                "is_private": True,
            }
        ),
    )


def test_reaction_operations(
    rc: Reporter, assessment_comment: AssessmentComment
) -> None:
    assessment = rc.assessments.get(assessment_comment.assessment_id)

    reaction = rc.reactions.create(
        {
            "model_type": "AssessmentComment",
            "model_id": assessment_comment.id,
            "reaction": "👍",
        }
    )

    assessment = rc.assessments.get(
        assessment_comment.assessment_id, include=["comments.reactions"]
    )
    reaction = assessment.comments[-1].reactions[-1]
    assert reaction.reaction == "👍"

    # # Uncomment in next version
    # rc.reactions.delete(reaction.id)
    #
    # assessment = rc.assessments.get(
    #     assessment_comment.assessment_id, include=["comments.reactions"]
    # )
    #
    # assert len(assessment.comments[-1].reactions) == 0
