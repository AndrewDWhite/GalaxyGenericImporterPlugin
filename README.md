# GalaxyGenericImporterPlugin
Plugin for GOG Galaxy to allow the generic definition of files to add using regular expressions

Will need both the standard gog plugin https://github.com/gogcom/galaxy-integrations-python-api and utils https://github.com/tylerbrawl/Galaxy-Utils packages to be placed as dependencies in the root of the folder

py -m pip install galaxy.plugin.api galaxyutils --target DIR

The plugin will need to be placed in 

%localappdata%\GOG.com\Galaxy\plugins\installed\importer_97543122-7785-4444-2254-711233556699

Configuration for execution, selection and location of files is located in the emulators.json file.

