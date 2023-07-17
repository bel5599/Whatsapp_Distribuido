from pydantic import BaseModel


class MessagesModel(BaseModel):
    source: str
    destiny: str
    value: str
    database_id: int
    id:int


class UserModel(BaseModel):
    nickname: str
    password: str
    ip: str
    port: str
    database_id: int

class UserUpdate(BaseModel):
    nickname: str
    ip: str
    port: str
    database_id: int


class DataBaseModel(BaseModel):
    database_id: int


class SearchMessagesModel(BaseModel):
    destiny: str
    database_id: int


class NicknameEntityBaseModel(BaseModel):
    search_id: int


class DataUsersModel(BaseModel):
    nickname: str
    password: str
    ip: str
    port: str

    def serialize(self):
        return {
            'nickname': self.nickname,
            'password': self.password,
            'ip': self.ip,
            'port': self.port
        }


class DataMessagesModel(BaseModel):
    message_id: int
    user_id_from: str
    user_id_to: str
    value: str

    def serialize(self):
        return {
            'message_id': self.message_id,
            'user_id_from': self.user_id_from,
            'user_id_to': self.user_id_to,
            'value': self.value,
        }


class DataBaseUserModel(BaseModel):
    users: list[DataUsersModel]
    messages: list[DataMessagesModel]

    def serialize(self):
        return {
            'users': [user.serialize() for user in self.users],
            'messages': [message.serialize() for message in self.messages]
        }


class CopyDataBaseModel(BaseModel):
    source: DataBaseUserModel
    database_id: int
