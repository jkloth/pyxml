/*
 * SGMLOP
 * $Id: sgmlop.c,v 1.2 1998/09/16 01:04:37 amk Exp $
 *
 * The sgmlop accelerator module
 *
 * This module provides a FastSGMLParser class, which is designed
 * to speed up the standard sgmllib and xmllib modules.  A parser
 * instance can be configured to support either basic SGML (enough
 * of it to process HTML documents, at least) or XML.
 *
 * History:
 * 98-04-04 fl  Created (for coreXML)
 * 98-04-05 fl  Added close method
 * 98-04-06 fl  Added parse method, revised callback interface
 * 98-04-14 fl  Fixed parsing of PI tags
 * 98-05-14 fl  Cleaned up for first public release
 * 98-05-19 fl  Fixed xmllib compatibility: handle_proc, handle_special
 * 98-05-22 fl  Added attribute parser
 * 98-05-23 fl  Added saxlib callback mode
 *
 * Copyright (c) 1998 by Secret Labs AB.
 *
 * fredrik@pythonware.com
 * http://www.pythonware.com
 *
 * --------------------------------------------------------------------
 * Permission to use, copy, modify, and distribute this software and
 * its associated documentation for any purpose and without fee is
 * hereby granted.  This software is provided as is.
 * --------------------------------------------------------------------
 */

#include "Python.h"

#include <ctype.h>

#ifdef USE_WCHAR
/* wide character set */
#include <wchar.h>
#define CHAR_T  wchar_t
#define ISALNUM iswalnum
#define ISSPACE iswspace
#define TOLOWER towlower
#else
/* 8-bit character set */
#define CHAR_T  char
#define ISALNUM isalnum
#define ISSPACE isspace
#define TOLOWER tolower
#endif

/* state flags */
#define MAYBE 1
#define SURE 2

/* parser type definition */
typedef struct {
    PyObject_HEAD

    /* mode flags */
    int xml; /* 0=sgml/html 1=xml */
    int saxlib; /* 0=xmllib/sgmllib callbacks 1=saxlib callbacks */

    /* state attributes */
    int shorttag; /* 0=normal 2=parsing shorttag */
    int doctype; /* 0=normal 1=dtd pending 2=parsing dtd */

    /* buffer (holds incomplete tags) */
    char* buffer;
    int bufferlen; /* current amount of data */
    int buffertotal; /* actually allocated */

    /* callbacks */
    PyObject* finish_starttag;
    PyObject* finish_endtag;
    PyObject* handle_proc;
    PyObject* handle_special;
    PyObject* handle_charref;
    PyObject* handle_entityref;
    PyObject* handle_data;
    PyObject* handle_cdata;
    PyObject* handle_comment;

} FastSGMLParserObject;

staticforward PyTypeObject FastSGMLParser_Type;

/* forward declarations */
static int fastfeed(FastSGMLParserObject* self);
static PyObject* attrparse(const CHAR_T *p, int len, int xml);


/* -------------------------------------------------------------------- */
/* create parser */

static PyObject*
_sgmlop_new(int xml)
{
    FastSGMLParserObject* self;

    self = PyObject_NEW(FastSGMLParserObject, &FastSGMLParser_Type);
    if (self == NULL)
        return NULL;

    self->xml = xml;

    self->shorttag = 0;
    self->doctype = 0;

    self->buffer = NULL;
    self->bufferlen = 0;
    self->buffertotal = 0;

    self->finish_starttag = NULL;
    self->finish_endtag = NULL;
    self->handle_proc = NULL;
    self->handle_special = NULL;
    self->handle_charref = NULL;
    self->handle_entityref = NULL;
    self->handle_data = NULL;
    self->handle_cdata = NULL;
    self->handle_comment = NULL;

    return (PyObject*) self;
}

static PyObject*
_sgmlop_sgmlparser(PyObject* self, PyObject* args)
{
    if (!PyArg_NoArgs(args))
        return NULL;

    return _sgmlop_new(0);
}

