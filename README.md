## Wiidb.py

Wiidb.py is intended to be an easy to use Python library for getting metadata
for Wii and Gamecube discs from thegametdb.com. Robustness is the main goal
here, so some erroneous or awkward database entries are handled, but ambiguous
entries, such as those with conflicting version information, are ignored.

Currently, it only pulls a few chunks of information: gameid, title, region,
and disc hashes. This is because the original goal was just to manage and
verify disc images.  In the future, it will most likely process more
properties.

If you find an error or any missing information, please submit corrections to
[http://gametdb.com].

### Usage

Using wiidb.py is pretty simple because there is only one class, WiiDB,  with
three "public" methods, one of which is `__init__`.

`__init__` takes only one argument. If you set `wiidb_file`, the module will
save a JSON file containing the metadata it uses and the hash index. If
`wiidb_file` is not provided, it defaults to './wiidb.json'. `__init__`
automatically runs the `update` method if it can't load `wiidb_file`.

`update` is self-explanatory. It downloads and processes wiitdb.zip into Python
dicts and rebuilds the hash index.

`get_game_data` returns a dict pulled from the main data dict. It accepts four
optional arguments, `gameid`, `crc`, `md5`, and `sha1`.  It will retrieve full
metadata for the game given any of those arguments. 

Here is a full example:
```python
import wiidb

wiidb = wiidb.WiiDB(wiidb_file='some_nifty_path.json'))

print(wiidb.get_game_data(gameid='GK7E08'))
print(wiidb.get_game_data(sha1='84318b312fa6138e106da3661154716fb906ba0c'))
```

Which will output this: (pretty printing not included)
```python
{
  "title": "Killer7",
  "gameid": "GK7E08",
  "versions": {
    "1.01": {
      "disc1": {
        "md5": "4cdb132c4ab2d95b9095fdb1647e9636",
        "crc": "64f21d40",
        "sha1": "20d7c2a1b7f156c671166d3d552ad4645fa0c3d7",
        "size": "1459978240"
      },
      "disc2": {
        "md5": "58a84314ef4ccf17bd118a03009f93ad",
        "crc": "3d830b55",
        "sha1": "6c3aad4b78364b8c2c18241650783128dc1d0dbe",
        "size": "1459978240"
      }
    },
    "1.0": {
      "disc1": {
        "md5": "8e86c62162c84b08255076f31e312db6",
        "crc": "fdcb9f51",
        "sha1": "d469ddae322993a0ef38ea3628fa955f5801e2f7",
        "size": "1459978240"
      },
      "disc2": {
        "md5": "7393ca0cef0ff815803aeaeaa3a31a8c",
        "crc": "a88b1f9c",
        "sha1": "b69b34baaef1cd432a9f33a85fb960bb93c27957",
        "size": "1459978240"
      }
    }
  },
  "region": "NTSC-U"
}
{
  "title": "Lost in Shadow",
  "gameid": "SDWJ18",
  "versions": {
    "1.0": {
      "disc1": {
        "md5": "9895ea282c824d0cd71f83b41894b4fc",
        "crc": "f817c6ee",
        "sha1": "84318b312fa6138e106da3661154716fb906ba0c",
        "size": "4699979776"
      }
    }
  },
  "region": "NTSC-J"
}
```
