# -*- coding: utf-8 -*-
"""
uds.tools.cli
~~~~~~~~~~~~~

:copyright: Copyright (c) 2015, National Institute of Information and Communications Technology.All rights reserved.
:license: GPL2, see LICENSE for more details.
"""
import sys
import argparse
import os

from uds.tools.cli.commands import new_project
from uds.tools.cli.commands import new_sensor
from uds.tools.cli.commands import run_sensor


def main():
    execute(sys.argv[1:])


def execute(args):
    """Execute 'uds' command.
    """
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='uds')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 2.0.0')
    subparsers = parser.add_subparsers(help='Following sub-command is available to develop MySensor.')

    # create the parser for the "newproject" command
    parser_new_project = subparsers.add_parser('new-project', help='create new project')
    parser_new_project.add_argument('name', type=str, help='project name to create')
    parser_new_project.set_defaults(func=execute_new_project)

    # create the parser for the "newsensor" command
    parser_new_sensor = subparsers.add_parser('new-sensor', help='create new sensor')
    parser_new_sensor.add_argument('name', type=str, help='sensor class name to create')
    parser_new_sensor.add_argument('-t', '--template', type=str, help='template class name')
    parser_new_sensor.set_defaults(func=execute_new_sensor)

    # create the parser for the "run" command
    parser_run = subparsers.add_parser('run', help='run sensor')
    parser_run.add_argument('path', type=str, help='path of the sensor script')
    parser_run.set_defaults(func=execute_run)

    parsed_args = parser.parse_args(args)
    parsed_args.func(parsed_args)


def execute_new_project(args):
    current_dir = os.getcwd()
    new_project(current_dir, args.name)


def execute_new_sensor(args):
    project_home = _get_project_home()
    if project_home is None:
        print '(uds-cli) Current directory is not UDS Project.'
        return
    if args.template is None:
        print '(uds-cli) Enter template with -t option!'
        return

    new_sensor(project_home, args.template, args.name)


def execute_run(args):
    project_home = _get_project_home()
    if project_home is None:
        print '(uds-cli) Current directory is not UDS Project.'
        return

    run_sensor(project_home, args.path)


def _get_project_home():
    current_dir = os.getcwd()
    uds_cfg_path = os.path.normpath(os.path.join(current_dir, 'uds.cfg'))
    if os.path.exists(uds_cfg_path):
        project_home = current_dir
    else:
        project_home = None

    return project_home


if __name__ == "__main__":
    main()

