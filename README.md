# [GalaxyGenericImporterPlugin](https://github.com/AndrewDWhite/GalaxyGenericImporterPlugin/releases/latest)
Plug-in for GOG Galaxy supporting programmatic importation of multiple platform game libraries. Allows for the generic definition of files to be added using user definable regular expressions. Programmatically imports games from predefined folders while allowing for others to be configured by users. Advanced users can also configure how games are are executed and populated into galaxy by editing the configurable regular expressions. The provides advantages over manual importation when importing many (hundreds) of programs into galaxy, assigning them tags, removing them and adding in unknown games with human readable names.

<img width="894" alt="galaxy_imported" src="https://user-images.githubusercontent.com/972757/83471895-e3d74c00-a453-11ea-8ea9-ac8f0a9c4af0.PNG">

## Known issues
- Upon galaxy update, the plugin's games may be determined to be unsupported. To resolve this for the current update as of 2020-06-15, disconnect the plugin and then reconnect it again. Contrary to galaxy's messages, your game data including play times will be retained upon reconnecting as they are also cached by the plugin.
- To preserve game data between updates ensure to copy the game_cache and game_cache-times files to the updated installation.
- To preserve configuration between versions ensure to copy the emulators.json file to the updated installation.
- If you want to allow for metadata to be stripped away between dots, like previous versions, you would add `([.].*)*` before the extension; for example gba would look like `.*[\\\\](.+?)([ ]*[\\(\\[].*[\\)\\]])*([.].*)*[.]gba` for it's regex. This expression will break games with dots in their name. You can look at the history of the configuration for some [examples](https://github.com/AndrewDWhite/GalaxyGenericImporterPlugin/blob/01ed3c6976e6cd17e805387fd0a60a5e48918973/emulators.json).
- Unknown game issues where galaxy refuses a name you provided to it or refuses to update, can sometimes be fixed by changing the username in config.cfg .
- Galaxy will place all programs under the same platform. Grouping by tags is a decent substitute so ensure to use useful ones. If you only intend to use one platform, you can also update the config.cfg file for that platform.
- To force the plug-in to re-send every program to galaxy again, useful after updating the configuration manually, remove the caches, game_cache and game_cache-times , and either completely exit and restart galaxy or disable and then re-enable the plug-in.
- If you own a lot of games, Galaxy may incorrectly report that the plug-in has crashed and force kill it for processing too long. You can try to optimize your regular expressions to allow it to execute quickly enough for it to not hit the maximum processing time.

