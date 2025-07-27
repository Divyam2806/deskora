from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import Session as SessionType
from assistant.database import Base, Session

class Setting(Base):
    __tablename__ = "settings"
    key = Column(String, primary_key=True)
    value = Column(Boolean, nullable=False)

def get_setting(key: str) -> bool:
    session: SessionType = Session()
    setting = session.query(Setting).filter_by(key=key).first()
    session.close()
    return setting.value if setting else False

def set_setting(key: str, value: bool):
    session: SessionType = Session()
    setting = session.query(Setting).filter_by(key=key).first()
    if setting:
        setting.value = value
    else:
        setting = Setting(key=key, value=value)
        session.add(setting)
    session.commit()
    session.close()

def initialize_default_settings():
    for key in ["listening_enabled", "speaking_enabled"]:
        if not setting_exists(key):
            set_setting(key, False)

def setting_exists(key: str) -> bool:
    session: SessionType = Session()
    exists = session.query(Setting).filter_by(key=key).first() is not None
    session.close()
    return exists
