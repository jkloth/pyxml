#ifndef DOMLETTE_H
#define DOMLETTE_H
#ifdef __cplusplus
extern "C" {
#endif

#include "Python.h"

extern DL_EXPORT(PyTypeObject) PyBoolean_Type;

#define Boolean_Check(v)  ((v)->ob_type == &PyBoolean_Type)
#define Boolean_Value(v)  (((PyBooleanObject *)(v))->value)

typedef struct {
  PyObject_HEAD
  int value;
} PyBooleanObject;

PyObject *boolean_new(PyObject *self, PyObject *args);
static PyObject *BooleanValue(PyObject *self, PyObject *args);
static PyObject *IsBooleanType(PyObject *self, PyObject *args);

PyBooleanObject *g_true;
PyBooleanObject *g_false;

#endif
