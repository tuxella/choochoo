
from .args import FORCE, mm, LIKE, AFTER
from ..squeal.tables.pipeline import PipelineType
from ..stoats.calculate import run_pipeline_after


def statistics(args, log, db):
    '''
## statistics

    > ch2 statistics

Generate any missing statistics.

    > ch2 statistics --force [DATE]

Delete statistics after the date (or all, if omitted) and then generate new values.
    '''
    force, like = args[FORCE], args[LIKE]
    run_pipeline_after(log, db, PipelineType.STATISTIC, force_after=force, like=like)