## Installation
The plug-in will need to be placed in `%localappdata%\GOG.com\Galaxy\plugins\installed\` as `importer_97543122-7785-4444-2254-711233556699` . The easiest version to install is the [latest version](https://github.com/AndrewDWhite/GalaxyGenericImporterPlugin/releases/latest) under releases with all of the libraries pre installed and can be unzipped into the installation directory. The a [Youtube video]( https://www.youtube.com/watch?v=FCrHWRy0fOs) showing installation using default directories for software.

<img alt="installation directory with plugins installed" src="https://user-images.githubusercontent.com/972757/119213521-981b1980-ba8d-11eb-9a13-e8a8a2438c14.png">

## Default directories
If the configuration is not changed to reflect your system, then the following is used by default. Your personal `documents\games\` folder will by default be used to house the folders for your systems which will be something like `C:\Users\andyn\Documents\Games\Dreamcast` depending on your user name. See the PSP example for how to have multiple emulators for the same system for different folders and kinds of images.

| Platform | Default Emulator Location | Default Folders |
|---|---|---|
| Sega Dreamcast | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\Dreamcast\Game Name\disc.gdi |
| | | %USERPROFILE%\Documents\Games\Dreamcast |
| | | Z:\data\Software\games\roms\Dreamcast |
| Game Boy Advance | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\GBA |
| | | %USERPROFILE%\Documents\Games\GBA |
| | | Z:\data\Software\games\roms\GBA |
| | | Z:\data\Software\games\roms\GBC |
| | | Z:\data\Software\games\roms\GB |
| Game Boy Color | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\GBC |
| | | F:\Software\games\roms\GB |
| | | %USERPROFILE%\Documents\Games\GBC |
| | | %USERPROFILE%\Documents\Games\GB |
| Gamecube | %USERPROFILE%\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe | F:\Software\games\roms\GameCube |
| | | %USERPROFILE%\Documents\Games\GameCube |
| | | Z:\data\Software\games\roms\GameCube |
| Sega Genesis | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\Genesis |
| | | %USERPROFILE%\Documents\Games\Genesis |
| | | Z:\data\Software\games\roms\Genesis |
| Nintendo 64 | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\N64 |
| | | %USERPROFILE%\Documents\Games\N64 |
| | | Z:\data\Software\games\roms\N64 |
| Nintendo DS | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\nds |
| | | %USERPROFILE%\Documents\Games\nds |
| | | Z:\data\Software\games\roms\nds |
| Nintendo Entertainment System | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\nes |
| | | %USERPROFILE%\Documents\Games\NES |
| | | Z:\data\Software\games\roms\nes\roms |
| Playstation 2 | C:\Program Files (x86)\PCSX2\pcsx2.exe | F:\Software\games\roms\PS2 |
| | | %USERPROFILE%\Documents\Games\PS2 |
| | | Z:\data\Software\games\roms\PS2 |
| Playstation 3 | %USERPROFILE%\Downloads\rpcs3-v0.0.7-9236-db4041e0_win64\rpcs3.exe | F:\Software\games\roms\PS3\out |
| | | %USERPROFILE%\Documents\Games\PS3 |
| | | Z:\data\Software\games\roms\PS3\out |
| Playstation Portable | %USERPROFILE%\Downloads\ppsspp_win\PPSSPPWindows64.exe | F:\Software\games\roms\psp |
| | | %USERPROFILE%\Documents\Games\psp |
| | | Z:\data\Software\games\roms\psp |
| | C:\Program Files\PPSSPP\ppsspp_win\PPSSPPWindows64.exe | E:\roms\psp\Digital Downloads |
| | | %USERPROFILE%\Documents\Games\psp\Digital Downloads |
| Playstation 1 | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\PS1 |
| | | %USERPROFILE%\Documents\Games\PS1 |
| | | Z:\data\Software\games\roms\PS1 |
| Super Nintendo Entertainment System | %APPDATA%\RetroArch\retroarch.exe  | F:\Software\games\roms\SNES |
| | | %USERPROFILE%\Documents\Games\SNES |
| | | Z:\data\Software\games\roms\SNES |
| Wii | %USERPROFILE%\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe | F:\Software\games\roms\Wii |
| | | %USERPROFILE%\Documents\Games\Wii |
| | | Z:\data\Software\games\roms\Wii |
| XBOX | %USERPROFILE%\Downloads\CxbxReloaded-Release-VS2017\cxbx.exe | F:\Software\games\roms\xbox\games |
| | | %USERPROFILE%\Documents\Games\xbox |
| | | Z:\data\Software\games\roms\xbox\games |
| Wii U | %USERPROFILE%\Downloads\cemu_1.17.2\Cemu.exe | F:\Software\games\roms\wii u\converted |
| | | %USERPROFILE%\Documents\Games\wiiu |
| | | Z:\data\Software\games\roms\wii u\converted |
| Arcade | %USERPROFILE%\Downloads\mame0220b_64bit\mame64.exe | F:\Software\games\roms\arcade |
| | | %USERPROFILE%\Documents\Games\arcade |
| | | Z:\data\Software\games\roms\arcade |
| Amazon | | D:\Amazon Games\Library |
| | | G:\Amazon Games\Library |
| | | C:\Amazon Games\Library |
| | | %appdata%\\Microsoft\\Windows\\Start Menu\\Programs\\Amazon Games |
| DOS | C:\Program Files (x86)\DOSBox-0.74-3\DOSBox.exe | %USERPROFILE%\Documents\Games\DOS |
| | | F:\Software\games\roms\dos |
| | | Z:\data\Software\games\roms\dos |
| mods | | %USERPROFILE%\Documents\Games\mods |
| Xbox 360 | %USERPROFILE%\Downloads\xenia_master\xenia.exe | %USERPROFILE%\Documents\Games\xbox 360 |
| | | F:\Software\games\roms\xbox 360\games |
| | | Z:\data\Software\games\roms\xbox 360\games  |
| Nintendo 3DS | %APPDATA%\RetroArch\retroarch.exe | F:\Software\games\roms\3ds\roms |
| | | %USERPROFILE%\Documents\Games\3ds |
| | | Z:\data\Software\games\roms\3ds\roms |
| Vita | %USERPROFILE%\Downloads\Vita3K-master-v4761-2020-07-11-3b714115_win64\Vita3K.exe | %USERPROFILE%\Documents\Games\vita |
| | | F:\Software\games\roms\vita\roms |
| | | Z:\data\Software\games\roms\vita\roms |
| Mattel Intellivision | %APPDATA%\RetroArch\retroarch.exe  | F:\Software\games\roms\Intellivision |
| | | %USERPROFILE%\Documents\Games\intellivision |
| | | Z:\data\Software\games\roms\Intellivision |
| NeoGeo | %APPDATA%\RetroArch\retroarch.exe  | Z:\data\Software\games\roms\neogeo |
| | | %USERPROFILE%\Documents\Games\neogeo |
| Amiga | %APPDATA%\RetroArch\retroarch.exe  | Z:\data\Software\games\roms\Amiga |
| | | %USERPROFILE%\Documents\Games\Amiga |


### Sega Dreamcast
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `flycast_libretro.dll` core.
#### roms
    F:\Software\games\roms\Dreamcast\Game Name\disc.gdi
    %USERPROFILE%\Documents\Games\Dreamcast
    Z:\data\Software\games\roms\Dreamcast
By default the folders in `F:\Software\games\roms\Dreamcast` will be populated as your game names. Additionally folders in your `documents\games\Dreamcast` folder will also be populated.
### Game Boy Advance
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `mgba_libretro.dll` core.
#### roms
    F:\Software\games\roms\GBA
    %USERPROFILE%\Documents\Games\GBA
    Z:\data\Software\games\roms\GBA
### Game Boy Color
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `gambatte_libretro.dll` core.
#### roms
    F:\Software\games\roms\GBC
    F:\Software\games\roms\GB
    %USERPROFILE%\Documents\Games\GBC
    %USERPROFILE%\Documents\Games\GB
    Z:\data\Software\games\roms\GBC |
    Z:\data\Software\games\roms\GB
### Gamecube
#### emulator
    %USERPROFILE%\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe`.
