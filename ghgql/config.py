"""
Config module.
"""
from pathlib import Path

import yaml


ETC_DIR = Path() / 'etc'
LOCAL_CONF_PATH = ETC_DIR / 'app.local.yml'
TEMPLATE_CONF_PATH = ETC_DIR / 'app.template.yml'

BASE_URL = "https://api.github.com/graphql"


def _load_yaml(path):
    with open(path) as f_in:
        conf = yaml.safe_load(f_in)

    return conf


def get_local_conf():
    """
    Read unversioned local config or fallback to template, file which is versioned.
    """
    if LOCAL_CONF_PATH.exists():
        path = LOCAL_CONF_PATH
    else:
        path = TEMPLATE_CONF_PATH

    return _load_yaml(path)


def setup():
    conf = get_local_conf()

    commit_report_conf = conf['commit_report']
    access_token = conf['access_token']

    return commit_report_conf, access_token


COMMIT_REPORT_CONF, ACCESS_TOKEN = setup()


if __name__ == '__main__':
    print(BASE_URL)
    print(ACCESS_TOKEN)
    print(COMMIT_REPORT_CONF)
