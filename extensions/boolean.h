#ifndef DOMLETTE_H
#define DOMLETTE_H
#ifdef __cplusplus
extern "C" {
#endif

#include "Python.h"

#if defined(_WIN32) || defined(__WIN32__)
#include <float.h>
#define NaN_Check(x) _isnan(x)
#define Inf_Check(x) (_finite(x) && !_isnan(x))
#else
#include <math.h>
#define NaN_Check(x) isnan(x)
#define Inf_Check(x) isinf(x)
#endif

extern DL_EXPORT(PyTypeObject) PyBoolean_Type;

#define Boolean_Check(v)  ((v)->ob_type == &PyBoolean_Type)
#define Boolean_Value(v)  (((PyBooleanObject *)(v))->value)

PyObject *boolean_new(PyObject *self, PyObject *args);
static PyObject *BooleanValue(PyObject *self, PyObject *args);
static PyObject *IsBooleanType(PyObject *self, PyObject *args);

typedef struct {
  PyObject_HEAD
  int value;
} PyBooleanObject;

PyBooleanObject *g_true;
PyBooleanObject *g_false;

#endif
