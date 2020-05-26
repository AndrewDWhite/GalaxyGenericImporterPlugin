# GalaxyGenericImporterPlugin
Plugin for GOG Galaxy to allow the generic definition of software using regular expressions.

## Installation
The plugin will need to be placed in `%localappdata%\GOG.com\Galaxy\plugins\installed\` as `importer_97543122-7785-4444-2254-711233556699` . The easiest version to install is the lastest version under releases with all of the libraries pre installed and can be unzipped into the installation directory. The following is a Youtube video showing installation using default directories for software. https://www.youtube.com/watch?v=FCrHWRy0fOs

## Default directories
If the configuration is not changed to reflect your system, then the following is used by default.

### Sega Dreamcast
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `flycast_libretro.dll` core.
#### roms
    F:\Software\games\roms\Dreamcast\Game Name\disc.gdi
By default the folders in `F:\Software\games\roms\Dreamcast` will be populated as your game names.
### Game Boy Advance
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `mgba_libretro.dll` core.
#### roms
    F:\Software\games\roms\GBA
### Game Boy Color
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `gambatte_libretro.dll` core.
#### roms
    F:\Software\games\roms\GBC
    F:\Software\games\roms\GB
### Gamecube
#### emulator
    %USERPROFILE%\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe`.
#### roms
    F:\Software\games\roms\GameCube
### Sega Genesis
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `genesis_plus_gx_libretro.dll` core.
#### roms
    F:\Software\games\roms\Genesis
### Nintendo 64
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `mupen64plus_next_libretro.dll` core.
#### roms
    F:\Software\games\roms\N64
#### Nintendo DS
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `desmume_libretro.dll` core.
#### roms
    F:\Software\games\roms\nds
### Nintendo Entertainment System
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `nestopia_libretro.dll` core.
#### roms
    F:\Software\games\roms\nes
### Playstation 2
#### emulator
    C:\Program Files (x86)\PCSX2\pcsx2.exe
#### roms
    F:\Software\games\roms\PS2
### Playstation 3
#### emulator
    %USERPROFILE%\Downloads\rpcs3-v0.0.7-9236-db4041e0_win64\rpcs3.exe
This will end up being something like `C:\Users\andyn\Downloads\rpcs3-v0.0.7-9236-db4041e0_win64\rpcs3.exe`.
#### roms
    F:\Software\games\roms\PS3\out
By default the folders in `F:\Software\games\roms\PS3\out` will be populated as your game names.
### Playstation Portable
#### emulator
    %USERPROFILE%\Downloads\ppsspp_win\PPSSPPWindows64.exe
This will end up being something like `C:\Users\andyn\Downloads\ppsspp_win\PPSSPPWindows64.exe`.
#### roms
    F:\Software\games\roms\psp
### Playstation 1
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `pcsx_rearmed_libretro.dll` core.
#### roms
    F:\Software\games\roms\PS1
### Super Nintendo Entertainment System
#### emulator
    %USERPROFILE%\AppData\Roaming\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `snes9x_libretro.dll` core.
#### roms
    F:\Software\games\roms\SNES
### Wii
#### emulator
    %USERPROFILE%\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe`.
#### roms
    F:\Software\games\roms\Wii
### XBOX
#### emulator
    %USERPROFILE%\Downloads\CxbxReloaded-Release-VS2017\cxbx.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\CxbxReloaded-Release-VS2017\cxbx.exe`.
#### roms
    F:\Software\games\roms\xbox\games
By default the folders in `F:\Software\games\roms\xbox\games` will be populated as your game names.    
### Wii U
#### emulator
    %USERPROFILE%\Downloads\cemu_1.17.2\Cemu.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\cemu_1.17.2\Cemu.exe`.
#### roms
    F:\Software\games\roms\wii u\converted
By default the folders in `F:\Software\games\roms\wii u\converted` will be populated as your game names.  
### Arcade
#### emulator
    %USERPROFILE%\Downloads\mame0220b_64bit\mame64.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\mame0220b_64bit\mame64.exe`.
#### roms
    F:\Software\games\roms\arcade

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
Will need both the standard gog plugin https://github.com/gogcom/galaxy-integrations-python-api and utils https://github.com/tylerbrawl/Galaxy-Utils packages to be placed as dependencies in the root of the folder

Also needs escapejson

    py -m pip install escapejson galaxy.plugin.api galaxyutils --target DIR

