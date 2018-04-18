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
    dota.create_practice_lobby(options={
        'game_mode': DOTA_GameMode.DOTA_GAMEMODE_1V1MID,
        'allow_cheats': True,
        'fill_with_bots': True,
        'pass_key': 'very hard password',
        'bot_radiant': 0,
        'bot_dire': 0
    })


@dota.on(Lobby.EVENT_LOBBY_NEW)
def entered_lobby(lobby):
    """
    Entered a lobby event handler (by creating or joining one).
    """

    # Add bots and yourself to lobby.
    # dota.join_practice_lobby_team(slot=2,
    #                               team=DOTA_GC_TEAM.SPECTATORS)
    dota.add_bot_to_practice_lobby(slot=1,
                                   team=DOTA_GC_TEAM.GOOD_GUYS,
                                   bot_difficulty=DOTABotDifficulty.BOT_DIFFICULTY_EXTRA1)
    dota.add_bot_to_practice_lobby(slot=4, team=DOTA_GC_TEAM.BAD_GUYS,
                                   bot_difficulty=DOTABotDifficulty.BOT_DIFFICULTY_EXTRA1)

    print(lobby)


@dota.on(Party.EVENT_NEW_PARTY)
def party_created():
    # Launch game.
    time.sleep(3)
    dota.launch_practice_lobby()


@dota.on(Lobby.EVENT_LOBBY_CHANGED)
def lobby_changed(l):
    print(l)


@click.command()
@click.option('--login', default='vergiliy57', help='Steam login.')
@click.option('--password', help='Steam login.')
def main(login, password):
    client.login(username=login, password=password)
    client.run_forever()


if __name__ == '__main__':
    main()
