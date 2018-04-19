#!/usr/bin/env python3
import time

from steam import SteamClient
from dota2 import Dota2Client
from dota2.enums import DOTA_GC_TEAM, DOTABotDifficulty, DOTA_GameMode
from dota2.features.party import Party
from dota2.features.lobby import Lobby
import click

# Setup logging.
import logging

logging.basicConfig(format='[%(asctime)s] %(levelname)s %(name)s: %(message)s', level=logging.DEBUG)

client = SteamClient()
dota = Dota2Client(client)


@client.on('logged_on')
def start_dota():
    dota.launch()


@dota.on('ready')
def dota_launched():
    # Create game lobby.
    # dota.invite_to_party(76561198044453639)
    dota.create_tournament_lobby(options={
        'game_mode': DOTA_GameMode.DOTA_GAMEMODE_1V1MID,
        'allow_cheats': True,
        'fill_with_bots': True,
        'bot_radiant': 0,
        'bot_dire': 0,
        'bot_difficulty_radiant': DOTABotDifficulty.BOT_DIFFICULTY_EXTRA3
    })


@dota.on(Lobby.EVENT_LOBBY_NEW)
def entered_lobby(lobby):
    """
    Entered a lobby event handler (by creating or joining one).
    """

    # Add bots and yourself to lobby.
    dota.join_practice_lobby_team()

    print(lobby)
    dota.invite_to_lobby(76561198082970923)


@dota.on(Lobby.EVENT_LOBBY_INVITE)
def party_created(p):
    # Launch game.
    print('ITS PARTY TIME!!!!!!!!!!!!!!!!!!!!!!!!!')


@dota.on(Lobby.EVENT_LOBBY_CHANGED)
def lobby_changed(l):
    global flag
    print(l)
    dota.launch_practice_lobby()


@click.command()
@click.option('--login', default='iovinien', help='Steam login.')
@click.option('--password', help='Steam login.')
def main(login, password):
    client.login(username=login, password=password)
    client.run_forever()


if __name__ == '__main__':
    main()
