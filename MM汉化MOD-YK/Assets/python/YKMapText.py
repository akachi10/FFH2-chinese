# YKMapText.py - YK Chinese package: map-script option text shim
# Looks up returned English UI strings as text-db keys; falls back to English.
from CvPythonExtensions import CyTranslator

def t(s):
	try:
		k = str(s)
	except:
		return s
	if not k:
		return s
	r = CyTranslator().getText(k, ())
	if r == k:
		k2 = k.strip()
		if k2 and k2 != k:
			r2 = CyTranslator().getText(k2, ())
			if r2 != k2:
				return unicode(r2)
	return unicode(r)

def wrap(fn):
	def _f(argsList):
		return t(fn(argsList))
	return _f
