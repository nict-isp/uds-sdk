# -*- coding: utf-8 -*-
"""
uds.tools.cli.commands
~~~~~~~~~~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import os
import shutil
import imp
import re


def new_project(current_dir, project_name):
    print '----------------------------------------------------------------------'
    print 'New Project                                                           '
    print '----------------------------------------------------------------------'

    template_dir = _get_template_project_dir()
    assert os.path.exists(template_dir)

    project_dir = os.path.join(current_dir, project_name)
    if os.path.exists(project_dir):
        print 'Project directory is already exists. project_dir_path=%s' % project_dir
        return

    print 'src_dir=%s' % template_dir
    print 'dst_dir=%s' % project_dir
    print '----------------------------------------------------------------------'

    shutil.copytree(template_dir, project_dir)
    print 'SUCCESS'
    print '----------------------------------------------------------------------'


def new_sensor(project_home, template_name, sensor_name):
    print '----------------------------------------------------------------------'
    print 'New Sensor                                                            '
    print '----------------------------------------------------------------------'

    template_file_path = os.path.join(_get_template_sensors_dir(), template_name + 'Template.py')
    assert os.path.exists(template_file_path)

    sensor_file_path = os.path.join(project_home, 'udsimpl/sensors/%s.py' % sensor_name)

    print 'template_file_path=%s' % template_file_path
    print 'sensor_path=%s' % sensor_file_path
    print '----------------------------------------------------------------------'

    if os.path.exists(sensor_file_path):
        print 'ERROR: The sensor is already exists.'
        return

    f = open(template_file_path, 'r')
    template_text = f.read()
    f.close()

    sensor_text = re.sub('(_My)(.*?)(Sensor)', sensor_name, template_text)

    f = open(sensor_file_path, 'w')
    f.write(sensor_text)
    f.close()

    print 'SUCCESS'
    print '----------------------------------------------------------------------'


def run_sensor(project_home, sensor_path):
    print '----------------------------------------------------------------------'
    print 'Run Sensor                                                            '
    print '----------------------------------------------------------------------'

    script_path = os.path.abspath(os.path.join(project_home, sensor_path))

    if not os.path.exists(script_path):
        print 'ERROR: The sensor is not exists.'
        return

    base_path = os.path.dirname(script_path)
    module_name = os.path.basename(os.path.splitext(script_path)[0])

    print 'script_path=%s' % script_path
    print 'module_name=%s' % module_name
    print 'class_name=%s' % module_name
    print '----------------------------------------------------------------------'

    sensor_module = load_module(module_name, base_path)
    sensor = sensor_module.get_sensor(project_home)
    sensor.run()


def _get_template_project_dir():
    template_dir = os.path.normpath(os.path.join(os.path.abspath(__file__), '../../../templates/project'))
    return template_dir


def _get_template_sensors_dir():
    template_dir = os.path.normpath(os.path.join(os.path.abspath(__file__), '../../../templates/sensors'))
    return template_dir


def load_module(module_name, base_path):
    f, n, d = imp.find_module(module_name, [base_path])
    return imp.load_module(module_name, f, n, d)