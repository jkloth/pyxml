/*
 Boolean extension, by Uche Ogbuji
 Copyright (c) 2001 Fourthought, Inc. USA.   All Rights Reserved.
 See  http://4suite.org/COPYRIGHT  for license and copyright information
*/

#include "boolean.h"
#include <string.h>
#include <ctype.h>
#include <stdio.h>


PyBooleanObject *boolean_NEW(int initval);
static PyObject *ErrorObject = NULL;

static PyMethodDef booleanMethods[] = {
     { "BooleanValue", BooleanValue, 1 },
     { "IsBooleanType", IsBooleanType, 1 },
     { NULL, NULL }
};


static PyObject *BooleanValue(PyObject *self, PyObject *args) {
  PyObject *obj, *tmp;
  PyBooleanObject *result = NULL;

  if (!PyArg_ParseTuple(args, "O", &obj)) 
    return NULL;

  if (Boolean_Check(obj)){
    result = (PyBooleanObject *)obj;
  } else if (PyNumber_Check(obj)){
    tmp = PyNumber_Int(obj);
    result = PyInt_AS_LONG(tmp) ? g_true : g_false;
  } else if (PyString_Check(obj)){
    result = (strlen(PyString_AS_STRING(obj))) ? g_true : g_false;
  } else {
    result = g_false;
  }
  Py_INCREF(result);
  return (PyObject *)result;
}

static int pyobj_as_boolean_int(PyObject *obj) {
  if (Boolean_Check(obj)){
    return Boolean_Value((PyBooleanObject *)obj);
  } else if (PyNumber_Check(obj)){
    return PyInt_AS_LONG(PyNumber_Int(obj)) ? 1 : 0;
  } else if (PyString_Check(obj)){
    return (strlen(PyString_AS_STRING(obj))) ? 1 : 0;
  } else {
    return 0;
  }
}

static PyObject *IsBooleanType(PyObject *self, PyObject *args) {
  PyObject *obj;
  PyObject *result = NULL;

  if (!PyArg_ParseTuple(args, "O", &obj))
    return NULL;

  if (Boolean_Check(obj))
    result = PyInt_FromLong((long)1);
  else
    result = PyInt_FromLong((long)0);
  Py_INCREF(result);
  return result;
}

PyBooleanObject *boolean_NEW(int initval)
{
  PyBooleanObject *object = (PyBooleanObject *)malloc(sizeof(PyBooleanObject));

  if (object == NULL)
    /*FIXME: figure out low memory exception procedure*/
    return (PyBooleanObject *)PyErr_NoMemory();

  object->ob_type = &PyBoolean_Type;
  object->value = initval;
  return object;
}

void boolean_dealloc(PyObject *self)
{
  PyMem_DEL(self);
}

int boolean_cmp(PyObject *o1, PyObject *o2){
  int result = -1;
/*   int *res = (int *)malloc(sizeof(int)); */
  PyBooleanObject *b1;
  PyBooleanObject *b2;

  if (Boolean_Check(o1) && Boolean_Check(o2)) {
    b1 = (PyBooleanObject *)o1;
    b2 = (PyBooleanObject *)o2;
    result = !(Boolean_Value(o1) == Boolean_Value(o2));
  } else if (Boolean_Check(o1)) {
    b1 = (PyBooleanObject *)o1;
    result = !(Boolean_Value(o1) == pyobj_as_boolean_int(o2));
  } else if (Boolean_Check(o2)) {
    b2 = (PyBooleanObject *)o2;
    result = !(Boolean_Value(o2) == pyobj_as_boolean_int(o1));
  }
  return result;
}

static PyObject *boolean_str(PyObject *self)
{
  PyObject *result = NULL;
  PyBooleanObject *obj = (PyBooleanObject *)self;

  if (Boolean_Value(obj)){
    result = PyString_FromString("true");
  } else {
    result = PyString_FromString("false");
  }
  Py_INCREF(result);
  return result;
}

