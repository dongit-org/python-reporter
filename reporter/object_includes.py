from reporter.objects import *

Activity._includes = {
    "assessment": Assessment,
    "finding": Finding,
    "user": User,
}

Assessment._includes = {
    "assessmentType": AssessmentType,
    "client": Client,
    "documents": Document,
    "findings": Finding,
    "phases": AssessmentPhase,
    "researchersOnReport": User,
    "targets": Target,
    "users": User,
}

Client._includes = {
    "assessments": Assessment,
    "documents": Document,
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
    "documents": Document,
    "resolvedTargets": Target,
    "resolvers": User,
    "targets": Target,
    "user": User,
}

Target._includes = {
    "assessment": Assessment,
    "documents": Document,
    "findings": Finding,
}

User._includes = {
    "assessments": Assessment,
    "clients": Client,
    "documents": Document,
}
