import cherrypy
from cherrypy.lib import auth_basic
import json
import os
import os.path
from time import time
from datetime import datetime
import mimetypes

class Wiki(object):
    documentsFolder = './documents'
    invoiceCounter = os.path.join(documentsFolder, '.invoiceCounter')
    
    @cherrypy.expose
    def documentList(self):
        allDocuments = []
        
        for document in (x for x in os.listdir(self.documentsFolder) if not x.startswith('.')):
            name, date, ext = document.rsplit('.', 2)
            allDocuments.append({
                'name': document,
                'shortname': "{}.{}".format(name, ext),
                'date': date,
                'editable': self.isDocumentEditable(document)
            })
        
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(allDocuments).encode('utf8')
    
    def isDocumentEditable(self, documentName):
        _, ext = os.path.splitext(documentName)
        return ext in ('.txt', '.md')
        
    @cherrypy.expose
    def document(self, documentName):
        guessedType = mimetypes.guess_type(documentName)
        if guessedType is None:
            guessedType = 'application/octet-stream'
        
        cherrypy.response.headers['Content-Type'] = guessedType[0]
        filepath = os.path.join(self.documentsFolder, documentName)
        return open(filepath, 'rb')
        
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
    def readDocument(self):
        pass
    
    @cherrypy.expose
    def saveDocument(self):
        pass
    
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
