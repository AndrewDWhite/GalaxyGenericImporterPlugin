# GalaxyGenericImporterPlugin
Plugin for GOG Galaxy to allow the generic definition of software using regular expressions.

## Installation
The plugin will need to be placed in 

    %localappdata%\GOG.com\Galaxy\plugins\installed\importer_97543122-7785-4444-2254-711233556699

Youtube video showing installation using default directories for software.

https://www.youtube.com/watch?v=FCrHWRy0fOs

## Configuration

Configuration for execution, selection and location of files is located in the emulators.json file.

The different platforms names are saved as tags, so you will want to manually import them to use these filters in GOG GAlaxy.



## Development notes

Will need both the standard gog plugin https://github.com/gogcom/galaxy-integrations-python-api and utils https://github.com/tylerbrawl/Galaxy-Utils packages to be placed as dependencies in the root of the folder

Also needs escapejson

    py -m pip install escapejson galaxy.plugin.api galaxyutils --target DIR