static int boolean_print(PyObject *self, FILE *fp, int flags)
{
  char buf[256];
  PyBooleanObject *obj = (PyBooleanObject *)self;

  /*Yeah, wasteful, but I hevan't yet decided whether to add to the output*/
  sprintf(buf, "%s", Boolean_Value(obj) ? "true" : "false");
  fputs(buf, fp);
  return 0;
}

static int boolean_coerce(PyObject **v, PyObject **w){
  PyObject *newv, *neww;

  if ((*v)->ob_type == (*w)->ob_type){
    Py_INCREF(*v);
    Py_INCREF(*w);
    return 0;
  }
  newv = PyNumber_Int(*v);
  neww = PyNumber_Int(*w);
  if (newv && neww){
    Py_INCREF(newv);
    Py_INCREF(neww);
    *v = newv;
    *w = neww;
    return 0;
  }
  return -1;  /* couldn't do it */
}

static PyObject *boolean_and(PyObject *o1, PyObject *o2){
  /* FIXME: Check whether we need to conver the 1st arg.  The Python/C docs don't help */
  int lhs = pyobj_as_boolean_int(o1), rhs = pyobj_as_boolean_int(o2);
  PyObject *result = NULL;

  result = PyInt_FromLong((long)(lhs && rhs));
  Py_INCREF(result);
  return result;
}

static PyObject *boolean_or(PyObject *o1, PyObject *o2){
  /* FIXME: Check whether we need to conver the 1st arg.  The Python/C docs don't help */
  int lhs = pyobj_as_boolean_int(o1), rhs = pyobj_as_boolean_int(o2);
  PyObject *result = NULL;

  result = PyInt_FromLong((long)(lhs || rhs));
  Py_INCREF(result);
  return result;
}

static PyObject *boolean_xor(PyObject *o1, PyObject *o2){
  /* FIXME: Check whether we need to conver the 1st arg.  The Python/C docs don't help */
  int lhs = pyobj_as_boolean_int(o1), rhs = pyobj_as_boolean_int(o2);
  PyObject *result = NULL;

  result = PyInt_FromLong((long)(lhs ^ rhs));
  Py_INCREF(result);
  return result;
}

static int boolean_nonzero(PyObject *o){
  PyBooleanObject *obj = (PyBooleanObject *)o;

  return Boolean_Value(obj);
}

static PyObject *boolean_int(PyObject *o){
  PyBooleanObject *obj = (PyBooleanObject *)o;
  PyObject *result = NULL;

  result = PyInt_FromLong((long)Boolean_Value(obj));
  Py_INCREF(result);
  return result;
}

static PyObject *boolean_long(PyObject *o){
  PyBooleanObject *obj = (PyBooleanObject *)o;
  PyObject *result = NULL;

  result = PyLong_FromLong((long)Boolean_Value(obj));
  Py_INCREF(result);
  return result;
}

static PyObject *boolean_float(PyObject *o){
  PyBooleanObject *obj = (PyBooleanObject *)o;
  PyObject *result = NULL;

  result = PyFloat_FromDouble((double)Boolean_Value(obj));
  Py_INCREF(result);
  return result;
}

void initboolean(void) {
  PyObject *m, *d;

  m = Py_InitModule("boolean", booleanMethods);
  d = PyModule_GetDict(m);

  PyBoolean_Type.ob_type = &PyType_Type;
  PyDict_SetItemString(d, "BooleanType", (PyObject *)&PyBoolean_Type);

  ErrorObject = PyString_FromString("boolean.error");
  PyDict_SetItemString(d, "error", ErrorObject);

  g_true = (PyBooleanObject *)boolean_NEW(1);
  Py_INCREF(g_true);

  g_false = (PyBooleanObject *)boolean_NEW(0);
  Py_INCREF(g_false);

  PyDict_SetItemString(d, "true", (PyObject *)g_true);
  PyDict_SetItemString(d, "false", (PyObject *)g_false);

  return;
}

