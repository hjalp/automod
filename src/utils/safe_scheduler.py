from datetime import datetime, timedelta
import logging
from traceback import format_exc
from schedule import Scheduler

logger = logging.getLogger('schedule')

class SafeScheduler(Scheduler):
    def __init__(self, reschedule_on_failure = True, minutes_after_failure = 0, seconds_after_failure = 0):
        self.reschedule_on_failure = reschedule_on_failure
        self.minutes_after_failure = minutes_after_failure
        self.seconds_after_failure = seconds_after_failure
        super().__init__()

    def run_job(self, job):
        try:
            super()._run_job(job)
        except Exception:
            self._logger.error(format_exc())
            if(self.reschedule_on_failure):
                if(self.minutes_after_failure!=0 or self.seconds_after_failure!=0):
                    self._logger.warn("Rescheduled in %s minutes and %s seconds." % (self.minutes_after_failure, self.seconds_after_failure))
                    job.last_run = None
                    job.next_run = datetime.now() + timedelta(minutes=self.minutes_after_failure, seconds=self.seconds_after_failure)
                else:
                    self._logger.warn("Rescheduled.")
                    job.last_run = datetime.now()
                    job._schedule_next_run()
            else:
                self._logger.warn("Job canceled.")
                self.cancel_job(job)