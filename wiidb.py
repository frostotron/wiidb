#!/usr/bin/env python3

import re
import urllib3
import xml.etree.ElementTree as ElementTree
import zipfile

wiitdb_zip_url = 'http://www.gametdb.com/wiitdb.zip?LANG=EN&WIIWARE=1&GAMECUBE=1'

class WiiDB:
    def __init__(self, wiidb_file='./wiidb.json'):
        self.wiidb_file = wiidb_file
        self.http = urllib3.PoolManager()
        self.game_data = {}
        self.hash_index = []

        self.version_regex = re.compile('[1-9]+\.[1-9]+')
        self.disc_number_regex = re.compile('(D|d)isc( |)[0-2]')

    def get_game_data(self, gameid=None, crc=None, md5=None, sha1=None):
        pass

    def update(self):
        # TODO: Work out downloading wiitdb.zip.
        '''
        print('Downloading new wiitdb.zip.')
        wiitdb_zip_file = self.http.request('GET', wiitdb_zip_url)
        print('Download finished.')
        '''
        wiitdb_xml = ''
        wiitdb_zip_file = './wiitdb.zip'
        print('Parsing XML...')
        with zipfile.ZipFile(wiitdb_zip_file) as wiitdb_zip:
            with wiitdb_zip.open('wiitdb.xml') as wiitdb_xml_file:
                wiitdb_xml = ElementTree.fromstring(wiitdb_xml_file.read())

        print('Reading game elements.')
        game_elements = wiitdb_xml.findall('./game')
        for game_element in game_elements:
            game_info = {}
            game_info['title'] = game_element.find('./locale[@lang=\'EN\']/title').text
            game_info['gameid'] = game_element.find('./id').text
            game_info['region'] = game_element.find('./region').text

            game_info['versions'] = self._divine_version_information(game_element.findall('./rom'))

            
            # TODO: Debug code. Remove.
            if game_info['versions'] is not None:
                if len(game_info['versions'].keys()) > 1 :
                    print(game_info)

    def _divine_version_information(self, rom_elements):
        # Sweet holy mother of Yoshis the version/disc information in this database is awful.
        game_versions = {}
        if len(rom_elements) > 1:
            # Is it multiple versions? Is it multiple discs? Gametdb doesn't say,
            #   so we have to guess from the "version" name...
            first_disc_name = rom_elements[0].get('version')
            disc_version = self.version_regex.search(first_disc_name)
            disc_number = self.disc_number_regex.search(first_disc_name)

            if disc_version and disc_number:
                print('%s matches both version and number: %s, %s.' % (first_disc_name, disc_version.group(0), disc_number.group(0)))
                # Multiple versions of a two-disc release. This bit of code is
                #   pretty much just for Killer7.
                pass

            elif disc_version:
                print('%s matches version: %s.' % (first_disc_name, disc_version.group(0)))
                # It's a normal multi-version release, like Smash.
                for disc in rom_elements:
                    disc_info = {}
                    version_name = disc.get('version')
                    disc_name = 'disc1'

                    disc_info['md5'] = disc.get('md5')

                    version_info = {disc_name: disc_info}

                    game_versions[version_name] = version_info
                    print('Added version %s.' % version_name)

            elif disc_number:
                # print('%s matches number: %s.' % (first_disc_name, disc_number.group(0)))
                # It's a single version two-disc release.
                pass


        elif len(rom_elements) == 1:
            # Whew, just one disc and one version.
            # One verison does not necessarily mean 1.0.
            version_name = '1.0'
            disc_name = 'disc1'

            disc_element = rom_elements[0]

            disc_info = {
                disc_name: {
                    'size': disc_element.get('size'),
                    'md5': disc_element.get('md5')
                    }
                }

            game_versions[version_name] = disc_info

        else: # Assuming rom_elements is an empty list
            pass

        if game_versions == {}:
            game_versions = None
        return game_versions

wiidb = WiiDB()
wiidb.update()

