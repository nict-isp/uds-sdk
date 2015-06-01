# -*- coding: utf-8 -*-
import os
from uds.sensors.base import Sensor


class _MySensor(Sensor):

    def __init__(self, project_home):
        super(_MySensor, self).__init__(project_home)

        # ~~~ Initialize sensor parameters here ~~~

        pass

    # Method overriding (mandatory)
    def fetch(self):
        pass

    # Method overriding (mandatory)
    def parse(self, source):
        pass

    # Method overriding (optional)
    def before_cycle(self):
        super(_MySensor, self).before_cycle()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def after_cycle(self):
        super(_MySensor, self).after_cycle()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def open(self):
        super(_MySensor, self).open()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def close(self):
        super(_MySensor, self).close()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (not recommended)
    def check(self, m2m_data_list):
        pass

    # Method overriding (not recommended)
    def filter(self, m2m_data_list):
        pass

    # Method overriding (not recommended)
    def store(self, m2m_data_list):
        pass


def get_sensor(project_home):
    return _MySensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()