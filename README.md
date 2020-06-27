# [GalaxyGenericImporterPlugin](https://github.com/AndrewDWhite/GalaxyGenericImporterPlugin/releases/latest)
Plugin for GOG Galaxy supporting programmatic importation of multiplatform game libraries. Allows for the generic definition of files to be added using user definable regular expressions. Programmatically imports games from predefined folders while allowing for others to be configured by users. Advanced users can also configure how games are are executed and populated into galaxy by editing the configurable regular expressions.

<img width="894" alt="galaxy_imported" src="https://user-images.githubusercontent.com/972757/83471895-e3d74c00-a453-11ea-8ea9-ac8f0a9c4af0.PNG">

## Known issues
- Upon galaxy update, the plugin's games may be determined to be unsupported. To resolve this for the current update as of 2020-06-15, disconnect the plugin and then reconnect it again. Contrary to galaxy's messages, your game data including play times will be retained upon reconnecting as they are also cached by the plugin.
- To preserve game data between updates ensure to copy the game_cache and game_cache-times files to the updated installation.
- To preserve configuration between versions ensure to copy the emulators.json file to the updated installation.

## Installation
The plugin will need to be placed in `%localappdata%\GOG.com\Galaxy\plugins\installed\` as `importer_97543122-7785-4444-2254-711233556699` . The easiest version to install is the [latest version](https://github.com/AndrewDWhite/GalaxyGenericImporterPlugin/releases/latest) under releases with all of the libraries pre installed and can be unzipped into the installation directory. The following is a Youtube video showing installation using default directories for software. https://www.youtube.com/watch?v=FCrHWRy0fOs

## Default directories
If the configuration is not changed to reflect your system, then the following is used by default. Your personal `documents\games\` folder will by default be used to house the folders for your systems which will be something like `C:\Users\andyn\Documents\Games\Dreamcast` depending on your username.

### Sega Dreamcast
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `flycast_libretro.dll` core.
#### roms
    F:\Software\games\roms\Dreamcast\Game Name\disc.gdi
    %USERPROFILE%\Documents\Games\Dreamcast
By default the folders in `F:\Software\games\roms\Dreamcast` will be populated as your game names. Additionally folders in your `documents\games\Dreamcast` folder will also be populated.
### Game Boy Advance
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `mgba_libretro.dll` core.
#### roms
    F:\Software\games\roms\GBA
    %USERPROFILE%\Documents\Games\GBA
### Game Boy Color
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `gambatte_libretro.dll` core.
#### roms
    F:\Software\games\roms\GBC
    F:\Software\games\roms\GB
    %USERPROFILE%\Documents\Games\GBC
    %USERPROFILE%\Documents\Games\GB
### Gamecube
#### emulator
    %USERPROFILE%\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe`.
#### roms
    F:\Software\games\roms\GameCube
    %USERPROFILE%\Documents\Games\GameCube
### Sega Genesis
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `genesis_plus_gx_libretro.dll` core.
#### roms
    F:\Software\games\roms\Genesis
    %USERPROFILE%\Documents\Games\Genesis
### Nintendo 64
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `mupen64plus_next_libretro.dll` core.
#### roms
    F:\Software\games\roms\N64
    %USERPROFILE%\Documents\Games\N64
#### Nintendo DS
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `desmume_libretro.dll` core.
#### roms
    F:\Software\games\roms\nds
    %USERPROFILE%\Documents\Games\nds
### Nintendo Entertainment System
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `nestopia_libretro.dll` core.
#### roms
    F:\Software\games\roms\nes
    %USERPROFILE%\Documents\Games\NES
### Playstation 2
#### emulator
    C:\Program Files (x86)\PCSX2\pcsx2.exe
#### roms
    F:\Software\games\roms\PS2
    %USERPROFILE%\Documents\Games\PS2
### Playstation 3
#### emulator
    %USERPROFILE%\Downloads\rpcs3-v0.0.7-9236-db4041e0_win64\rpcs3.exe
This will end up being something like `C:\Users\andyn\Downloads\rpcs3-v0.0.7-9236-db4041e0_win64\rpcs3.exe`.
#### roms
    F:\Software\games\roms\PS3\out
    %USERPROFILE%\Documents\Games\PS3
