import time
import sys
from time import sleep
from subprocess import Popen, PIPE

import click
import requests


@click.group()
def main():
    print(
        ' ################################################################')
    print(
        ' #                                                              #')
    print(
        ' #      ____                    __                              #')
    print(
        ' #     /\  _`\                 /\ \__  __                       #')
    print(
        ' #     \ \,\L\_\  _____     ___\ \ ,_\/\_\  _____   __  __      #')
    print(
        ' #      \/_\__ \ /\ \'__`\  / __`\ \ \/\/\ \/\ \'__`\/\ \/\ \     #')
    print(
        ' #        /\ \L\ \ \ \L\ \/\ \L\ \ \ \_\ \ \ \ \L\ \ \ \_\ \    #')
    print(
        ' #        \ `\____\ \ ,__/\ \____/\ \__\\ \_\ \ ,__/\/`____  \   #')
    print(
        ' #         \/_____/\ \ \/  \/___/  \/__/ \/_/\ \ \/  `/___/> \  #')
    print(
        ' #                  \ \_\                     \ \_\     /\___/  #')
    print(
        ' #                   \/_/                      \/_/     \/__/   #')
    print(
        ' #                                                              #')
    print(
        ' #                                                              #')
    print(
        ' #    by bjarneo <http://www.github.com/bjarneo/Spotipy>        #')
    print(
        ' #                                                              #')
    print(
        ' ################################################################\n')


def osascript(command):
    '''Run apple script command.'''
    p = Popen(
        ['osascript', '-e', 'tell app "Spotify" to {}'.format(command)],
        stdout=PIPE, stderr=PIPE)
    # get stdout and stderr
    output, err = p.communicate()
    # strip text and decode to unicode
    output = output.strip().decode('utf-8')
    return output


@main.command()
@click.argument('query')
def search(query):
    '''Search for song then play it.'''
    # call track api to search for songs
    url = 'https://ws.spotify.com/search/1/track.json'
    # get results
    datas = requests.get(url, params={'q': query}).json()

    # define string format for each row
    space = '{:^4} | {:^25} | {:^40} | {:^25}'

    # print header
    print(space.format('#', 'Artist', 'Song', 'Album'))
    # print divider
    print(space.format('-' * 4, '-' * 25, '-' * 40, '-' * 25))

    # print each song
    for i, track in enumerate(datas['tracks']):
        print(space.format(
            i, track['artists'][0]['name'][:25], track['name'][:40],
            track['album']['name'][:25]))

    # sleep 0.01 second for sexy print
    time.sleep(0.01)

    # ask user which one he/she wants
    index = input('\nWhich one do you want to listen? ')

    # get result and convert it to integer
    try:
        index = int(index)
    except ValueError:
        print('Index should be integer.')
        sys.exit(1)

    # call apple script to play the specific song
    try:
        osascript('play track "{}"'.format(datas['tracks'][index]['href']))
        print('Playing now: {}'.format(datas['tracks'][index]['name']))
    except IndexError:
        # in case of user enters a invalid index
        print('Play for nothing')
        sys.exit(1)


@main.command()
def next():
    '''Play next song.'''
    osascript('next track')
    print('Next track')


@main.command()
def previous():
    '''Play previous song.'''
    osascript('previous track')
    print('Previous track')


@main.command()
def playpause():
    '''Play or pause current song.'''
    osascript('playpause')
    print('Playpause track')


@main.command()
def volume():
    '''The sound volume set in Spotify (0-100).'''
    output = osascript('get sound volume')
    print('Current volume:', output)


@main.command()
@click.argument('volume')
def set_volume(volume):
    '''Set spotify sound volume (0-100).'''
    osascript('set sound volume to {}'.format(volume))
    print('Current volume:', volume)


@main.command()
def state():
    '''Stopped, playing, or paused.'''
    output = osascript('get player state')
    print('Player state:', output)


@main.command()
def position():
    '''The curret position (in seconds) of the current song playing.'''
    output = osascript('get player position')
    print('Player position:', output)


@main.command()
@click.argument('position')
def set_position(position):
    '''Set track position (in seconds) of the current song.'''
    osascript('set player position to {}'.format(position))
    print('Player position:', position)


@main.command()
def repeat():
    '''Is repeating enabled or disabled (boolean value)'''
    output = osascript('get repeating')
    print('Repeat:', output)


@main.command()
def toggle_repeat():
    '''Toggle repeat option.'''
    # get current repeat status
    output = osascript('get repeating')

    if 'true' == output:
        # if true then set repeating to false
        osascript('set repeating to false')
        print('Repeat: false')
    else:
        # if true then set repeating to true
        osascript('set repeating to true')
        print('Repeat: true')


@main.command()
@click.argument('repeat')
def set_repeat(repeat):
    '''Set repeat option.'''
    osascript('set repeating to {}'.format(repeat))
    print('Repeat:', repeat)


@main.command()
def shuffle():
    '''Is shuffling enabled or disabled (boolean value).'''
    output = osascript('get shuffling')
    print('Shuffle:', output)


@main.command()
def toggle_shuffle():
    '''Toggle shuffle option.'''
    # get current shuffle status
    output = osascript('get shuffling')

    if 'true' == output:
        # if true then set shuffle to false
        osascript('set shuffling to false')
        print('Shuffle: false')
    else:
        # if true then set shuffle to true
        osascript('set shuffling to true')
        print('Shuffle: true')


@main.command()
@click.argument('shuffle')
def set_shuffle(shuffle):
    '''Set shuffle option.'''
    osascript('set shuffling to {}'.format(shuffle))
    print('Shuffle:', shuffle)


@main.command()
def track():
    '''Print current track info.'''
    infos = [
        ('Artist', osascript('get artist of current track')),
        ('Album', osascript('get album of current track')),
        ('Disc number', osascript('get disc number of current track')),
        ('Duration', osascript('get duration of current track')),
        ('Played count', osascript('get played count of current track')),
        ('Track number', osascript('get track number of current track')),
        ('Starred', osascript('get starred of current track')),
        ('Popularity', osascript('get popularity of current track')),
        ('Track Id', osascript('get id of current track')),
        ('Name', osascript('get name of current track')),
        # ('artwork', osascript('get artwork of current track')),
        ('Album artist', osascript('get album artist of current track')),
        ('Url', osascript('get spotify url of current track')),
    ]

    # define row string format
    row = '{:12}:  {}'
    for k, v in infos:
        print(row.format(k, v))


@main.command()
def current():
    '''Continuously getting current track, and check this is a new track.'''
    # save old track url
    old_url = ''

    # check current_url is the same as old_url
    while True:
        # get current track url
        current_url = osascript('get spotify url of current track')

        # if current_url is not the same as old_url,
        # send message to facebook group
        if current_url != old_url:
            # call track api to retrieve track info
            url = 'https://api.spotify.com/v1/tracks/{}'.format(
                current_url.split(':')[-1])
            res = requests.get(url)
            datas = res.json()

            print('Now playing: {}'.format(datas['name']))

        # update old_url with current_url
        old_url = current_url

        # sleep for 0.1 second
        sleep(0.1)

if __name__ == '__main__':
    main()
