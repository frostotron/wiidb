#!/usr/bin/env python3

import json
import re
import urllib3
import xml.etree.ElementTree as ElementTree
import zipfile

# TODO: Add option to display probable database errors such as empty version strings
#   and malformatted names.

# This is currently only designed to handle disc images, so wiiware titles
#   are just extra junk to process for now.
wiitdb_zip_url = 'http://www.gametdb.com/wiitdb.zip?LANG=EN&GAMECUBE=1'

class WiiDB:
    def __init__(self, wiidb_file='./wiidb.json'):
        self.wiidb_file = wiidb_file
        self.http = urllib3.PoolManager()
        self.game_data = {}
        self.hash_index = []

        self.version_regex = re.compile('[0-9]+\.[0-9]+')
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
            gameid = game_element.find('./id').text
            game_info['title'] = game_element.find('./locale[@lang=\'EN\']/title').text
            game_info['gameid'] = gameid
            game_info['region'] = game_element.find('./region').text

            game_info['versions'] = self._divine_version_information(game_element.findall('./rom'))

            self.game_data[gameid] = game_info

    def _divine_version_information(self, rom_elements):
        # Sweet holy mother of Yoshis the version/disc information in this database is awful.
        game_versions = {}
        disc_total = len(rom_elements)
        if disc_total > 1:
            # Is it multiple versions? Is it multiple discs? Gametdb doesn't say,
            #   so we have to guess from the "version" name...
            first_disc_version_string = ''
            # Some of these disc entries have no version name. It looks like gametdb.com needs moderators.
            for rom_element in rom_elements:
                if rom_element.get('version') is not '':
                    first_disc_version_string = rom_element.get('version')
                else:
                    # TODO: Database error!
                    pass

            first_disc_version = self.version_regex.search(first_disc_version_string)
            first_disc_number = self.disc_number_regex.search(first_disc_version_string)

            tiger_woods_2004_versions = ['disc1ukv', 'disc2ukv', 'disc1eur', 'disc2eur']
            if first_disc_version in tiger_woods_2004_versions:
                # TODO: Database issue!
                # Ignore it for now.
                print('I found Tiger Woods 2004!')

            elif first_disc_version and first_disc_number:
                # Multiple versions of a two-disc release. This bit of code is
                #   pretty much just for Killer7.
                game_versions = {}
                for rom_element in rom_elements:
                    version_string = rom_element.get('version')
                    disc_name = self._determine_disc_name( \
                        self.disc_number_regex.search(version_string).group())

                    version_regex_result = self.version_regex.search( \
                        rom_element.get('version'))
                    if version_regex_result == None:
                        disc_version = 1.0
                    else:
                        disc_version = version_regex_result.group()

                    disc_info = self._build_disc_info(rom_element)

                    if not(disc_version in game_versions.keys()):
                        game_versions[disc_version] = {}

                    game_versions[disc_version][disc_name] = self._build_disc_info(rom_element)
                    

            elif first_disc_number:
                # print('%s matches number: %s.' % (first_disc_name, first_disc_number.group(0)))
                # It's a single version two-disc release.
                # TODO: Probably put the Tiger Woods 2004 version and name-determining
                #   bits in this block.
                game_versions['1.0'] = {}
                # A few games have disc1 labeled as disc0 and disc2 labeled as disc1.
                #   How confusing...
                disc0_found = False
                for rom_element in rom_elements:
                    disc_name = self._determine_disc_name(rom_element.get('version'))
                    disc_info = self._build_disc_info(rom_element)
                    game_versions['1.0'][disc_name] = disc_info

            elif first_disc_version:
                # It's a normal multi-version release, like Smash.
                for rom_element in rom_elements:
                    # TODO: Deal with identically named versions, particularly ''.
                    version_name = rom_element.get('version')
                    disc_name = 'disc1'

                    version_info = {disc_name: self._build_disc_info(rom_element)}

                    game_versions[version_name] = version_info
            else:
                # For now, we can just ignore blank version names as there are
                #   only a handful of entries that have no version information.
                #   and they are all database errors.
                # TODO: Database error!
                print('Could not get version information, ignoring game: %s.' % rom_elements[0].get('name'))
                print('Version string: %s.' % first_disc_version)
                print('Number of discs: %s.' % len(rom_elements))

        elif disc_total == 1:
            # Whew, just one disc and one version.
            # One verison does not necessarily mean 1.0.
            version_name = '1.0'
            disc_name = 'disc1'
            rom_element = rom_elements[0]
            disc_info = { disc_name: self._build_disc_info(rom_element) }

            game_versions[version_name] = disc_info

        # Returning None is more useful than returning an empty dict, but
        #   changing from None to a dict earlier on in the code will get ugly.
        if game_versions == {}:
            game_versions = None
        return game_versions

    def _build_disc_info(self, rom_element):
        disc_info = {
            'size': rom_element.get('size'),
            'crc': rom_element.get('crc'),
            'md5': rom_element.get('md5'),
            'sha1': rom_element.get('sha1')
        }
        
        return disc_info

    def _determine_disc_name(self, version_string):
        disc_name = ''
        disc0_found = False
        if '0' in version_string:
            # TODO: Database error!
            disc_name = 'disc1'
            disc0_found = True

        elif '1' in version_string:
            if disc0_found == True:
                disc_name = 'disc2'

            else:
                disc_name = 'disc1'

        elif '2' in version_string:
            disc_name = 'disc2'

        else:
            print('Erroneous disc name: %s' % rom_element.get('version'))

        return disc_name

wiidb = WiiDB()
wiidb.update()

print(json.dumps(wiidb.game_data['GALE01'], indent=2))
print(json.dumps(wiidb.game_data['GK7E08'], indent=2))
