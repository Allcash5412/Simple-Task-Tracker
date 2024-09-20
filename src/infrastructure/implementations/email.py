from typing import List
import asyncio

class EmailManager:

    async def send_email(self, to: str, subject: str, body: str):
        print(f'Mock email sent to: {to} | Subject: {subject} | Body: {body}')

    async def send_emails(self, receivers: List[str], subject: str, body: str):
        tasks = []
        for receiver in receivers:
            tasks.append(asyncio.create_task(self.send_email(receiver, subject, body)))
        await asyncio.gather(*tasks)
