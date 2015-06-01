# -*- coding: utf-8 -*-
import os
from uds.sensors.ieee1888 import IEEE1888Sensor


class _MyIEEE1888Sensor(IEEE1888Sensor):
    
    def __init__(self, project_home):
        super(_MyIEEE1888Sensor, self).__init__(project_home)

        # ~~~ Initialize sensor parameters here ~~~

        pass

    # Method overriding (mandatory)
    def create_query_keys(self):
        pass

    # Method overriding (mandatory)
    def parse_response(self, content, url):
        pass

    # Method overriding (optional)
    def before_cycle(self):
        super(_MyIEEE1888Sensor, self).before_cycle()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def after_cycle(self):
        super(_MyIEEE1888Sensor, self).after_cycle()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def open(self):
        super(_MyIEEE1888Sensor, self).open()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def close(self):
        super(_MyIEEE1888Sensor, self).close()

        # ~~~ Write optional code here ~~~

        pass


def get_sensor(project_home):
    return _MyIEEE1888Sensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()