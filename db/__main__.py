import argparse
import logging
from envparse import env

from alembic.config import CommandLine, Config


def main():
    env.read_envfile()

    logging.basicConfig(level=logging.DEBUG)

    alembic = CommandLine()
    alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    options = alembic.parser.parse_args()

    config = Config("./alembic.ini")
    config.set_main_option('sqlalchemy.url',
                           f"postgresql://{env.str('POSTGRES_USER')}:{env.str('POSTGRES_PASSWORD')}@{env.str('POSTGRES_HOST')}:{env.str('POSTGRES_PORT')}/{env.str('POSTGRES_DB')}")
    exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
    main()
