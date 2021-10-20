#!/usr/bin/env python3
from plexapi.server import PlexServer


def get_ps_name(location):
    last_slash = location.rfind('/')
    longeur = len(location) - last_slash
    new = location[0:-longeur]
    last_slash = new.rfind('/') + 1
    new = new[last_slash:]
    return new


plex_base_url = "http://localhost:32400/"
plex_token = "plex_token"
#https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
plex = PlexServer(plex_base_url, plex_token)
print("Connected to: " + str(plex.myPlexAccount()).replace('<MyPlexAccount:https://plex.tv/user:', '').replace('>', ''))

plex.library.refresh()

for section in plex.library.sections():
    music = plex.library.section(section.title)
    if section.type == "artist":

        for mus in music.searchTracks():
            location = mus.locations[0]
            playlist_name = get_ps_name(location)
            playlist = [playlist for playlist in plex.playlists() if playlist.title == playlist_name]

            if not playlist:
                plex.createPlaylist(playlist_name, items=mus)
            else:
                plex.playlist(playlist_name).addItems(mus)
