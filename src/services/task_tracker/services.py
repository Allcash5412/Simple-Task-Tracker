import logging
from fastapi import HTTPException
from typing import Tuple, Sequence, Optional, Dict

from src.db.models import User, Task
from src.services.task_tracker.dto import DeletedTask
from src.services.task_tracker.dto import CreatedTask, UpdatedTask, UpdateTask
from src.exceptions import get_exception_404_not_found_with_detail
from src.domain.task_tracker.entities import TaskBase
from src.exceptions import get_exception_400_bad_request_with_detail
from src.services.auth.interfaces import AbstractUserRepository
from src.services.task_tracker.dto import CreateTask
from src.db.enums import UserRole

from src.domain.auth.entities import UserBase

from src.exceptions import get_exception_403_forbidden_with_detail

from src.services.task_tracker.interfaces import AbstractTaskRepository
from src.services.task_tracker.interfaces import AbstractAPIUpdateTask, AbstractAPICreateTask
from src.services.auth.services import UserValidationService


logger = logging.getLogger('app')


class TaskMixin:

    async def _get_responsible_person_or_error(self, user_id: int) -> User | HTTPException:
        responsible_person: User = await self.user_repository.get_user_model_by(id=user_id)

        if not responsible_person:
            raise get_exception_400_bad_request_with_detail('Responsible user not found!')

        return responsible_person

    async def _get_task_or_error(self, task_id: int) -> Task | HTTPException:
        exist_task: Task = await self.task_repository.get_task_model_by({'id': task_id})

        if not exist_task:
            raise get_exception_404_not_found_with_detail('Task user not found!')

        return exist_task


class CreateTaskService(TaskMixin):

    def __init__(self, user: UserBase,
                 user_repository: AbstractUserRepository,
                 task_repository: AbstractTaskRepository, task_to_create: AbstractAPICreateTask):

        self.user: UserBase = user
        self.user_repository: AbstractUserRepository = user_repository
        self.task_repository: AbstractTaskRepository = task_repository
        self.task_to_create: AbstractAPICreateTask = task_to_create

    async def create_task(self) -> CreatedTask:
        await self._checks_to_create_task()

        responsible_person: User = await self._get_responsible_person_or_error(self.task_to_create.responsible_person_id)
        assignees: Sequence[User] = await self.user_repository.get_users_by_ids(self.task_to_create.assignees_ids)

        try:
            task = CreateTask(
                name=self.task_to_create.name,
                description=self.task_to_create.description,
                responsible_person=responsible_person.id,
                status=self.task_to_create.status,
                priority=self.task_to_create.priority,
                assignees=assignees
            )

            task_base: TaskBase = await self.task_repository.create_task(task)
            created_task: CreatedTask = CreatedTask(**task_base.__dict__)

            await self.task_repository.commit()
            return created_task

        except Exception as e:
            logger.error(e)

    async def _checks_to_create_task(self) -> Optional[HTTPException]:
        task_validation_service = TaskValidationService(self.task_repository)
        self._check_role_to_create_task()
        await task_validation_service.check_on_exist_task_by_name(self.task_to_create.name)

    def _check_role_to_create_task(self) -> bool | HTTPException:
        available_roles: Tuple[UserRole, UserRole, UserRole] = (
            UserRole.ADMIN, UserRole.TEAM_LEAD, UserRole.PROJECT_MANAGER)
        check_result: bool = UserValidationService.check_role_for_access_to_action(self.user.role, available_roles)

        if check_result:
            raise get_exception_403_forbidden_with_detail('Users does not have the permissions to create task!')

        return True


