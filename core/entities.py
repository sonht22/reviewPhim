from dataclasses import dataclass

@dataclass
class TimeRange:
    start: str  # Format "HH:MM:SS"
    end: str    # Format "HH:MM:SS"

@dataclass
class RecapSegment:
    id: int
    script: str
    visual_time: TimeRange
    visual_description: str