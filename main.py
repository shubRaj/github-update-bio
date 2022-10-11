import requests
from dotenv import load_dotenv
import os
import json
from custom_exceptions import TokenNotFound
import pytz
import datetime
load_dotenv()


class Github:
    __HOST = "https://api.github.com/user"

    def __init__(self):
        self.__session = requests.session()

    def get_session(self):
        return self.__session

    def close(self):
        return self.get_session().close()

    def get_token(self):
        token = os.getenv("TOKEN", None)
        if token is not None:
            return token
        raise TokenNotFound

    def get_headers(self):
        return {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {self.get_token()}"}

    def whoami(self):
        return self.get_session().get(self.__HOST, headers=self.get_headers()).json()

    def update_bio(self, bio):
        whoami = self.whoami()
        body = {
            "name": whoami["name"],
            "email": whoami["email"],
            "blog": whoami["blog"],
            "twitter_username": whoami["twitter_username"],
            "company": whoami["company"],
            "location": whoami["location"],
            "hireable": whoami["hireable"],
            "bio": bio
        }
        return self.get_session().patch(self.__HOST, headers=self.get_headers(), data=json.dumps(body)).json()
if __name__ == '__main__':
    github = Github()
    timezone = pytz.timezone('Asia/Kathmandu')
    dt = datetime.datetime.now(timezone)
    github.update_bio(f"I only code at {dt.strftime('%-I %p')} "+"{GMT+5:45}" )