static PyObject*
_sgmlop_xmlparser(PyObject* self, PyObject* args)
{
    if (!PyArg_NoArgs(args))
        return NULL;

    return _sgmlop_new(1);
}

static void
_sgmlop_dealloc(FastSGMLParserObject* self)
{
    if (self->buffer)
        free(self->buffer);
    Py_XDECREF(self->finish_starttag);
    Py_XDECREF(self->finish_endtag);
    Py_XDECREF(self->handle_proc);
    Py_XDECREF(self->handle_special);
    Py_XDECREF(self->handle_charref);
    Py_XDECREF(self->handle_entityref);
    Py_XDECREF(self->handle_data);
    Py_XDECREF(self->handle_cdata);
    Py_XDECREF(self->handle_comment);
    PyMem_DEL(self);
}

#define GETCB(member, name)\
    Py_XDECREF(self->member);\
    self->member = PyObject_GetAttrString(item, name);

static PyObject*
_sgmlop_register(FastSGMLParserObject* self, PyObject* args)
{
    /* register a callback object */
    PyObject* item;
    int saxlib = 0;
    if (!PyArg_ParseTuple(args, "O|i", &item, &saxlib))
        return NULL;

    if (saxlib) {

        /* saxlib DocumentHandler callbacks */

        self->saxlib = 1;

        GETCB(finish_starttag, "startElement");
        GETCB(finish_endtag, "endElement");
        GETCB(handle_proc, "processingInstruction");
        GETCB(handle_special, "handle_special"); /* FIXME: ??? */
        Py_XDECREF(self->handle_charref); self->handle_charref = NULL;
        GETCB(handle_entityref, "handle_entityref"); /* FIXME: ??? */
        GETCB(handle_data, "characters");
        GETCB(handle_cdata, "characters");
        Py_XDECREF(self->handle_comment); self->handle_comment = NULL;

    } else {

        /* sgmllib/xmllib callbacks */

        self->saxlib = 0;

        GETCB(finish_starttag, "finish_starttag");
        GETCB(finish_endtag, "finish_endtag");
        GETCB(handle_proc, "handle_proc");
        GETCB(handle_special, "handle_special");
        GETCB(handle_charref, "handle_charref");
        GETCB(handle_entityref, "handle_entityref");
        GETCB(handle_data, "handle_data");
        GETCB(handle_cdata, "handle_cdata");
        GETCB(handle_comment, "handle_comment");
        
    }

    Py_INCREF(Py_None);
    return Py_None;
}


/* -------------------------------------------------------------------- */
/* feed data to parser.  the parser processes as much of the data as
   possible, and keeps the rest in a local buffer. */

static PyObject*
feed(FastSGMLParserObject* self, char* string, int stringlen, int last)
{
    /* common subroutine for SGMLParser.feed and SGMLParser.close */

    int length;

    /* append new text block to local buffer */
    if (!self->buffer) {
        length = stringlen;
        self->buffer = malloc(length);
        self->buffertotal = stringlen;
    } else {
        length = self->bufferlen + stringlen;
        if (length > self->buffertotal) {
            self->buffer = realloc(self->buffer, length);
            self->buffertotal = length;
        }
    }
    if (!self->buffer) {
        PyErr_NoMemory();
        return NULL;
    }
    memcpy(self->buffer + self->bufferlen, string, stringlen);
    self->bufferlen = length;

    length = fastfeed(self);
    if (length < 0)
        return NULL;

    if (length > self->bufferlen) {
        /* ran beyond the end of the buffer (internal error)*/
        PyErr_SetString(PyExc_RuntimeError, "buffer overrun");
        return NULL;
    }

    if (length > 0 && length < self->bufferlen)
        /* adjust buffer */
        memmove(self->buffer, self->buffer + length,
                self->bufferlen - length);

    self->bufferlen = self->bufferlen - length;

    return Py_BuildValue("i", self->bufferlen);
}

static PyObject*
_sgmlop_feed(FastSGMLParserObject* self, PyObject* args)
{
    /* feed a chunk of data to the parser */

    char* string;
    int stringlen;
    if (!PyArg_ParseTuple(args, "s#", &string, &stringlen))
        return NULL;

    return feed(self, string, stringlen, 0);
}

