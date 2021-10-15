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
            outputFile.write(str(
                "<html>\
                <head>\
                <meta charset='UTF-8'>\
                <title>Cache</title>\
                </head>\
                <body>\
                <script src='https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'></script>\
                <link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/1.11.0/css/jquery.dataTables.css'>\
                <script type='text/javascript' charset='utf8' src='https://cdn.datatables.net/1.11.0/js/jquery.dataTables.js'></script>\
                <script type='text/javascript' charset='utf8' src='https://cdn.datatables.net/select/1.3.3/js/dataTables.select.js'></script>\
                <link rel='stylesheet' type='text/css' href='https://cdn.datatables.net/select/1.3.3/css/select.dataTables.css'>\
                <table id='mytable' class='display'>"
                ))
            outputFile.write(str("<thead><tr>"))
            for headerKey in data_read[0]:
                outputFile.write(str("<th>"+str(headerKey)+"</th>"))
            outputFile.write(str("</tr></thead><tbody>"))
            for entry in data_read:
                logger.info(entry)
                outputFile.write(str("<tr>"))
                for key in entry:
                    if (key=="hash_digest"):
                        outputFile.write(str("<td><a href='https://gamesdb.gog.com/platforms/test/external_releases/"+str(entry[key])+"'>"+str(entry[key])+"</td>"))
                    else:
                        outputFile.write(str("<td>"+str(entry[key])+"</td>"))
                outputFile.write(str("</tr>"))
            outputFile.write(str("</tbody></table><script type='text/javascript'>$(document).ready( function () {    $('#mytable').DataTable({select: {style: 'single'}});} );</script></body></html>"))
    
    def main(self):
        asyncio.run(BackendInfoPage.generatePage(self))
        
if __name__ == "__main__":
    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG)
    runner = BackendInfoPage();
    runner.main()