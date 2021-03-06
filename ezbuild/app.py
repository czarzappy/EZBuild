import ezbuild.common.file as file
import sys, getopt
from pathlib import Path

from ezbuild.common import bash, butler, zlog
import ezbuild.common.unity as unity
from ezbuild.common.steamcmd import SteamCMD


def run(argv):

    config_file = ''
    try:
        opts, args = getopt.getopt(argv, "hc:", ["cfile="])
    except getopt.GetoptError:
        print('app.py -c <configfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('app.py -c <configfile>')
            sys.exit()
        elif opt in ("-c", "--cfile"):
            config_file = arg
    zlog.info('Config file is', config_file)

    if config_file is None:
        zlog.warn('No config file defined!')
        return

    build_config = file.load_config(config_file)

    project_path = Path(build_config["project_path"])

    zlog.info("project path", project_path)

    output_dir = project_path / "Builds"

    project_version_path = project_path / "ProjectSettings" / "ProjectVersion.txt"
    project_version_dict = file.load_yaml(project_version_path)

    unity_version = project_version_dict['m_EditorVersion']

    if unity_version is None:
        unity_version = build_config["unity_version"]

    unity_path = unity.get_unity_path(unity_version)
    zlog.info('Using Unity:', unity_path)

    unity_cmd = unity.Unity(unity_path, output_dir)

    killed_unity = False
    # only kill unity if we are going to do a build
    if build_config["steps"].__contains__("build"):
        bash.check_and_kill_process(unity_path)
        killed_unity = True

    project_name = build_config["project_name"]
    zlog.info("Publishing to ITCH.IO: {}".format(project_name))

    for target_config in build_config["targets"]:

        channel_name = target_config["channel_name"]

        if target_config.__contains__("active"):
            active = target_config["active"]

            if not active:
                print("Skipping target:", channel_name)
                continue

        project_output_dir = '{}/{}-{}'.format(output_dir, project_name, channel_name)
        print('project_output_dir:', project_output_dir)

        if build_config["steps"].__contains__("build"):
            bash.clear_dir(project_output_dir)
            bash.mkdir(project_output_dir)

            build_target = target_config["build_target"]

            print("starting unity build")
            unity_cmd.run_build_target(project_name, build_target, project_output_dir)

        if build_config["steps"].__contains__("publish-itch"):
            org_name = build_config["org_name"]

            butler.push(org_name, project_name, project_output_dir, channel_name)
            butler.status(org_name, project_name, channel_name)

    if build_config["steps"].__contains__("publish-steam"):
        steam_cmd = SteamCMD()  # TODO: support generate credential management for SteamCMD login
        app_build_path = build_config["steam"]["app_build_path"]
        print('App Build Path:', app_build_path)
        steam_cmd.run_app_build(app_build_path)

    # if killed_unity:
        #  TODO: Reopen Unity if we killed it