static PyObject*
_sgmlop_close(FastSGMLParserObject* self, PyObject* args)
{
    /* feed final chunk of data to the parser */

    char* string = "";
    int stringlen = 0;
    if (!PyArg_ParseTuple(args, "|s#", &string, &stringlen))
        return NULL;

    return feed(self, string, stringlen, 1);
}

static PyObject*
_sgmlop_parse(FastSGMLParserObject* self, PyObject* args)
{
    /* feed a single chunk of data to the parser */

    char* string;
    int stringlen;
    if (!PyArg_ParseTuple(args, "s#", &string, &stringlen))
        return NULL;

    return feed(self, string, stringlen, 1);
}


/* -------------------------------------------------------------------- */
/* type interface */

static PyMethodDef _sgmlop_methods[] = {
    /* register callbacks */
    {"register", (PyCFunction) _sgmlop_register, 1},
    /* incremental parsing */
    {"feed", (PyCFunction) _sgmlop_feed, 1},
    {"close", (PyCFunction) _sgmlop_close, 1},
    /* one-shot parsing */
    {"parse", (PyCFunction) _sgmlop_parse, 1},
    {NULL, NULL}
};

static PyObject*  
_sgmlop_getattr(FastSGMLParserObject* self, char* name)
{
    return Py_FindMethod(_sgmlop_methods, (PyObject*) self, name);
}

statichere PyTypeObject FastSGMLParser_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                          /*ob_size*/
    "FastSGMLParser", 		/*tp_name*/
    sizeof(FastSGMLParserObject), /*tp_size*/
    0,                          /*tp_itemsize*/
    /* methods */
    (destructor)_sgmlop_dealloc, /*tp_dealloc*/
    0,                          /*tp_print*/
    (getattrfunc)_sgmlop_getattr, /*tp_getattr*/
    0                           /*tp_setattr*/
};

static PyMethodDef _functions[] = {
    {"SGMLParser", _sgmlop_sgmlparser, 0},
    {"XMLParser", _sgmlop_xmlparser, 0},
    {NULL, NULL}
};

void
#ifdef WIN32
__declspec(dllexport)
#endif
#ifdef USE_WCHAR
initwsgmlop()
{
    /* Patch object type */
    FastSGMLParser_Type.ob_type = &PyType_Type;

    Py_InitModule("wsgmlop", _functions);
}
#else
initsgmlop()
{
    /* Patch object type */
    FastSGMLParser_Type.ob_type = &PyType_Type;

    Py_InitModule("sgmlop", _functions);
}
#endif

/* -------------------------------------------------------------------- */
/* the parser does it all in a single loop, keeping the necessary
   state in a few flag variables and the data buffer.  if you have
   a good optimizer, this can be incredibly fast. */

#define TAG 0x100
#define TAG_START 0x101
#define TAG_END 0x102
#define TAG_EMPTY 0x103
#define DIRECTIVE 0x104
#define DOCTYPE 0x105
#define PI 0x106
#define DTD_START 0x107
#define DTD_END 0x108
#define DTD_ENTITY 0x109
#define CDATA 0x200
#define ENTITYREF 0x400
#define CHARREF 0x401
#define COMMENT 0x800