static PyNumberMethods boolean_as_number = {
  0,       /* binaryfunc nb_add;          __add__ */
  0,       /* binaryfunc nb_subtract;     __sub__ */
  0,       /* binaryfunc nb_multiply;     __mul__ */
  0,       /* binaryfunc nb_divide;       __div__ */
  0,       /* binaryfunc nb_remainder;    __mod__ */
  0,    /* binaryfunc nb_divmod;       __divmod__ */
  0,       /* ternaryfunc nb_power;       __pow__ */
  0,       /* unaryfunc nb_negative;      __neg__ */
  0,       /* unaryfunc nb_positive;      __pos__ */
  0,       /* unaryfunc nb_absolute;      __abs__ */
  boolean_nonzero,   /* inquiry nb_nonzero;         __nonzero__ */
  0,    /* unaryfunc nb_invert;        __invert__ */
  0,    /* binaryfunc nb_lshift;       __lshift__ */
  0,    /* binaryfunc nb_rshift;       __rshift__ */
  boolean_and,       /* binaryfunc nb_and;         __and__ */
  boolean_xor,       /* binaryfunc nb_xor;         __xor__ */
  boolean_or,        /* binaryfunc nb_or;          __or__ */
  boolean_coerce,    /* coercion nb_coerce;         __coerce__ */
  boolean_int,       /* unaryfunc nb_int;           __int__ */
  boolean_long,      /* unaryfunc nb_long;          __long__ */
  boolean_float,     /* unaryfunc nb_float;          __float__ */
  0,       /* unaryfunc nb_oct;           __oct__ */
  0,       /* unaryfunc nb_hex;           __hex__ */
};

static PyTypeObject PyBoolean_Type = {
    PyObject_HEAD_INIT(0)
    0,
    "boolean",
    sizeof(PyBooleanObject),
    0,
    0,    /*tp_dealloc*/
    boolean_print,   /*tp_print*/
    0,   /*tp_getattr*/
    0,              /*tp_setattr*/
    (cmpfunc)boolean_cmp,                          /*tp_compare*/
    0,          /*tp_repr*/
    &boolean_as_number,                          /*tp_as_number*/
    0,              /*tp_as_sequence*/
    0,              /*tp_as_mapping*/
    0,                             /*tp_hash*/
    0,          /*tp_call*/
    boolean_str,          /*tp_str*/
    0,                      /*tp_getattro*/
    0,          /*tp_setattro*/
};


#if (0)

static PyNumberMethods boolean_as_number = {
  boolean_add,       /* binaryfunc nb_add;         __add__ */
  boolean_sub,       /* binaryfunc nb_subtract;    __sub__ */
  boolean_mul,       /* binaryfunc nb_multiply;    __mul__ */
  boolean_div,       /* binaryfunc nb_divide;      __div__ */
  boolean_mod,       /* binaryfunc nb_remainder;   __mod__ */
  boolean_divmod,    /* binaryfunc nb_divmod;      __divmod__ */
  boolean_pow,       /* ternaryfunc nb_power;      __pow__ */
  boolean_neg,       /* unaryfunc nb_negative;     __neg__ */
  boolean_pos,       /* unaryfunc nb_positive;     __pos__ */
  boolean_abs,       /* unaryfunc nb_absolute;     __abs__ */
  boolean_nonzero,   /* inquiry nb_nonzero;        __nonzero__ */
  boolean_invert,    /* unaryfunc nb_invert;       __invert__ */
  boolean_lshift,    /* binaryfunc nb_lshift;      __lshift__ */
  boolean_rshift,    /* binaryfunc nb_rshift;      __rshift__ */
  boolean_and,       /* binaryfunc nb_and;         __and__ */
  boolean_xor,       /* binaryfunc nb_xor;         __xor__ */
  boolean_or,        /* binaryfunc nb_or;          __or__ */
  boolean_coerce,    /* coercion nb_coerce;        __coerce__ */
  boolean_int,       /* unaryfunc nb_int;          __int__ */
  boolean_long,      /* unaryfunc nb_long;         __long__ */
  boolean_float,     /* unaryfunc nb_float;        __float__ */
  boolean_oct,       /* unaryfunc nb_oct;          __oct__ */
  boolean_hex,       /* unaryfunc nb_hex;          __hex__ */
};

#endif