#### roms
    F:\Software\games\roms\GameCube
    %USERPROFILE%\Documents\Games\GameCube
    Z:\data\Software\games\roms\GameCube
### Sega Genesis
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `genesis_plus_gx_libretro.dll` core.
#### roms
    F:\Software\games\roms\Genesis
    %USERPROFILE%\Documents\Games\Genesis
    Z:\data\Software\games\roms\Genesis
### Nintendo 64
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `mupen64plus_next_libretro.dll` core.
#### roms
    F:\Software\games\roms\N64
    %USERPROFILE%\Documents\Games\N64
    Z:\data\Software\games\roms\N64
#### Nintendo DS
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `desmume_libretro.dll` core.
#### roms
    F:\Software\games\roms\nds
    %USERPROFILE%\Documents\Games\nds
### Nintendo Entertainment System
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `nestopia_libretro.dll` core.
#### roms
    F:\Software\games\roms\nes
    %USERPROFILE%\Documents\Games\NES
    Z:\data\Software\games\roms\nes\roms
### Playstation 2
#### emulator
    C:\Program Files (x86)\PCSX2\pcsx2.exe
#### roms
    F:\Software\games\roms\PS2
    %USERPROFILE%\Documents\Games\PS2
    Z:\data\Software\games\roms\PS2
### Playstation 3
#### emulator
    %USERPROFILE%\Downloads\rpcs3-v0.0.7-9236-db4041e0_win64\rpcs3.exe
This will end up being something like `C:\Users\andyn\Downloads\rpcs3-v0.0.7-9236-db4041e0_win64\rpcs3.exe`.
#### roms
    F:\Software\games\roms\PS3\out
    %USERPROFILE%\Documents\Games\PS3
    Z:\data\Software\games\roms\PS3\out
By default the folders in `F:\Software\games\roms\PS3\out` will be populated as your game names.
### Playstation Portable
This system is setup by default as an example of having two different emulators or versions of one to launch different programs in separate folders.
#### emulator
    %USERPROFILE%\Downloads\ppsspp_win\PPSSPPWindows64.exe
This will end up being something like `C:\Users\andyn\Downloads\ppsspp_win\PPSSPPWindows64.exe`. This instance is setup to load isos of disks.

    C:\Program Files\PPSSPP\ppsspp_win\PPSSPPWindows64.exe
This one is setup for running digital downloaded PBP from the Playstation store.
#### roms
    F:\Software\games\roms\psp
    %USERPROFILE%\Documents\Games\psp
    Z:\data\Software\games\roms\psp
    E:\roms\psp\Digital Downloads
    %USERPROFILE%\Documents\Games\psp\Digital Downloads
