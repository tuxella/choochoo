
from logging import basicConfig, getLogger, INFO, DEBUG
from sys import stdout
from tempfile import TemporaryDirectory
from time import sleep
from unittest import TestCase

from ch2.command.args import JUPYTER, ROOT
from ch2.uranus.server import stop, start_from_args
from ch2.uranus.template.load import create_notebook


class TestUranus(TestCase):

    def setUp(self):
        if not getLogger().handlers:
            basicConfig(stream=stdout, level=DEBUG)
        self._log = getLogger()

    def test_display(self):
        with TemporaryDirectory() as dir:
            self._log.debug(f'Dir {dir}')
            args = {JUPYTER: True, ROOT: dir}
            start_from_args(args, self._log)
            sleep(1)
            name = create_notebook(self._log, 'compare_activities',
                                   activity_date='2018-03-01 16:00', compare_date='2017-09-19 16:00')
            self._log.debug(f'Name {name}')
            sleep(3600)
            stop()
