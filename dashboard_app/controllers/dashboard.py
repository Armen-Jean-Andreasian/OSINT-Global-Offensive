from logger_app.controllers import LoggerController
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from project_components import ServiceResponse


class DashboardController:
    @staticmethod
    def get_loggers(user_id) -> "ServiceResponse":
        """Retrieves loggers of user and returns them"""
        return LoggerController.find_user_loggers(user_id)

    @staticmethod
    def create_logger(user_id, destination) -> "ServiceResponse":
        """Creates a logger"""
        return LoggerController.create(user_id=user_id, destination=destination)