The first three are setup for isos while the last two are for PBPs. By default the folders in `%USERPROFILE%\Documents\Games\psp\Digital Downloads` will be populated as your game names.
### Playstation 1
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `pcsx_rearmed_libretro.dll` core.
#### roms
    F:\Software\games\roms\PS1
    %USERPROFILE%\Documents\Games\PS1
    Z:\data\Software\games\roms\PS1
### Super Nintendo Entertainment System
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `snes9x_libretro.dll` core.
#### roms
    F:\Software\games\roms\SNES
    %USERPROFILE%\Documents\Games\SNES
    Z:\data\Software\games\roms\SNES
### Wii
#### emulator
    %USERPROFILE%\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\dolphin-master-5.0-11701-x64\Dolphin-x64\Dolphin.exe`.
#### roms
    F:\Software\games\roms\Wii
    %USERPROFILE%\Documents\Games\Wii
    Z:\data\Software\games\roms\Wii
### XBOX
#### emulator
    %USERPROFILE%\Downloads\CxbxReloaded-Release-VS2017\cxbx.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\CxbxReloaded-Release-VS2017\cxbx.exe`.
#### roms
    F:\Software\games\roms\xbox\games
    %USERPROFILE%\Documents\Games\xbox
    Z:\data\Software\games\roms\xbox\games
