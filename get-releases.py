#!/usr/bin/python2
# -*- coding: utf-8 -*-

############################################################################
#   Copyright (C) 2014 Evgeniy Alekseev                                    #
#                                                                          #
#   This program is free software: you can redistribute it and/or          #
#   modify it under the terms of the GNU General Public License as         #
#   published by the Free Software Foundation, either version 3 of the     #
#   License, or (at your option) any later version.                        #
#                                                                          #
#   This program is distributed in the hope that it will be useful,        #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#   GNU General Public License for more details.                           #
#                                                                          #
#   You should have received a copy of the GNU General Public License      #
#   along with this program. If not, see http://www.gnu.org/licenses/      #
############################################################################

import argparse
import datetime
import os
import lastfm

api_key = '23caa86333d2cb2055fa82129802780a'


def get_albums(artist):
    """get album by artist"""
    global api_key
    api = lastfm.Api(api_key)
    lastfm_artist = api.get_artist(artist)
    lastfm_albums = lastfm_artist.top_albums
    # need to do it since some albums has no release date
    albums = {}
    null_date = datetime.datetime(1970, 1, 1, 0, 0)
    for album in lastfm_albums:
        date = album.release_date
        if (date == ""):
            date = null_date
            null_date += datetime.timedelta(days=1)
        albums[date] = album.name
    return albums


def get_existance_releases(path):
    """get releases from existant directory"""
    return [os.path.basename(dirname) for dirname, dirnames, filenames in os.walk(os.path.join(path, ""))]


def get_uniq(existance, lastfm):
    """return uniq releases"""
    releases = {}
    for lastfm_release in lastfm:
        exist = False
        for ex_release in existance:
            if (ex_release.lower().find(lastfm[lastfm_release].lower()) > -1):
                exist = True
                break
        if (not exist):
            releases[lastfm_release] = lastfm[lastfm_release]
    return releases


def sort_albums(albums, count):
    """sort albums"""
    if (count == 0):
        return [[date, albums[date]] for date in reversed(sorted(albums))]
    else:
        return [[date, albums[date]] for date in reversed(sorted(albums))][:count]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Get lastest releases from given artist")
    parser.add_argument('artist', help = "artist names comma separated or path to directory")
    parser.add_argument('-c', '--count', dest = 'count', type=int, default = 1, help = "count of releases. 0 is all")
    args = parser.parse_args()

    dir_list = False
    if (os.path.isdir(args.artist)):
        artists = os.listdir(args.artist)
        dir_list = True
    else:
        artists = args.artist.split(',')
    for artist in artists:
        print ("%s :" % artist)
        albums = get_albums(artist)
        if (dir_list):
            albums = get_uniq(get_existance_releases(os.path.join(args.artist, artist)), albums)
        for album in sort_albums(albums, args.count):
            print ("  %4i-%02i-%02i : %s" % (album[0].year, album[0].month, album[0].day, album[1]))
