"""
Small utility to convert MSIE favourites to an object structure.

Originally written by Fredrik Lundh.
Modified by Lars Marius Garshol
"""

import bookmark,os,string

DIR = "Favoritter" # Norwegian version

#USRDIR = os.environ["USERPROFILE"] # NT version
USRDIR = r"c:\windows" # 95 version

class MSIE:
    # internet explorer

    def __init__(self,bookmarks):
        # FIXME: use registry for this!

        self.bms=bookmarks
        self.root = None
        self.path = os.path.join(USRDIR, DIR)

        self.__walk()

    def __walk(self, subpath=[]):
        # traverse favourites folder
        path = os.path.join(self.path, string.join(subpath, os.sep))
        for file in os.listdir(path):
            fullname = os.path.join(path, file)
            if os.path.isdir(fullname):
                self.bms.add_folder(file,None,None)
                self.__walk(subpath + [file])
            else:
                url = self.__geturl(fullname)
                if url:
                    self.bms.add_bookmark(os.path.splitext(file)[0],None,
                                          None,url)

    def __geturl(self, file):
        try:
            fp = open(file)
            if fp.readline() != "[InternetShortcut]\n":
                return None
            while 1:
                s = fp.readline()
                if not s:
                    break
                if s[:4] == "URL=":
                    return s[4:-1]
        except IOError:
            pass
        return None

# --- Testprogram

if __name__ == '__main__':
    msie=MSIE(bookmark.Bookmarks())
    msie.bms.dump_xbel()
