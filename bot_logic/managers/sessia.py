from datetime import datetime
# from ..objects.user import User

class Sessia():
    def __init__(self, *, bot):
        self._start = datetime.today()
        self._bot = bot
        # self._users: dict[int, User] = {}
    
    def add_user(self, user_id: int):
        # self._users[user_id] = User(user_id=user_id)
        ...
    
    def get_user(self, user_id: int):
        if self._users[user_id]:
            return self._users[user_id]
        else:
            self.add_user(user_id=user_id)
            return self._users[user_id]
    
    def forget_user(self, user_id: int):
        del self._users[user_id]