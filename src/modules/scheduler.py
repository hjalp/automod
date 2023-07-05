import functools
import logging
import schedule

from pythorhead import Lemmy
from utils import validate_title, validate_time
from utils.dataclass import PostSchedule
from utils.safe_scheduler import SafeScheduler

VALID_DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

class Scheduler:
    def __init__(self, scheduler: SafeScheduler, uri: str, timezone: str, username: str, password: str):

        self._lemmy = Lemmy(uri)
        self._logger: logging.Logger = logging.getLogger(__name__)
        self._scheduler: SafeScheduler = scheduler
        self._timezone = timezone
        self._username = username
        self._password = password

    def schedule_posts(self, scheduled_posts: dict):

        post_details = []

        for i in range(len(scheduled_posts)):
            post = self._parse_config(scheduled_posts[i])
            post_details.append(post)

            def post_job(index):
                post = post_details[index]

                self._lemmy.log_in(self._username, self._password)
                community_id = self._lemmy.discover_community(post.community)
                self._lemmy.post.create(
                    community_id=community_id,
                    name=post.title,
                    url=post.external_link,
                    body=post.content,
                )

                print(f'{post.title} was posted. It will be posted again at:')
                print(self._scheduler.get_next_run(str(index)))

            job = schedule.Job(interval=post.frequency,scheduler=self._scheduler)

            job.unit = post.frequency_unit
            job.start_day = post.day
            job.at(time_str=post.time, tz=self._timezone)
            job.do(post_job, index=i)
            job.tag(str(i))
        
        print('The following scheduled posts were queued:')
        print(self._scheduler.get_jobs())
                

    def _parse_config(self, scheduled_post: dict) -> PostSchedule:           
        post = PostSchedule(
            community=scheduled_post['community'],
            title=validate_title(scheduled_post['title']),
            frequency_unit=scheduled_post['frequency_unit'],
            content=scheduled_post['content'],
            external_link=scheduled_post['external_link']
        )

        post.frequency = scheduled_post['frequency'] if not scheduled_post['frequency'] == None and scheduled_post['frequency'] > 1 else 1

        if scheduled_post['frequency_unit'].lower() == 'weeks':
            if scheduled_post['day'].lower() in VALID_DAYS:
                post.day = scheduled_post['day'].lower()
            else:
                post.day = 'monday'

        if scheduled_post['frequency_unit'].lower() == 'days' or scheduled_post['frequency_unit'].lower() == 'weeks':
            post.time = validate_time(scheduled_post['time'], mode=24)
        elif scheduled_post['frequency_unit'].lower() == 'minutes' or scheduled_post['frequency_unit'].lower() == 'hours':
            post.time = validate_time(scheduled_post['time'], mode=0)

        return post