#!/usr/bin/env python

import argparse
import os
import random
import sys


DEFAULT_SLOW = ".92"
DEFAULT_MENU = "1"
DEFAULT_FAST = "1.3"


def list_audio(directory):
    audio_files = []
    for curr in os.listdir(directory):
        if curr.endswith(".ogg") or curr.endswith(".wav"):
            audio_files.append(curr)

    return audio_files


def read_file(filename):
    with open(filename) as f:
        lines = [x.rstrip() for x in f.readlines()]

    return lines


# i realize that this is O(n), but these lists are small
# in practice
def song_should_override(song, override_list):
    for x in override_list:
        if x.startswith(song):
            return x

    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Joust Jingle Juggler")
    parser.add_argument('--alpha', '-a', action='store_false', dest='shuffle')
    parser.add_argument('--slow', default=DEFAULT_SLOW)
    parser.add_argument('--menu', default=DEFAULT_MENU)
    parser.add_argument('--fast', default=DEFAULT_FAST)
    parser.add_argument('--excludes-file', '-e', default=os.path.join('.', 'excludes'))
    parser.add_argument('--overrides-file', '-o', default=os.path.join('.', 'overrides'))
    parser.add_argument('--no-write-shuffle', '-w', action='store_false', dest='write_shuffle')
    flags = parser.parse_args()

    found_songs = list_audio('.')
    songs_to_exclude = set(read_file(flags.excludes_file))
    songs_to_override = read_file(flags.overrides_file)

    text_to_write = []

    for curr in found_songs:
        if curr not in songs_to_exclude:
            potential_override = song_should_override(curr, songs_to_override)
            if potential_override is not None:
                sys.stderr.write("Overriding %s\n" % curr)
                sys.stderr.flush()
                text_to_write.append(potential_override)
            else:
                text_to_write.append("%s    %s, %s, %s" % (curr, flags.slow, flags.menu, flags.fast))
        else:
            sys.stderr.write("Excluding %s\n" % curr)
            sys.stderr.flush()

    print 'ENABLE_USER_PLAYLIST    true'

    if flags.shuffle:
        random.shuffle(text_to_write)

    if flags.write_shuffle:
        print 'ENABLE_SHUFFLE     true'
    else:
        print 'ENABLE_SHUFFLE     false'

    print '\n'.join(text_to_write)




