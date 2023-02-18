# -*- coding: utf-8 -*-

import argparse
import getpass
import os
import sys

from .openai.api import ChatGPT
from .openai.auth import Auth0
from .openai.bot import ChatBot
from .openai.utils import Console

if 'nt' == os.name:
    import pyreadline as readline
else:
    import readline

    readline.set_completer_delims('')


def main():
    Console.debug_b(
        '''
        Pandora - A command-line interface to ChatGPT
        Github: https://github.com/pengzhile/pandora
        ''',
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--proxy',
        help='Use a proxy. Format: http://user:pass@ip:port',
        required=False,
        type=str,
        default=None,
    )
    parser.add_argument(
        '-t',
        '--token_file',
        help='Specify an access token file and login with your access token.',
        required=False,
        type=str,
        default=os.environ.get("chatgpt_access_token_file",None),
    )
    args, _ = parser.parse_known_args()

    token_file = args.token_file
    if token_file:
        print(f"Read access token from file [{token_file}]")
        if not os.path.isfile(token_file):
            raise Exception('Error: {} is not a file.'.format(token_file))

        with open(token_file, 'r') as f:
            access_token = f.read().strip()
    else:
        Console.info_b('Please enter your email and password to log in ChatGPT!')
        email = input('  Email: ')
        password = getpass.getpass('  Password: ')
        Console.warn('### Do login, please wait...')
        access_token = Auth0(email, password, args.proxy).auth()

    ChatBot(ChatGPT(access_token, args.proxy)).run()


def run():
    try:
        main()
    except KeyboardInterrupt:
        Console.info('\n\nBye...')
        sys.exit(0)
    except Exception as e:
        Console.error_bh('### Error occurred: ' + str(e))
