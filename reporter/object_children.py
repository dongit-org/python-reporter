"""RestObject _includes - see RestObject.__init__"""

# pylint: disable = wildcard-import, unused-wildcard-import, protected-access

from reporter.objects import *

Assessment._children = {
    "comments": AssessmentAssessmentCommentManager,
    "findings": AssessmentFindingManager,
    "output_files": AssessmentOutputFileManager,
    "targets": AssessmentTargetManager,
    "tasks": AssessmentTaskManager,
    "task_sets": AssessmentTaskSetManager,
    "users": AssessmentAssessmentUserManager,
}

AssessmentComment._children = {
    "replies": AssessmentCommentReplyManager,
}

AssessmentSection._children = {
    "comments": AssessmentSectionAssessmentSectionCommentManager,
}

AssessmentSectionComment._children = {
    "replies": AssessmentSectionEventReplyManager,
}

Client._children = {
    "assessments": ClientAssessmentManager,
    "user_groups": ClientUserGroupManager,
}

Finding._children = {
    "comments": FindingFindingCommentManager,
    "retests": FindingFindingRetestManager,
    "retestInquiries": FindingFindingRetestInquiryManager,
}

FindingComment._children = {
    "replies": FindingEventReplyManager,
}

FindingRetest._children = {
    "replies": FindingEventReplyManager,
}

FindingRetestInquiry._children = {
    "replies": FindingEventReplyManager,
}