static int
fastfeed(FastSGMLParserObject* self)
{
    CHAR_T *end; /* tail */
    CHAR_T *p, *q, *s; /* scanning pointers */
    CHAR_T *b, *t, *e; /* token start/end */

    int token;

    s = q = p = (CHAR_T*) self->buffer;
    end = (CHAR_T*) (self->buffer + self->bufferlen);

    while (p < end) {

        q = p; /* start of token */

        if (*p == '<') {
            int has_attr;

            /* <tags> */
            token = TAG_START;
            if (++p >= end)
                goto eol;

            if (*p == '!') {
                /* <! directive */
                if (++p >= end)
                    goto eol;
                token = DIRECTIVE;
                b = t = p;
                if (*p == '-') {
                    /* <!-- comment --> */
                    token = COMMENT;
                    b = p + 2;
                    for (;;) {
                        if (p+3 >= end)
                            goto eol;
                        if (p[1] != '-')
                            p += 2; /* boyer moore, sort of ;-) */
                        else if (p[0] != '-' || p[2] != '>')
                            p++;
                        else
                            break;
                    }
                    e = p;
                    p += 3;
                    goto eot;
                } else if (self->xml) {
                    /* FIXME: recognize <!ATTLIST data> ? */
                    /* FIXME: recognize <!ELEMENT data> ? */
                    /* FIXME: recognize <!ENTITY data> ? */
                    /* FIXME: recognize <!NOTATION data> ? */
                    if (*p == 'D' ) {
                        /* FIXME: make sure this really is a !DOCTYPE tag */
                        /* <!DOCTYPE data> or <!DOCTYPE data [ data ]> */
                        token = DOCTYPE;
                        self->doctype = MAYBE;
                    } else if (*p == '[') {
                        /* FIXME: make sure this really is a ![CDATA[ tag */
                        /* FIXME: recognize <![INCLUDE */
                        /* FIXME: recognize <![IGNORE */
                        /* <![CDATA[data]]> */
                        token = CDATA;
                        b = t = p + 7;
                        for (;;) {
                            if (p+3 >= end)
                                goto eol;
                            if (p[1] != ']')
                                p += 2;
                            else if (p[0] != ']' || p[2] != '>')
                                p++;
                            else
                                break;
                        }
                        e = p;
                        p += 3;
                        goto eot;
                    }
                }
            } else if (*p == '?') {
                token = PI;
                if (++p >= end)
                    goto eol;
            } else if (*p == '/') {
                /* </endtag> */
                token = TAG_END;
                if (++p >= end)
                    goto eol;
            }

            /* process tag name */
            b = p;
            if (!self->xml)
                /* FIXME: is SGML not case sensitive? */
                while (ISALNUM(*p) || *p == '-' || *p == ':' || *p == '?') {
                    *p = TOLOWER(*p);
                    if (++p >= end)
                        goto eol;
                }
            else
                /* FIXME: is XML case sensitive? */
                while (ISALNUM(*p) || *p == '-' || *p == ':' || *p == '?')
                    if (++p >= end)
                        goto eol;
            t = p;

            has_attr = 0;

            if (*p == '/' && !self->xml) {
                /* <tag/data/ or <tag/> */
                token = TAG_START;
                e = p;
                if (++p >= end)
                    goto eol;
                if (*p == '>') {
                    /* <tag/> */
                    token = TAG_EMPTY;
                    if (++p >= end)
                        goto eol;
                } else
                    /* <tag/data/ */
                    self->shorttag = SURE;
                    /* we'll generate an end tag when we stumble upon
                       the end slash */

            } else {

                /* skip attributes */
                int quote = 0;
                int last = 0;
                while (*p != '>' || quote) {
                    if (!ISSPACE(*p)) {
                        has_attr = 1;
                        /* FIXME: note: end tags cannot have attributes! */
                    }
                    if (quote) {
                        if (*p == quote)
                            quote = 0;
                    } else {
                        if (*p == '"' || *p == '\'')
                            quote = *p;
                    }
                    if (*p == '[' && !quote && self->doctype) {
                        self->doctype = SURE;
                        token = DTD_START;
                        e = p++;
                        goto eot;
                    }
                    last = *p;
                    if (++p >= end)
                        goto eol;
                }

                e = p++;

                if (last == '/') {
                    /* <tag/> */
                    e--;
                    token = TAG_EMPTY;
                } else if (token == PI && last == '?')
                    e--;

                if (self->doctype == MAYBE)
                    self->doctype = 0; /* there was no dtd */

                if (has_attr)
                    ; /* FIXME: process attributes */

            }

        } else if (*p == '/' && self->shorttag) {

            /* end of shorttag. this generates an empty end tag */
            token = TAG_END;
            self->shorttag = 0;
            b = t = e = p;
            if (++p >= end)
                goto eol;

        } else if (*p == ']' && self->doctype) {

            /* end of dtd. this generates an empty end tag */
            token = DTD_END;
            /* FIXME: who handles the ending > !? */
            b = t = e = p;
            if (++p >= end)
                goto eol;
            self->doctype = 0;

        } else if (*p == '%' && self->doctype) {

            /* doctype entities */
            token = DTD_ENTITY;
            if (++p >= end)
                goto eol;
            b = t = p;
            while (ISALNUM(*p) || *p == '.')
                if (++p >= end)
                    goto eol;
            e = p;
            if (*p == ';')
                p++;

        } else if (*p == '&') {

            /* entities */
            token = ENTITYREF;
            if (++p >= end)
                goto eol;
            if (*p == '#') {
                token = CHARREF;
                if (++p >= end)
                    goto eol;
            }
            b = t = p;
            while (ISALNUM(*p) || *p == '.')
                if (++p >= end)
                    goto eol;
            e = p;
            if (*p == ';')
                p++;

        } else {

            /* raw data */
            if (++p >= end)
                goto eol;
            continue;

        }

      eot: /* end of token */

        if (q != s && self->handle_data) {
            /* flush any raw data before this tag */
            PyObject* res;
            if (self->saxlib)
                res = PyObject_CallFunction(self->handle_data,
                                            "s#ii", s, q-s, 0, q-s);
            else
                res = PyObject_CallFunction(self->handle_data,
                                            "s#", s, q-s);
            if (!res)
                return -1;
            Py_DECREF(res);
        }

        /* invoke callbacks */
        if (token & TAG) {
            if (token == TAG_END) {
                if (self->finish_endtag) {
                    PyObject* res;
                    res = PyObject_CallFunction(self->finish_endtag,
                                                "s#", b, t-b);
                    if (!res)
                        return -1;
                    Py_DECREF(res);
                }
            } else if (token == DIRECTIVE || token == DOCTYPE) {
                if (self->handle_special) {
                    PyObject* res;
                    res = PyObject_CallFunction(self->handle_special,
                                                "s#", b, e-b);
                    if (!res)
                        return -1;
                    Py_DECREF(res);
                }
            } else if (token == PI) {
                if (self->handle_special) {
                    PyObject* res;
                    int len = t-b;
                    while (ISSPACE(*t))
                        t++;
                    res = PyObject_CallFunction(self->handle_proc,
                                                "s#s#", b, len, t, e-t);
                    if (!res)
                        return -1;
                    Py_DECREF(res);
                }
            } else if (self->finish_starttag) {
                PyObject* res;
                PyObject* attr;
                int len = t-b;
                while (ISSPACE(*t))
                    t++;
                attr = attrparse(t, e-t, self->xml);
                if (!attr)
                    return -1;
                res = PyObject_CallFunction(self->finish_starttag,
                                            "s#O", b, len, attr);
                Py_DECREF(attr);
                if (!res)
                    return -1;
                Py_DECREF(res);
            }
        } else if (token == ENTITYREF && self->handle_entityref) {
            PyObject* res;
            res = PyObject_CallFunction(self->handle_entityref,
                                        "s#", b, e-b);
            if (!res)
                return -1;
            Py_DECREF(res);
        } else if (token == CHARREF && (self->handle_charref ||
                                        self->handle_data)) {
            PyObject* res;
            if (self->handle_charref)
                res = PyObject_CallFunction(self->handle_charref,
                                            "s#", b, e-b);
            else {
                /* fallback: handle charref's as data */
                /* FIXME: hexadecimal charrefs? */
                CHAR_T ch;
                CHAR_T *p;
                ch = 0;
                for (p = b; p < e; p++)
                    ch = ch*10 + *p - '0';
                if (self->saxlib)
                    res = PyObject_CallFunction(self->handle_data,
                                                "s#ii", &ch, sizeof(CHAR_T),
                                                0, sizeof(CHAR_T));
                else
                    res = PyObject_CallFunction(self->handle_data,
                                                "s#", &ch, sizeof(CHAR_T));
            }
            if (!res)
                return -1;
            Py_DECREF(res);
        } else if (token == CDATA && (self->handle_cdata ||
                                      self->handle_data)) {
            PyObject* res;
            if (self->handle_cdata) {
                if (self->saxlib)
                    res = PyObject_CallFunction(self->handle_cdata,
                                                "s#ii", b, e-b, 0, e-b);
                else
                    res = PyObject_CallFunction(self->handle_cdata,
                                                "s#", b, e-b);
            } else {
                /* fallback: handle cdata as plain data */
                if (self->saxlib)
                    res = PyObject_CallFunction(self->handle_data,
                                                "s#ii", b, e-b, 0, e-b);
                else
                    res = PyObject_CallFunction(self->handle_data,
                                                "s#", b, e-b);
            }
            if (!res)
                return -1;
            Py_DECREF(res);
        } else if (token == COMMENT && self->handle_comment) {
            PyObject* res;
            res = PyObject_CallFunction(self->handle_comment,
                                        "s#", b, e-b);
            if (!res)
                return -1;
            Py_DECREF(res);
        }
        
        q = p; /* start of token */
        s = p; /* start of span */
    }

  eol: /* end of line */
    if (q != s && self->handle_data) {
        PyObject* res;
        if (self->saxlib)
            res = PyObject_CallFunction(self->handle_data,
                                        "s#ii", s, q-s, 0, q-s);
        else
            res = PyObject_CallFunction(self->handle_data,
                                        "s#", s, q-s);
        if (!res)
            return -1;
        Py_DECREF(res);
    }

    /* returns the number of bytes consumed in this pass */
    return ((char*) q) - self->buffer;
}

