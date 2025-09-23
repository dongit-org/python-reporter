"""RestObject _includes - see RestObject._deserialize_includes"""
# pylint: disable = wildcard-import, unused-wildcard-import, protected-access

from reporter.objects import *

Activity._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "impersonator": User,
    "user": User,
}

Assessment._includes = {
    "activities": Activity,
    "assessmentTemplate": AssessmentTemplate,
    "assessmentUsers": AssessmentUser,
    "client": Client,
    "comments": AssessmentComment,
    "documents": Document,
    "findings": Finding,
    "findingLayout": FindingLayout,
    "language": Language,
    "nestedSections": AssessmentSection,
    "outputFiles": OutputFile,
    "phases": AssessmentPhase,
    "researchersOnReport": User,
    "sections": AssessmentSection,
    "targets": Target,
    "tasks": Task,
    "taskSets": TaskSet,
    "testCases": TestCase,
    "theme": Theme,
    "userGroups": UserGroup,
    "users": User,
}

AssessmentComment._includes = {
    "assessment": Assessment,
    "createdBy": User,
    "updatedBy": User,
    "documents": Document,
    "reactions": Reaction,
    "replies": AssessmentComment,
}

AssessmentPhase._includes = {
    "assessment": Assessment,
    "researchers": User,
    "reviewers": User,
}

AssessmentSection._includes = {
    "assessment": Assessment,
    "documents": User,
    "findings": Finding,
    "items": AssessmentSection,
    "comments": AssessmentSectionComment,
}

AssessmentSectionComment._includes = {
    "assessment": Assessment,
    "assessmentSection": AssessmentSection,
    "createdBy": User,
    "updatedBy": User,
    "documents": Document,
    "replies": AssessmentSectionComment,
}

AssessmentTemplate._includes = {
    "languages": Language,
    "taskSets": TaskSet,
}

AssessmentUser._includes = {
    "assessment": Assessment,
    "autoAssignments": AutoAssignment,
    "roles": Role,
    "user": User,
}

AutoAssignment._includes = {
    "assessment": Assessment,
    "user": User,
}

Client._includes = {
    "assessments": Assessment,
    "documents": Document,
    "userGroups": UserGroup,
    "users": User,
}

CustomField._includes = {
    "documents": Document,
}

Document._includes = {
    "uploadedBy": User,
}

FindingComment._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "createdBy": User,
    "updatedBy": User,
    "documents": Document,
    "parent": FindingEvent,
    "reactions": Reaction,
    "replies": FindingComment,
}

FindingImportEvent._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "createdBy": User,
    "users": User,
}

FindingCreatedEvent._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "createdBy": User,
    "replies": FindingComment,
    "reactions": Reaction,
    "resolvedTargets": Target,
}

FindingLayout._includes = {
    "assessments": Assessment,
    "fields": FindingLayoutField,
}

FindingLayoutField._includes = {
    "findingLayout": FindingLayout,
}

FindingPublishedEvent._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "createdBy": User,
    "updatedBy": User,
    "relatedEvent": FindingEvent,
    "parent": FindingEvent,
}

FindingResolverEvent._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "createdBy": User,
    "replies": FindingComment,
    "addedUsers": User,
    "removedUsers": User,
}

FindingRetest._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "relatedEvents": FindingEvent,
    "relatedEvent": FindingEvent,
    "createdBy": User,
    "updatedBy": User,
    "reviewedBy": User,
    "documents": Document,
    "reactions": Reaction,
    "retestInquiry": FindingRetestInquiry,
    "replies": FindingComment,
    "resolvedTargets": Target,
    "nextStatusChange": FindingEvent,
    "previousStatusChange": FindingEvent,
}

FindingRetestCancelledEvent._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "relatedEvent": FindingEvent,
    "createdBy": User,
    "updatedBy": User,
    "documents": Document,
    "retestInquiry": FindingRetestInquiry,
    "replies": FindingComment,
    "resolvedTargets": Target,
    "nextStatusChange": FindingEvent,
    "previousStatusChange": FindingEvent,
}

FindingRetestInquiry._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "createdBy": User,
    "updatedBy": User,
    "relatedEvents": FindingEvent,
    "convertedFromCommentBy": User,
    "documents": Document,
    "reactions": Reaction,
    "retest": FindingRetest,
    "replies": FindingComment,
    "resolvedTargets": Target,
    "nextStatusChange": FindingEvent,
    "previousStatusChange": FindingEvent,
}

FindingReviewEvent._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "createdBy": User,
    "updatedBy": User,
    "findingRetest": User,
    "relatedEvents": FindingEvent,
    "parent": FindingEvent,
}

FindingStatusChange._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "createdBy": User,
    "updatedBy": User,
    "nextStatusChange": FindingEvent,
    "previousStatusChange": FindingEvent,
    "resolvedTargets": Target,
}

FindingTemplate._includes = {
    "documents": Document,
}

Finding._includes = {
    "activities": Activity,
    "allComments": FindingComment,
    "allEvents": FindingEvent,
    "assessment": Assessment,
    "assessmentSection": AssessmentSection,
    "comments": FindingComment,
    "createdEvent": FindingCreatedEvent,
    "documents": Document,
    "events": FindingEvent,
    "importEvents": FindingImportEvent,
    "importedFrom": Finding,
    "importedTo": Finding,
    "publishedEvents": FindingPublishedEvent,
    "resolvedTargets": Target,
    "resolvers": User,
    "resolverEvents": FindingResolverEvent,
    "retestCancelledEvents": FindingRetestCancelledEvent,
    "retestInquiries": FindingRetestInquiry,
    "retests": FindingRetest,
    "reviewEvents": FindingReviewEvent,
    "statusChanges": FindingStatusChange,
    "targets": Target,
    "testCases": TestCase,
    "toolFindings": ToolFinding,
    "userGroups": UserGroup,
    "user": User,
}

Language._includes = {
    "assessments": Assessment,
}

OutputFile._includes = {
    "assessment": Assessment,
    "documents": Document,
    "toolFindings": ToolFinding,
}

Reaction._includes = {
    "assessment": Assessment,
    "user": User,
}

ReportPage._includes = {
    "customField": CustomField,
    "theme": Theme,
}

Target._includes = {
    "assessment": Assessment,
    "documents": Document,
    "findings": Finding,
}

Task._includes = {
    "assessment": Assessment,
    "client": Client,
    "completedBy": User,
    "finding": Finding,
    "taskSet": TaskSet,
    "users": User,
}

TaskSet._includes = {
    "assessments": Assessment,
    "assessmentTemplates": AssessmentTemplate,
    "copiedTasks": Task,
}

TestCase._includes = {
    "assessment": Assessment,
    "findings": Finding,
    "updatedBy": User,
}

Theme._includes = {
    "assessments": Assessment,
    "assessmentTemplates": AssessmentTemplate,
    "documents": Document,
    "languages": Language,
    "pages": ReportPage,
}

ToolFinding._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "importStatusBy": User,
    "outputFile": OutputFile,
    "toolTargetInfos": ToolFindingTargetInfo,
    "toolTargets": ToolTarget,
}

ToolTarget._includes = {
    "assessment": Assessment,
    "target": Target,
    "toolFindings": ToolFinding,
}

User._includes = {
    "assessments": Assessment,
    "clients": Client,
    "documents": Document,
    "roles": Role,
    "tasks": Task,
    "userGroups": UserGroup,
}

UserGroup._includes = {
    "assessments": Assessment,
    "client": Client,
    "users": User,
    "findings": Finding,
}
