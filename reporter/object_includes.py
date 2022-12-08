"""RestObject _includes - see RestObject._deserialize_includes"""

# pylint: disable = wildcard-import, unused-wildcard-import, protected-access

from reporter.objects import *

Activity._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "user": User,
}

Assessment._includes = {
    "assessmentTemplate": AssessmentTemplate,
    "assessmentUsers": AssessmentUser,
    "client": Client,
    "documents": Document,
    "findings": Finding,
    "nestedSections": AssessmentSection,
    "outputFiles": OutputFile,
    "phases": AssessmentPhase,
    "researchersOnReport": User,
    "sections": AssessmentSection,
    "targets": Target,
    "tasks": Task,
    "taskSets": TaskSet,
    "userGroups": UserGroup,
    "users": User,
}

AssessmentPhase._includes = {
    "assessment": Assessment,
    "researchers": User,
    "reviewers": User,
}

AssessmentSection._includes = {
    "assessment": Assessment,
    "documents": User,
    "findings": User,
    "items": AssessmentSection,
}

AssessmentTemplate._includes = {
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

Document._includes = {
    "uploadedBy": User,
}

FindingTemplate._includes = {
    "documents": Document,
}

Finding._includes = {
    "assessment": Assessment,
    "assessmentSection": AssessmentSection,
    "documents": Document,
    "resolvedTargets": Target,
    "resolvers": User,
    "targets": Target,
    "userGroups": UserGroup,
    "user": User,
}

OutputFile._includes = {
    "assessment": Assessment,
    "documents": Document,
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
