from xml.etree.ElementTree import ElementTree
import os

class WebsiteConstructor:

    def __init__(self,directory):
        #self.tree = ElementTree().parse(file)
        self.directory = [directory]
        self.ensureDirectory()

    def ensureDirectory(self):
        path = os.path.join(*self.directory)
        print(path)
        print('----')
        if not os.path.isdir(path):os.mkdir(path)

    def characters(self, text):
        self.out.write(text)

    def defaultStart(self,name,attrs):
        self.out.write('<' + name)
        for key,val in attrs.items():
            self.out.write(' %s=%s' % (key,val))
        self.out.write('>')

    def defaultEnd(self,name):
        self.out.write('</%s>\n' % name)

    def startDirectory(self,attrs):
        print('startDirectory')
        self.directory.append(attrs['name'])
        self.ensureDirectory()

    def endDirectory(self):
        print('endDirectory')
        self.directory.pop()

    def startPage(self,attrs):
        print('startPage')
        filename = os.path.join(*self.directory,attrs['name']+'.html')
        self.out = open(filename,'w')
        self.writeHeader(attrs['title'])

    def endPage(self):
        print('endPage')
        self.writeFooter()
        self.out.close()

    def writeHeader(self,title):
        self.out.write('<html>\n <head>\n <title>')
        self.out.write(title)
        self.out.write('</title>\n </head>\n <body>\n')

    def writeFooter(self):
        self.out.write('\n </body>\n</html>\n')

    def construct(self,tree):
        n = 0
        for child in tree:
            if child.tag == 'page':
                self.startPage(child.attrib)
                self.construct(tree[n])
                self.endPage()

            elif child.tag == 'directory':
                self.startDirectory(child.attrib)
                self.construct(tree[n])
                self.endDirectory()

            elif len(tree[n]) == 0:
                self.defaultStart(child.tag,child.attrib)
                self.characters(child.text)
                self.defaultEnd(child.tag)

            else:
                self.defaultStart(child.tag,child.attrib)
                self.construct(tree[n])
                self.defaultEnd(child.tag)
            n += 1

tree = ElementTree().parse('website.xml')
website = WebsiteConstructor('public')
website.construct(tree)

