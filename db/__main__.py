import argparse
import logging
from envparse import env

from alembic.config import CommandLine, Config

from db.utils import generate_db_url


def main():
    env.read_envfile()

    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    options = alembic.parser.parse_args()

    config = Config("./alembic.ini")
    config.set_main_option('sqlalchemy.url', generate_db_url(prefix='postgresql'))
    exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()
