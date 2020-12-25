# -*- encoding:utf-8 -*-
import datetime
import json
import logging
import os
import sys

from jishaku.modules import resolve_extensions
from discord.ext import commands

from utils import colored_logger


class Kagura(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_time = datetime.datetime.utcnow()

        self.config_path = 'config.json'

        # START
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config: dict = json.load(f)
        else:
            with open(self.config_path, 'w') as f:
                json.dump({}, f)
                self.config: dict = json.load(f)

        self.configs = {}

        # LOGGER
        self.db = None

        # LOGGER
        logging.basicConfig(filename='kagura.log', level=logging.INFO)
        self.logger = logging.getLogger("Kagura")

        stdout = logging.StreamHandler(sys.stdout)
        stdout.setLevel(logging.INFO)
        stdout.setFormatter(colored_logger.ColoredFormatter(colored_logger.formatter_message(
            "[$BOLD%(name)s$RESET][%(levelname)s] %(message)s $RESET($BOLD%(filename)s$RESET:%(lineno)d)")))

        self.logger.addHandler(stdout)

        # COMMANDS
        self.load_commands()

        # EVENTS
        self.load_event()

    def load_commands(self):
        # First try loading
        try:
            self.load_extension('jishaku')
        except Exception as e:
            self.logger.error(f'$REDError detect during loading $BLUEJishaku', exc_info=e)

        for ext in resolve_extensions(self, 'commands.*'):
            try:
                self.load_extension(ext)
            except Exception as e:
                self.logger.error(f'$REDError detect during loading commands $BLUE{ext}', exc_info=e)

    def load_event(self):
        for ext in resolve_extensions(self, 'events.*'):
            try:
                self.load_extension(ext)
            except Exception as e:
                self.logger.error(f'$REDError detect during loading event $BLUE{ext}', exc_info=e)

    async def on_ready(self):
        print('Client {0} is connected.'.format(self.user))

    # async def is_owner(self, user: discord.User):
    #     if something:  # Implement your own conditions here
    #         return True

    #    # Else fall back to the original
    #    return await super().is_owner(user)

    # async def on_message(self, message):
    #     print('Message from {0.author} -> {0.content}'.format(message))
