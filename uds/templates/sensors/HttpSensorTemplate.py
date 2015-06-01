# -*- coding: utf-8 -*-
import os
from uds.sensors.http import HttpSensor


class _MyHttpSensor(HttpSensor):
    
    def __init__(self, project_home):
        super(_MyHttpSensor, self).__init__(project_home)

        # ~~~ Initialize sensor parameters here ~~~

        pass

    # Method overriding (mandatory)
    def create_request(self):
        pass

    # Method overriding (mandatory)
    def parse_content(self, content, url):
        pass

    # Method overriding (optional)
    def before_cycle(self):
        super(_MyHttpSensor, self).before_cycle()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def after_cycle(self):
        super(_MyHttpSensor, self).after_cycle()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def open(self):
        super(_MyHttpSensor, self).open()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def close(self):
        super(_MyHttpSensor, self).close()

        # ~~~ Write optional code here ~~~

        pass


def get_sensor(project_home):
    return _MyHttpSensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()