import json
import os
import wiidb
import unittest

test_wiidb_directory = './test_wiidb.json'

class LowEffortTestGroup(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        if os.path.isfile(test_wiidb_directory):
            os.remove(test_wiidb_directory)

        self.wiidb = wiidb.WiiDB(test_wiidb_directory)
        self.maxDiff = None

    @classmethod
    def tearDownClass(self):
        if os.path.isfile(test_wiidb_directory):
            os.remove(test_wiidb_directory)

    def test_one_disc_metadata(self):
        expected_metadata = {
          "versions": {
            "1.0": {
              "disc1": {
                "sha1": "84318b312fa6138e106da3661154716fb906ba0c",
                "size": "4699979776",
                "crc": "f817c6ee",
                "md5": "9895ea282c824d0cd71f83b41894b4fc"
              }
            }
          },
          "region": "NTSC-J",
          "gameid": "SDWJ18",
          "title": "Lost in Shadow"
        }

        self.assertEqual(expected_metadata, self.wiidb.get_game_data(gameid='SDWJ18'))

    def test_two_disc_multiversion_metadata(self):
        expected_metadata = {
          "versions": {
            "1.01": {
              "disc2": {
                "sha1": "6c3aad4b78364b8c2c18241650783128dc1d0dbe",
                "size": "1459978240",
                "crc": "3d830b55",
                "md5": "58a84314ef4ccf17bd118a03009f93ad"
              },
              "disc1": {
                "sha1": "20d7c2a1b7f156c671166d3d552ad4645fa0c3d7",
                "size": "1459978240",
                "crc": "64f21d40",
                "md5": "4cdb132c4ab2d95b9095fdb1647e9636"
              }
            },
            "1.0": {
              "disc2": {
                "sha1": "b69b34baaef1cd432a9f33a85fb960bb93c27957",
                "size": "1459978240",
                "crc": "a88b1f9c",
                "md5": "7393ca0cef0ff815803aeaeaa3a31a8c"
              },
              "disc1": {
                "sha1": "d469ddae322993a0ef38ea3628fa955f5801e2f7",
                "size": "1459978240",
                "crc": "fdcb9f51",
                "md5": "8e86c62162c84b08255076f31e312db6"
              }
            }
          },
          "region": "NTSC-U",
          "gameid": "GK7E08",
          "title": "Killer7"
        }

        self.assertEqual(expected_metadata, self.wiidb.get_game_data(gameid='GK7E08'))
