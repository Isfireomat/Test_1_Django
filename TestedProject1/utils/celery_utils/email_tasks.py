# from typing import List
# import logging
# from django.core.mail import send_mail
# # from utils.celery_utils.connection import app
# from celery import shared_task
# # from connection import app

# logger = logging.getLogger(__name__)

# # @app.task
# # def add(x, y):
# #     return x + y

# # @app.task
# # def send_mail_password_reset_request(self,
# #                                      subject: str,
# #                                      message: str,
# #                                      from_email: str,
# #                                      recipient_list: List[str]
# #                                      ) -> None:
# #     try:
# #         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
# #         logger.info(f"Task {self.request.id} successful send email")
# #     except Exception as e:
# #         logger.error(f"Task {self.request.id} failed: {e}")
# #         raise self.retry(exc=e, countdown=60)