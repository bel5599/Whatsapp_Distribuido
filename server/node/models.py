from pydantic import BaseModel


class MessengesModel(BaseModel):
    source: str
    destiny: str
    value: str
    database_id: int


class UserModel(BaseModel):
    nickname: str
    password: str
    ip: str
    port: str
    database_id: int


class DataBaseModel(BaseModel):
    database_id: int


class SearchMessengesModel(BaseModel):
    source: str
    destiny: str
    database_id: int


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


class DataMessengesModel(BaseModel):
    messenge_id: int
    user_id_from: str
    user_id_to: str
    value: str

    def serialize(self):
        return {
            'messenge_id': self.messenge_id,
            'user_id_from': self.user_id_from,
            'user_id_to': self.user_id_to,
            'value': self.value,
        }


class DataBaseUserModel(BaseModel):
    users: list[DataUsersModel]
    messenges: list[DataMessengesModel]

    def serialize(self):
        return {
            'users': self.users,
            'messenges': self.messenges
        }


class CopyDataBaseModel(BaseModel):
    source: DataBaseUserModel
    database_id: int
