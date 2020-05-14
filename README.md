# GalaxyGenericImporterPlugin
Plugin for GOG Galaxy to allow the generic definition of software using regular expressions.

## Installation
The plugin will need to be placed in `%localappdata%\GOG.com\Galaxy\plugins\installed\importer_97543122-7785-4444-2254-711233556699` . The following is a Youtube video showing installation using default directories for software. https://www.youtube.com/watch?v=FCrHWRy0fOs

## Configuration
Configuration for execution, selection and location of files is located in the `emulators.json` file. See the included for an example and used by default if not changed.

### name
The different platforms names are saved as tags, so you will want to manually import them to use these filters in GOG Galaxy.

### execution
The escaped execution command to send to the operating system. Allows for expansion of the following variables.
#### %ROM_RAW%
The full filename of the software.
#### %ROM_NAME%
The filename without the path and extension.
#### %ROM_DIR%
The full path to the software.
#### path_regex
The regular expression to use to allow for the selection of the software. For most platforms this is just an escaped version of the directory where the games are stored.
#### filename_regex
The regular expression to use to select valid files.

#### Example configuration entry
The following is an example of the configuration of a single entry for a system. These objects should be enclosed in an array. Again see the example file for how this should look all together.

       {
            "name" : "dreamcast",
            "execution" : "\"C:\\Users\\andyn\\AppData\\Roaming\\RetroArch\\retroarch.exe\" -f -L \"C:\\Users\\andyn\\AppData\\Roaming\\RetroArch\\cores\\flycast_libretro.dll\" \"%ROM_RAW%\"",
            "path_regex" : "F:\\Software\\games\\roms\\Dreamcast",
            "filename_regex" : ["disc[.]gdi"]
        }

## Development notes
Will need both the standard gog plugin https://github.com/gogcom/galaxy-integrations-python-api and utils https://github.com/tylerbrawl/Galaxy-Utils packages to be placed as dependencies in the root of the folder

Also needs escapejson

    py -m pip install escapejson galaxy.plugin.api galaxyutils --target DIR

