from enum import Enum


class UserRole(Enum):
    """ Role for user """
    ADMIN = 'Admin'
    PROJECT_MANAGER = 'Project Manager'
    TEAM_LEAD = 'Team Lead'
    DEVELOPER = 'Developer'
    QA = 'QA'
    USER = 'User'
    GUEST = 'Guest'


class TaskStatus(Enum):
    """ Task status """
    TODO = 'TODO'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'


class TaskPriority(Enum):
    """ Task priority """
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