class UpdateTaskService(TaskMixin):

    def __init__(self, user: UserBase,
                 user_repository: AbstractUserRepository,
                 task_repository: AbstractTaskRepository, task_to_update: AbstractAPIUpdateTask,
                 task_id: int):

        self.user: UserBase = user
        self.user_repository: AbstractUserRepository = user_repository
        self.task_repository: AbstractTaskRepository = task_repository
        self.task_to_update: AbstractAPIUpdateTask = task_to_update
        self.task_id: int = task_id

    async def update_task(self) -> UpdatedTask:

        await self._checks_to_update_task()

        assignees_to_update: Optional[Sequence[User]] = await self._get_assignees_to_update()
        data_for_update: Dict = self.task_to_update.model_dump(exclude_unset=True)

        responsible_person_id: int = data_for_update.pop('responsible_person_id', None)

        data_for_update.pop('assignees_ids', None)

        logger.debug(f'self.task_to_update = {self.task_to_update}')
        logger.debug(f'data_for_update = {data_for_update}')


        update_task = UpdateTask(
            **data_for_update
        )

        if assignees_to_update:
            update_task.assignees = assignees_to_update

        if responsible_person_id:
            update_task.responsible_person = responsible_person_id
            logger.debug(f'update_task = {update_task}')

        await self.task_repository.update_task_by_id(self.task_id, update_task.model_dump(exclude_unset=True))
        updated_task: Task = await self._get_task_or_error(self.task_id)
        responsible_person = await self._get_responsible_person_or_error(updated_task.responsible_person)

        logger.debug(f'updated_task type(Task) = {updated_task}')
        updated_task: UpdatedTask = UpdatedTask(name=updated_task.name,
                                            responsible_person=responsible_person,
                                            assignees=updated_task.assignees)

        await self.task_repository.commit()

        return updated_task

    async def _get_assignees_to_update(self) -> Optional[Sequence[User]]:
        assignees_ids = self.task_to_update.assignees_ids
        assignees = None
        if assignees_ids:
            assignees: Sequence[User] = await self.user_repository.get_users_by_ids(self.task_to_update.assignees_ids)
        return assignees

    async def _checks_to_update_task(self) -> Optional[HTTPException]:
        task_validation_service = TaskValidationService(self.task_repository)
        self._check_role_to_update_task()
        await task_validation_service.check_on_exist_task_by_id(self.task_id)
        await task_validation_service.check_on_exist_task_by_name(self.task_to_update.name)

    def _check_role_to_update_task(self) -> bool | HTTPException:
        available_roles: Tuple[UserRole] = tuple(role for role in UserRole if role != role.GUEST)
        check_result: bool = UserValidationService.check_role_for_access_to_action(self.user.role, available_roles)
        if check_result:
            raise get_exception_403_forbidden_with_detail('You do not have the permissions to update task!')
        return True


class DeleteTaskService:

    def __init__(self, user: UserBase,
                 user_repository: AbstractUserRepository,
                 task_repository: AbstractTaskRepository,
                 task_id: int):

        self.user: UserBase = user
        self.user_repository: AbstractUserRepository = user_repository
        self.task_repository: AbstractTaskRepository = task_repository
        self.task_id: int = task_id

    async def delete_task(self) -> DeletedTask:
        self._check_role_to_delete_task()

        task_to_delete: Task = await self.task_repository.get_task_model_by({'id': self.task_id})
        if not task_to_delete:
            raise get_exception_404_not_found_with_detail(f'Task with id: {self.task_id} does not exist!')

        await self.task_repository.delete_task_by({'id': self.task_id})

        deleted_task = DeletedTask(
            name=task_to_delete.name,
            assignees=task_to_delete.assignees
        )
        await self.task_repository.commit()
        return deleted_task


    def _check_role_to_delete_task(self) -> bool | HTTPException:
        available_roles: Tuple[UserRole, UserRole, UserRole] = (UserRole.ADMIN, UserRole.PROJECT_MANAGER, UserRole.TEAM_LEAD)
        check_result: bool = UserValidationService.check_role_for_access_to_action(self.user.role, available_roles)
        if check_result:
            raise get_exception_403_forbidden_with_detail('You do not have the permissions to delete task!')
        return True


class TaskValidationService:

    def __init__(self, task_repository: AbstractTaskRepository):
        self.task_repository: AbstractTaskRepository = task_repository

    async def check_on_exist_task_by_name(self, task_name: str) -> HTTPException | bool:
        check_on_exiting_task = await self.task_repository.get_task_by({'name': task_name})
        if check_on_exiting_task:
            raise get_exception_400_bad_request_with_detail(f'Task with this name already exists!')
        return False

    async def check_on_exist_task_by_id(self, task_id: int) -> HTTPException | bool:
        task: TaskBase = await self.task_repository.get_task_by({'id': task_id})
        if not task:
            raise get_exception_404_not_found_with_detail(f'Task with id: {task_id} not found!')
        return False
