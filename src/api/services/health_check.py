import datetime
import os

from fastapi import Depends
from git import Repo
from sqlalchemy.exc import SQLAlchemyError
from telegram.ext import Application

from src.api.constants import DATE_TIME_FORMAT
from src.api.schemas import BotStatus, CommitStatus, DBStatus, HealthCheck
from src.bot import init_bot
from src.bot.bot import create_bot
from src.core.db.repository import TaskRepository
from src.depends import Container
from src.settings import settings


class HealthCheckService:
    """Сервис для проверки работы бота."""

    def __init__(
        self,
        task_repository: TaskRepository = Depends(),
    ) -> None:
        self._repository: TaskRepository = task_repository
        self._container = Container()
        self._bot = init_bot(self._container.telegram_bot())

    async def check_bot(self) -> BotStatus:
        try:
            webhook_info = await self._bot.bot.get_webhook_info()
            if settings.BOT_WEBHOOK_MODE:
                bot_status: BotStatus = {"status": True, "method": "webhooks", "url": webhook_info.url}
                return bot_status
            else:
                bot_status: BotStatus = {"status": True, "method": "pulling"}
                return bot_status
        except Exception as exc:
            bot_status: BotStatus = {"status": False, "error": f"{exc}"}
            return bot_status

    async def get_last_commit(self) -> CommitStatus:
        repo = Repo(os.getcwd())
        master = repo.head.reference
        commit_date = datetime.datetime.fromtimestamp(master.commit.committed_date)
        commit_status: CommitStatus = {
            "last_commit": str(master.commit)[:7],
            "commit_date": commit_date.strftime(DATE_TIME_FORMAT),
            "tags": repo.tags,
        }
        return commit_status

    async def check_db_connection(self) -> DBStatus:
        try:
            active_tasks = await self._repository.count_active_all()
            get_last_update = await self._repository.get_last_update()
            if get_last_update is None:
                get_last_update = 0
            db_status: DBStatus = {
                "status": True,
                "last_update": get_last_update,
                "active_tasks": active_tasks,
            }
            return db_status
        except SQLAlchemyError as exc:
            db_status: DBStatus = {"status": False, "db_connection_error": f"{exc}"}
            return db_status
