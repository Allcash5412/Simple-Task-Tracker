import logging
from typing import Sequence

from fastapi import APIRouter

from src.db.models import User
from src.api.routes.task_tracker.dto import APIUpdateTask
from src.services.task_tracker.dto import CreatedTask, UpdatedTask, DeletedTask, CreateTask
from src.infrastructure.implementations.email import EmailManager

from src.services.task_tracker.services import CreateTaskService, UpdateTaskService, DeleteTaskService


from src.api.routes.task_tracker.dependencies import TaskRepositoryDep
from src.api.routes.dependencies import CurrentUser, UserRepositoryDep
from src.api.routes.task_tracker.dto import APICreateTask

task_tracker = APIRouter(prefix='/task_tracker')
logger = logging.getLogger('app')


@task_tracker.post('/create_task/')
async def create_task(current_user: CurrentUser, task: APICreateTask,
                      user_repository: UserRepositoryDep, task_repository: TaskRepositoryDep):

    create_task_service = CreateTaskService(current_user, user_repository, task_repository, task)
    created_task: CreatedTask = await create_task_service.create_task()

    created_task_assignees = created_task.__dict__.pop('assignees')

    try:
        email_manager: EmailManager = EmailManager()
        assignees_emails = [assignee.email for assignee in created_task_assignees]
        await email_manager.send_emails(assignees_emails, 'Task Created!', f'Task: {created_task.name} has been created!')
    except Exception as e:
        logger.error(e)
    return created_task


@task_tracker.put('/update_task/{task_id}')
async def update_task(task_id: int, current_user: CurrentUser, task: APIUpdateTask,
                      user_repository: UserRepositoryDep, task_repository: TaskRepositoryDep):

    update_task_service = UpdateTaskService(current_user, user_repository,
                                            task_repository, task, task_id)
    updated_task: UpdatedTask = await update_task_service.update_task()
    logger.debug(f'updated_task = {updated_task}')

    updated_task_dict = updated_task.__dict__

    updated_task_responsible_person: User = updated_task_dict.pop('responsible_person')
    updated_task_assignees: Sequence[User] = updated_task_dict.pop('assignees')

    email_manager: EmailManager = EmailManager()
    if updated_task_assignees:
        emails_to_notify = [assignee.email for assignee in updated_task_assignees]
        emails_to_notify.append(updated_task_responsible_person.email)

        await email_manager.send_emails(emails_to_notify, 'Task Changed!', f'Task: "{updated_task.name}" updated!')

    return updated_task


@task_tracker.delete('/delete_task/{task_id}')
async def delete_task(task_id: int, current_user: CurrentUser, user_repository: UserRepositoryDep, task_repository: TaskRepositoryDep):

    delete_task_service = DeleteTaskService(current_user, user_repository,
                                            task_repository, task_id)

    deleted_task: DeletedTask = await delete_task_service.delete_task()


    email_manager: EmailManager = EmailManager()
    deleted_task_assignees = deleted_task.__dict__.pop('assignees')

    emails_to_notify = [assignee.email for assignee in deleted_task_assignees]

    await email_manager.send_emails(emails_to_notify, 'Task Changed!', f'Task: "{deleted_task.name}" deleted!')

    return deleted_task

