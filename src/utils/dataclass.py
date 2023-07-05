from dataclasses import dataclass
from typing import Optional

@dataclass
class PostSchedule:
    community: str
    title: str
    frequency_unit: str
    # feature: boolean = 0
    frequency: int = 1
    content: Optional[str] = None
    external_link: Optional[str] = None
    day: Optional[str] = None
    time: Optional[str] = None
