import re

REGEX_VALID_TITLE = re.compile(r".*\S{3,}.*")
REGEX_VALID_TIME_24H = re.compile(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")
REGEX_VALID_TIME_SHORT = re.compile(r"^:[0-5][0-9]$")

def validate_title(title: str) -> str:
    if len(title) >= 200:
        return title[:196] + '...'
    elif not REGEX_VALID_TITLE.match(title):
        return title.rstrip() + '...'
    else:
        return title
    
def validate_time(time: str, mode: int) -> str:
    if mode == 24 and REGEX_VALID_TIME_24H.match(time):
        return time
    elif mode == 0 and REGEX_VALID_TIME_SHORT.match(time):
        return time
    elif mode == 24 and not REGEX_VALID_TIME_24H.match(time):
        return '00:00'
    elif mode == 0 and not REGEX_VALID_TIME_SHORT.match(time):
        return ':00'