By default the folders in `F:\Software\games\roms\xbox\games` will be populated as your game names.    
### Wii U
#### emulator
    %USERPROFILE%\Downloads\cemu_1.17.2\Cemu.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\cemu_1.17.2\Cemu.exe`.
#### roms
    F:\Software\games\roms\wii u\converted
    %USERPROFILE%\Documents\Games\wiiu
    Z:\data\Software\games\roms\wii u\converted
By default the folders in `F:\Software\games\roms\wii u\converted` will be populated as your game names.  
### Arcade
#### emulator
    %USERPROFILE%\Downloads\mame0220b_64bit\mame64.exe
This will end up being something like `C:\Users\andyn\AppData\Downloads\mame0220b_64bit\mame64.exe`.
#### roms
    F:\Software\games\roms\arcade
    %USERPROFILE%\Documents\Games\arcade
    Z:\data\Software\games\roms\arcade
By default the folders in `F:\Software\games\roms\arcade` will be populated as your game names.  
### Amazon
#### game library folders
    D:\Amazon Games\Library
    G:\Amazon Games\Library
    C:\Amazon Games\Library
This will by default populate any exe files found in the root folder of each game. See the second method for the ease of use solution.

    %appdata%\\Microsoft\\Windows\\Start Menu\\Programs\\Amazon Games
This will by default use the links in the start menu created by amazon games for the applications. Is is recommended to just use this version since it is easier to create and manage.
### Dos
#### emulator
    C:\Program Files (x86)\DOSBox-0.74-3\DOSBox.exe
#### roms
    %USERPROFILE%\Documents\Games\DOS
    F:\Software\games\roms\dos
    Z:\data\Software\games\roms\dos
By default the folders in `F:\Software\games\roms\dos` will be populated as your game names. 
#### configuration starts
    %USERPROFILE%\Documents\Games\DOS\configurations
    F:\Software\games\roms\dos\configurations    
    Z:\data\Software\games\roms\dos\configurations
### mods

#### programs
    %USERPROFILE%\Documents\Games\mods
This will by default populate batch and link files into galaxy for directly launching programs such as mods. Additionally this folder by default supports launching BlueStacks application links.

<img alt="Mods default folder with a mod and a blustax link" src="https://user-images.githubusercontent.com/972757/119213717-4d9a9c80-ba8f-11eb-8f87-e6be9dc497fb.png">

### Xbox 360
#### emulator
    %USERPROFILE%\Downloads\xenia_master\xenia.exe
#### roms
    %USERPROFILE%\Documents\Games\xbox 360
    F:\Software\games\roms\xbox 360\games
    Z:\data\Software\games\roms\xbox 360\games
#### Nintendo 3DS
#### emulator
    %APPDATA%\RetroArch\retroarch.exe
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `citra_libretro.dll` core.
#### roms
    F:\Software\games\roms\3ds\roms
    %USERPROFILE%\Documents\Games\3ds
    Z:\data\Software\games\roms\3ds\roms
### Vita
#### emulator
    %USERPROFILE%\Downloads\Vita3K-master-v4761-2020-07-11-3b714115_win64\Vita3K.exe
#### roms
    %USERPROFILE%\Documents\Games\vita
    F:\Software\games\roms\vita\roms
    Z:\data\Software\games\roms\vita\roms
By default the folders in `F:\Software\games\roms\vita\roms` will be populated as your game names. 
### Mattel Intellivision
#### emulator
    %APPDATA%\RetroArch
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `freeintv_libretro.dll` core.
#### roms
    F:\Software\games\roms\Intellivision
    %USERPROFILE%\Documents\Games\intellivision
    Z:\data\Software\games\roms\Intellivision
### NeoGeo
#### emulator
     %APPDATA%\RetroArch\retroarch.exe
#### roms
    Z:\data\Software\games\roms\neogeo
    %USERPROFILE%\Documents\Games\neogeo
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `mame_libretro.dll` core. The folder names will be populated as the game names and the zip files should follow the Mame conventions.
### Amiga
#### emulator
     %APPDATA%\RetroArch\retroarch.exe
#### roms
    Z:\data\Software\games\roms\Amiga
    %USERPROFILE%\Documents\Games\Amiga
This will end up being something like `C:\Users\andyn\AppData\Roaming\RetroArch\retroarch.exe`. And use the `puae_libretro.dll` core. The folder names will be populated as the game names.
### Owned
    %USERPROFILE%\Documents\Games\Owned
By default this will populate games as ones that you own but cannot run on this device or wish to have marked as installed.
### PS4
    %USERPROFILE%\Documents\Games\ps4
    Z:\data\Software\games\roms\ps4
By default this will populate games as ones that you own but cannot run on this device or wish to have marked as installed.


## Configuration
Configuration for execution, selection and location of files is located in the `emulators.json` file. See the included for an example and for what is used by default if not changed. You will need to change this. Any platform(s) you do not need can be safely removed.

<img alt="Main configuration file for program execution" src="https://user-images.githubusercontent.com/972757/119213854-46c05980-ba90-11eb-8322-19a442eae03f.png">

### name
The different platforms names are saved as tags, so you will want to manually import them to use these filters in GOG Galaxy.

### execution
The escaped execution command to send to the operating system. Allows for expansion of the following variables.
#### %ROM_RAW%
The full filename of the software. Note that if this used without any leading executable, this can be used as the executable; see the mods section of the emulators.json file for an example.
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
The regular expression to use to select the name portion of the file. for example, `".*[\\\\](.+)[\\\\].*"` would use the last folder name as the game name. This name is normalized to remove characters which are [known](https://github.com/AndrewDWhite/GalaxyGenericImporterPlugin/issues/85) to cause issues in galaxy.
#### game_name_regex_group
The regular expression group to use from the game_name_regex match.
#### gameShouldBeInstalled
This allows programs to be listed but not marked as installed when set to false.
#### hashContent
This specifies that the game id sent to galaxy should be using a hash of the content of the data instead of the default based on name and path. Currently this requires the entire application to be loaded into ram at once for the hashing. This is planned to be expanded to allow for further identification algorithms to be specified in the future.

#### Example configuration entry
The following is an example of the configuration of a single entry for a system. These objects should be enclosed in an array. Again see the example file for how this should look all together.

       {
            "name" : "dreamcast",
            "execution" : "\"%APPDATA%\\RetroArch\\retroarch.exe\" -f -L \"%APPDATA%\\RetroArch\\cores\\flycast_libretro.dll\" \"%ROM_RAW%\"",
            "path_regex" : ["%USERPROFILE%\\Documents\\Games\\Dreamcast","F:\\Software\\games\\roms\\Dreamcast"],
            "tags" : ["retroarch"],
            "game_name_regex" : ".*[\\\\](.+?)([ ]*[\\(\\[].*[\\)\\]])*([.].*)*[\\\\](disc)[.]gdi",
            "game_name_regex_group" : 1,
            "system_rom_name_regex_group" : 4,
            "filename_regex" : ["disc[.]gdi"],
            "gameShouldBeInstalled" : true,
            "hashContent" : false
        }

## Development notes
Galaxy plug-in specific dependencies:
 - https://github.com/gogcom/galaxy-integrations-python-api 
 - https://github.com/tylerbrawl/Galaxy-Utils

Use pip to install the dependencies to your local development copy (windows example below)

     py -3.7-32 -m pip install  -r requirements.txt --target .

Run coverage tests

    ./coverage.sh

![Python package](https://github.com/AndrewDWhite/GalaxyGenericImporterPlugin/workflows/Python%20package/badge.svg?branch=master)