static PyObject*
attrparse(const CHAR_T* p, int len, int xml)
{
    PyObject* attrs;
    PyObject* key = NULL;
    PyObject* value = NULL;
    const CHAR_T* end = p + len;
    const CHAR_T* q;

    if (xml)
        attrs = PyDict_New();
    else
        attrs = PyList_New(0);

    while (p < end) {

        /* skip leading space */
        while (p < end && ISSPACE(*p))
            p++;
        if (p >= end)
            break;

        /* get attribute name (key) */
        q = p;
        while (p < end && *p != '=' && !ISSPACE(*p))
            p++;

        key = PyString_FromStringAndSize(q, p-q);
        if (key == NULL)
            goto err;

        while (p < end && ISSPACE(*p))
            p++;

        if (p < end && *p != '=') {

            /* attribute value not specified: set value to name */
            value = key;
            Py_INCREF(value);

        } else {

            /* attribute value found */

            if (p < end)
                p++;
            while (p < end && ISSPACE(*p))
                p++;

            q = p;
            if (p < end && (*p == '"' || *p == '\'')) {
                p++;
                while (p < end && *p != *q)
                    p++;
                value = PyString_FromStringAndSize(q+1, p-q-1);
                if (p < end && *p == *q)
                    p++;
            } else {
                while (p < end && !ISSPACE(*p))
                    p++;
                value = PyString_FromStringAndSize(q, p-q);
            }

            if (value == NULL)
                goto err;

        }

        if (xml) {

            /* add to dictionary */

            /* PyString_InternInPlace(&key); */
            if (PyDict_SetItem(attrs, key, value) < 0)
                goto err;
            Py_DECREF(key);
            Py_DECREF(value);

        } else {

            /* add to list */

            PyObject* res;
            res = PyTuple_New(2);
            PyTuple_SET_ITEM(res, 0, key);
            PyTuple_SET_ITEM(res, 0, value);
            if (PyList_Append(attrs, res) < 0) {
                Py_DECREF(res);
                goto err;
            }
            Py_DECREF(res);

        }

        key = NULL;
        value = NULL;
        
    }

    return attrs;

  err:
    Py_XDECREF(key);
    Py_XDECREF(value);
    Py_DECREF(attrs);
    return NULL;
}
