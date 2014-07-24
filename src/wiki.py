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
    
    def listAllDocuments(self):
        for document in (x for x in os.listdir(self.documentsFolder) if not x.startswith('.')):
            name, date, ext = self.splitDocumentName(document)
            yield "{}.{}".format(name, ext), document, date
    
    @cherrypy.expose
    def documentList(self):
        allDocuments = {}
        
        for shortname, fullname, date in self.listAllDocuments():
            if shortname not in allDocuments or allDocuments[shortname]['date'] < date:
                allDocuments[shortname] = {
                    'name': fullname,
                    'shortname': shortname,
                    'date': date,
                    'mimetype': self.mimetype(shortname)
                }
        
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(list(allDocuments.values())).encode('utf8')
    
    @cherrypy.expose
    def documentVersions(self, documentShortName):
        allVersions = []
        
        for shortName, fullname, date in self.listAllDocuments():
            if shortName == documentShortName:
                allVersions.append({
                    'name': fullname,
                    'shortname': shortName,
                    'date': date,
                    'mimetype': self.mimetype(shortName)
                })
        
        cherrypy.response.headers['Content-Type'] = "application/json"
        return json.dumps(allVersions).encode('utf8');
    
    def splitDocumentName(self, documentName):
        name, date, ext = documentName.rsplit('.', 2)
        return name, date, ext
    
    def mimetype(self, documentName):
        guessedType = mimetypes.guess_type(documentName)
        if guessedType is None:
            guessedType = 'application/octet-stream'
            
        return guessedType[0]
    
    def isDocumentEditable(self, documentName):
        _, ext = os.path.splitext(documentName)
        return ext in ('.txt', '.md')
        
    @cherrypy.expose
    def document(self, documentName):
        cherrypy.response.headers['Content-Type'] = self.mimetype(documentName)
        filepath = os.path.join(self.documentsFolder, documentName)
        return open(filepath, 'rb')
    
    @cherrypy.expose
    def download(self, documentName):
        cherrypy.response.headers['Content-Disposition'] = 'attachment'
        return self.document(documentName)
        
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
