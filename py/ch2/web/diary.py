import datetime as dt
import time as t
from json import dumps
from logging import getLogger

from werkzeug import Response

from ..diary.database import read_date, read_schedule
from ..diary.views.web import rewrite_db
from ..lib import time_to_local_time
from ..lib.schedule import Schedule
from ..sql import ActivityJournal, StatisticJournal
from ..stats.display.activity import active_days, active_months, latest_activity, activities_start, activities_finish, \
    activities_by_group
from ..stats.display.nearby import constraints


log = getLogger(__name__)


class Diary:

    FMT = ('%Y', '%Y-%m', '%Y-%m-%d')

    @staticmethod
    def read_diary(request, s, date):
        schedule, date = parse_date(date)
        if schedule == 'd':
            data = read_date(s, date)
        else:
            data = read_schedule(s, Schedule(schedule), date)
        return Response(dumps(rewrite_db(list(data))))

    def read_neighbour_activities(self, request, s, date):
        # used in the sidebar menu to advance/retreat to the next activity
        ymd = date.count('-')
        before = ActivityJournal.before_local_time(s, date)
        after = ActivityJournal.after_local_time(s, date)
        result = {}
        if before: result['before'] = time_to_local_time(before.start, self.FMT[ymd])
        if after: result['after'] = time_to_local_time(after.start, self.FMT[ymd])
        return Response(dumps(result))

    @staticmethod
    def read_active_days(request, s, month):
        return Response(dumps(active_days(s, month)))

    @staticmethod
    def read_active_months(request, s, year):
        return Response(dumps(active_months(s, year)))

    @staticmethod
    def read_analysis_params(request, s):
        # odds and sods used to set menus in jupyter URLs
        latest = latest_activity(s)
        result = {'activities_start': activities_start(s),
                  'activities_finish': activities_finish(s),
                  'activities_by_group': activities_by_group(s),
                  'latest_activity_group': latest.activity_group.name if latest else None,
                  'latest_activity_time': time_to_local_time(latest.start) if latest else None,
                  'nearby_constraints': list(constraints(s))}
        return Response(dumps(result))

    @staticmethod
    def write_statistics(request, s):
        # used to write modified fields back to the database
        data = request.json
        log.info(data)
        n = 0
        for key, value in data.items():
            try:
                id = int(key)
                journal = s.query(StatisticJournal).filter(StatisticJournal.id == id).one()
                journal.set(value)
                n += 1
            except Exception as e:
                log.error(f'Could not save {key}:{value}: {e}')
        s.commit()
        log.info(f'Saved {n} values')
        return Response()


def parse_date(date):
    for schedule, format in (('y', '%Y'), ('m', '%Y-%m'), ('d', '%Y-%m-%d')):
        try:
            return schedule, dt.date(*t.strptime(date, format)[:3])
        except:
            pass
    raise Exception(f'Cannot parse {date}')
