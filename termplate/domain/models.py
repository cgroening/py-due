from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Config:
    example_setting: int = 3
    another_setting: list[int] | None = None


@dataclass
class Task:
    title: str
    done: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
