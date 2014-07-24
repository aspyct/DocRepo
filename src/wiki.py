import cherrypy
from cherrypy.lib import auth_basic
import json
import os
import os.path
from time import time
from datetime import datetime

class Wiki(object):
    documentsFolder = './documents'
    invoiceCounter = os.path.join(documentsFolder, '.invoiceCounter')
    
    @cherrypy.expose
    def documentList(self):
        allDocuments = [{'name': x} for x in os.listdir(self.documentsFolder) if not x.startswith('.')]
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(allDocuments).encode('utf8')
        
    @cherrypy.expose
    def uploadDocument(self, document):
        documentName, documentExtension = os.path.splitext(document.filename)
        documentDate = datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        print(documentDate)
        
        filename = "{}.{}{}".format(documentName, documentDate, documentExtension)
        filepath = os.path.join(self.documentsFolder, filename)
        with open(filepath, 'wb') as f:
            data = document.file.read()
            f.write(data)
            
        raise cherrypy.HTTPRedirect('/')
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def invoiceNumber(self):
        with open(self.invoiceCounter, 'r+') as f:
            data = f.read()
            
            if not data:
                data = '0'
            
            invoiceNumber = int(data) + 1
            f.seek(0)
            f.write(str(invoiceNumber))
            
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps({
            'invoiceNumber': invoiceNumber
        }).encode('utf8')
        

if __name__ == '__main__':
    cherrypy.quickstart(Wiki(), '', config='conf.ini')
