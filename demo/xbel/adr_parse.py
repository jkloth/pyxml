"""
Small utility to parse Opera bookmark files.
Written by Lars Marius Garshol
"""

import string,bookmark

# --- Constants

short_months={"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05",
              "Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10",
              "Nov":"11","Dec":"12"}

# --- Parsing exception

class OperaParseException(Exception):
    pass

# --- Methods
        
def readfield(infile,fieldname):
    line=infile.readline()
    pos=string.find(line,fieldname+"=")
    if pos==-1:
        raise OperaParseException("Field '%s' missing" % fieldname)

    return line[pos+len(fieldname)+1:-1]

def swallow_rest(infile):
    "Reads input until first blank line."
    while 1:
        line=infile.readline()
        if line=="" or line=="\n": break

def parse_date(date):
    # CREATED=904923783 (Fri Sep 04 17:43:03 1998)
    # VISITED=0 (?)
    lp=string.find(date,"(")
    rp=string.find(date,")")
    if lp==-1 or rp==-1:
        raise OperaParseException("Date without parentheses")

    if date[lp:rp+1]=="(?)":
        return None

    month=short_months[date[lp+5:lp+8]]
    day=date[lp+9:lp+11]
    year=date[rp-4:rp]

    return "%s%s%s" % (year,month,day)

def parse_adr(filename):
    bms=bookmark.Bookmarks()
    
    infile=open(filename)
    version=infile.readline()

    while 1:
        line=infile.readline()
        if line=="": break
        
        if line[:-1]=="#FOLDER":
            name=readfield(infile,"NAME")
            created=parse_date(readfield(infile,"CREATED"))
            visited=parse_date(readfield(infile,"VISITED"))
            order=readfield(infile,"ORDER")
            swallow_rest(infile)

            bms.add_folder(name,created,visited)
        elif line[:-1]=="#URL":
            name=readfield(infile,"NAME")
            url=readfield(infile,"URL")
            created=parse_date(readfield(infile,"CREATED"))
            visited=parse_date(readfield(infile,"VISITED"))
            order=readfield(infile,"ORDER")
            swallow_rest(infile)

            bms.add_bookmark(name,created,visited,url)
        elif line[:-1]=="-":
            bms.leave_folder()

    return bms

# --- Test-program

if __name__ == '__main__':
    bms=parse_adr(r"c:\programfiler\opera\opera3.adr")
    bms.dump_xbel()
