#!/usr/bin/env python3

import json
import wiidb

wiidb = wiidb.WiiDB()

print(json.dumps(wiidb.get_game_data(gameid='GK7E08'), indent=2))
print(json.dumps(wiidb.get_game_data(sha1='84318b312fa6138e106da3661154716fb906ba0c'), indent=2))
