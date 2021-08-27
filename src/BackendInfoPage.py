import logging
import asyncio

from configuration import DefaultConfig
from Backend import Backend
from ListGames import ListGames
from piptools.writer import OutputWriter

class BackendInfoPage():

    async def generatePage(self):
        self.configuration = DefaultConfig()
        self.backend = Backend()
        await self.backend.setup(self.configuration)
        
        logger.info("Loading data:")
        systems = ListGames()
        data_read = await systems.read_from_cache()
        if (len(data_read)>0):
            outputFile = open("cache.html", "w")
            outputFile.write(str("<html><head><title>Cache</title></head><body><table>"))
            for headerKey in data_read[0]:
                outputFile.write(str("<th>"+str(headerKey)+"</th>"))
            for entry in data_read:
                logger.info(entry)
                outputFile.write(str("<tr>"))
                for key in entry:
                    if (key=="hash_digest"):
                        outputFile.write(str("<td><a href='https://gamesdb.gog.com/platforms/test/external_releases/"+str(entry[key])+"'>"+str(entry[key])+"</td>"))
                    else:
                        outputFile.write(str("<td>"+str(entry[key])+"</td>"))
                outputFile.write(str("</tr>"))
            outputFile.write(str("</body></html>"))
    
    def main(self):
        asyncio.run(BackendInfoPage.generatePage(self))
        
if __name__ == "__main__":
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    runner = BackendInfoPage();
    runner.main()