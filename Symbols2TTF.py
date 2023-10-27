
import fontforge
import xml.etree.ElementTree as ET

class Symbols2TTF(object):
    """Symbols2TTF class"""

    def __init__(self, opts={
        'force_chars': False
    }):
        """Constructor function"""

        ET.register_namespace('','http://www.w3.org/2000/svg')

        self.font = fontforge.font() # create a new font
        self.ns   = {'': 'http://www.w3.org/2000/svg'}
        self.force_chars = opts['force_chars']


    def collectGlyphsBy(self, tree=ET.ElementTree, map_chars=u'A', map_ids=[]):
        """Walks through SVG <symbol> elements and creates glyphs from them."""

        idNUM = len(map_ids)
        chMAX = len(map_chars)
        nss = self.ns
        tag = './/{http://www.w3.org/2000/svg}symbol'

        if chMAX == 0:
            chMAX = 1
            map_chars = u'A'

        if idNUM == 1:
            tag += f'[@id="{map_ids[0]}"]'

        root  = tree.getroot()
        elems = root.findall(tag, namespaces=nss)
        elCNT = max(idNUM, len(elems))
        index = 0

        if (self.force_chars):
            if (elCNT > chMAX):
                map_chars = self.nearMapChars(map_chars[chMAX-1], elCNT - chMAX)
            chMAX = elCNT

        if idNUM == 0:
            for el in elems:
                char = id = map_chars[index]
                file = self.createSvgFrom(el, id)
                self.importGlyphFrom(file, char)
                index += 1
                if index >= chMAX:
                    break
        else:
            for el in elems:
                id = el.attrib.get('id')
                if id in map_ids:
                    char = map_chars[map_ids.index(id)]
                    file = self.createSvgFrom(el, id)
                    self.importGlyphFrom(file, char)
                    index += 1
                if index >= chMAX:
                    break

    def nearMapChars(self, start=u'A', count=3):
        chars = []
        first = ord(start)
        index = 0
        while index < count:
            chars.append(chr(first + index))
            index += 1
        return u''.join(chars)

    def importGlyphFrom(self, filename='', char=u'A'):
        glyph = self.font.createMappedChar(char)
        glyph.importOutlines(filename)

    def createSvgFrom(self, el=ET.Element, id=''):

        tree = ET.ElementTree(el)
        root = tree.getroot()
        file = f'gliph-ff-{id}.svg'
        root.tag = '{http://www.w3.org/2000/svg}svg'

        with open(file, 'wb') as f:
            tree.write(f, encoding = 'utf-8', method = 'xml')
        return file

    def loadSvgTree(self, svgfile=''):
        """Load and parse SVG from file"""
        return ET.parse(svgfile)

    def saveResult(self, filename='result.ttf'):
        self.font.generate(filename)

def fromSvgList(
        svg_list = [],
        map_chars = u'ABC',
        map_ids = [],
        output = 'result.ttf'
    ):
    if type(svg_list) != list or len(svg_list) == 0:
        raise ValueError('svg files list is empty.')

    ttf = Symbols2TTF()
    for svg in svg_list:
        tree = ttf.loadSvgTree(svg)
        ttf.collectGlyphsBy(tree, map_chars, map_ids)
    ttf.saveResult(output)