By default the folders in `F:\Software\games\roms\PS3\out` will be populated as your game names.
### Playstation Portable
#### emulator
    %USERPROFILE%\Downloads\ppsspp_win\PPSSPPWindows64.exe
This will end up being something like `C:\Users\andyn\Downloads\ppsspp_win\PPSSPPWindows64.exe`.
#### roms
    F:\Software\games\roms\psp
    %USERPROFILE%\Documents\Games\psp
### Playstation 1
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `pcsx_rearmed_libretro.dll` core.
#### roms
    F:\Software\games\roms\PS1
    %USERPROFILE%\Documents\Games\PS1
### Super Nintendo Entertainment System
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `snes9x_libretro.dll` core.
#### roms
    F:\Software\games\roms\SNES
    %USERPROFILE%\Documents\Games\SNES
### Wii
#### emulator
    %USERPROFILE%\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe`.
#### roms
    F:\Software\games\roms\Wii
    %USERPROFILE%\Documents\Games\Wii
### XBOX
#### emulator
    %USERPROFILE%\Downloads\CxbxReloaded-Release-VS2017\cxbx.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\CxbxReloaded-Release-VS2017\cxbx.exe`.
#### roms
    F:\Software\games\roms\xbox\games
    %USERPROFILE%\Documents\Games\xbox
By default the folders in `F:\Software\games\roms\xbox\games` will be populated as your game names.    
### Wii U
#### emulator
    %USERPROFILE%\Downloads\cemu_1.17.2\Cemu.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\cemu_1.17.2\Cemu.exe`.
#### roms
    F:\Software\games\roms\wii u\converted
    %USERPROFILE%\Documents\Games\wiiu
By default the folders in `F:\Software\games\roms\wii u\converted` will be populated as your game names.  
### Arcade
#### emulator
    %USERPROFILE%\Downloads\mame0220b_64bit\mame64.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\mame0220b_64bit\mame64.exe`.
#### roms
    F:\Software\games\roms\arcade
    %USERPROFILE%\Documents\Games\arcade
### Amazon
#### game library folders
    D:\Amazon Games\Library
    G:\Amazon Games\Library
    C:\Amazon Games\Library
This will by default populate any exe files found in the root folder of each game.
### Dos
#### emulator
    C:\Program Files (x86)\DOSBox-0.74-3\DOSBox.exe
#### roms
    %USERPROFILE%\Documents\Games\DOS
    F:\Software\games\dos
### mods

#### programs
    %USERPROFILE%\Documents\Games\mods
This will by default populate batch and link files into galaxy for directly launching programs such as mods.

## Configuration
Configuration for execution, selection and location of files is located in the `emulators.json` file. See the included for an example and used by default if not changed. You will need to change this. Any platform you do not need can be safetly removed.

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
#### tags
Optional: Additional tags to add to files.
#### game_name_regex
The regular expression to use to select the name portion of the file. for example, `".*[\\\\](.+)[\\\\].*"` would use the last folder name as the game name.
#### game_name_regex_group
The regular expression group to use from the game_name_regex match.

#### Example configuration entry
The following is an example of the configuration of a single entry for a system. These objects should be enclosed in an array. Again see the example file for how this should look all together.

       {
            "name" : "dreamcast",
            "execution" : "\"C:\\Users\\andyn\\AppData\\Roaming\\RetroArch\\retroarch.exe\" -f -L \"C:\\Users\\andyn\\AppData\\Roaming\\RetroArch\\cores\\flycast_libretro.dll\" \"%ROM_RAW%\"",
            "path_regex" : "F:\\Software\\games\\roms\\Dreamcast",
            "tags" : ["retroarch"],
            "game_name_regex" : ".*[\\\\](.+)[\\\\].*",
            "game_name_regex_group" : 1,
            "filename_regex" : ["disc[.]gdi"]
        }

## Development notes
Galaxy plugin specific dependencies:
 - https://github.com/gogcom/galaxy-integrations-python-api 
 - https://github.com/tylerbrawl/Galaxy-Utils

Use pip to install the dependencies to your local development copy (windows example below)

     py -3.7-32 -m pip install  -r requirements.txt --target .

Run coverage tests

    ./coverage.sh

![Python package](https://github.com/AndrewDWhite/GalaxyGenericImporterPlugin/workflows/Python%20package/badge.svg?branch=master)
