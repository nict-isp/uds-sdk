# -*- coding: utf-8 -*-
import os
from uds.sensors.mysql import MySQLSensor


class _MyMySQLSensor(MySQLSensor):
    
    def __init__(self, project_home):
        super(_MyMySQLSensor, self).__init__(project_home)

        # ~~~ Initialize sensor parameters here ~~~

        pass

    # Method overriding (mandatory)
    def create_query(self):
        pass

    # Method overriding (mandatory)
    def parse_rows(self, rows):
        pass

    # Method overriding (optional)
    def before_cycle(self):
        super(_MyMySQLSensor, self).before_cycle()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def after_cycle(self):
        super(_MyMySQLSensor, self).after_cycle()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def open(self):
        super(_MyMySQLSensor, self).open()

        # ~~~ Write optional code here ~~~

        pass

    # Method overriding (optional)
    def close(self):
        super(_MyMySQLSensor, self).close()

        # ~~~ Write optional code here ~~~

        pass


def get_sensor(project_home):
    return _MyMySQLSensor(project_home)


if __name__ == '__main__':
    PROJECT_HOME = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    sensor = get_sensor(PROJECT_HOME)
    sensor.run()