"""NS module -- XML Namespace constants

This module contains the definitions of namespaces (and sometimes other
URI's) used by a variety of XML standards.  Each class has a short
all-uppercase name, which should follow any (emerging) convention for
how that standard is commonly used.  For example, ds is almost always
used as the namespace prefixes for items in XML Signature, so DS is the
class name.   Attributes within that class, all uppercase, define symbolic
names (hopefully evocative) for "constants" used in that standard.
"""


class XMLNS:
    """XMLNS, Namespaces in XML

    XMLNS (14-Jan-1999) is a W3C Recommendation.  It is specified in
    http://www.w3.org/TR/REC-xml-names
	BASE -- the basic namespace defined by the specification
	XML -- the namespace for XML 1.0
	HTML -- the namespace for HTML4.0
    """

    BASE        = "http://www.w3.org/2000/xmlns/"
    XML         = "http://www.w3.org/XML/1998/namespace"
    HTML        = "http://www.w3.org/TR/REC-html40"


class SOAP:
    """SOAP, the Simple Object Access Protocol

    SOAP (v1.1, 8-May-2000) is a W3C note.  It is specified in
    http://www.w3.org/TR/SOAP
	ENV -- namespace for the SOAP envelope
	ENC -- namespace for the SOAP encoding in section 5
    (Note that no BASE is defined.)
    """

    ENV         = "http://schemas.xmlsoap.org/soap/envelope/"
    ENC         = "http://schemas.xmlsoap.org/soap/encoding/"


class DSIG:
    """DSIG, XML-Signature Syntax and Processing

    DSIG (19-Apr-2001) is a W3C Candidate Recommendation.  It is specified
    in http://www.w3.org/TR/xmldsig-core/
	BASE -- the basic namespace defined by the specification
	DIGEST_SHA1 -- The SHA-1 digest method
	DIGEST_MD2 -- The MD2 digest method
	DIGEST_MD5 -- The MD5 digest method
	SIG_DSA_SHA1 -- The DSA/DHA-1 signature method
	SIG_RSA_SHA1 -- The RSA/DHA-1 signature method
	HMAC_SHA1 -- The SHA-1 HMAC method
	ENC_BASE64 -- The Base64 encoding method
	ENVELOPED -- an enveloped XML signature
	C14N  -- XML canonicalization
	C14N_COMM  -- XML canonicalization, retaining comments
    """

    BASE        = "http://www.w3.org/2000/09/xmldsig#"
    DIGEST_SHA1 = BASE + "sha1"
    DIGEST_MD2  = BASE + "md2"
    DIGEST_MD5  = BASE + "md5"
    SIG_DSA_SHA1= BASE + "dsa-sha1"
    SIG_RSA_SHA1= BASE + "rsa-sha1"
    HMAC_SHA1   = BASE + "hmac-sha1"
    ENC_BASE64  = BASE + "base64"
    ENVELOPED   = BASE + "enveloped-signature"
    C14N        = "http://www.w3.org/TR/2000/CR-xml-c14n-20010315"
    C14N_COMM   = C14N + "#WithComments"


class SCHEMA:
    """SCHEMA, XML Schema

    XML Schema (30-Mar-2001) is a W3C proposed recommendation.  It is
    specified in http://www.w3.org/TR/xmlschema-1 (Structures) and
    http://www.w3.org/TR/xmlschema-2 (Datatypes). Schema has been under
    development for a comparitively long time, and other standards have
    at times used earlier drafts.  This class defines the most-used, and
    sets BASE to the latest.
	BASE -- the basic namespace (2001)
	XSD1, XSI1 -- schema and schema-instance for 1999
	XSD2, XSI2 -- schema and schema-instance for October 2000
	XSD3, XSI3 -- schema and schema-instance for 2001
	XSD_LIST -- a sequence of the XSDn values
	XSI_LIST -- a sequence of the XSIn values
    """

    XSD1        = "http://www.w3.org/1999/XMLSchema"
    XSD2        = "http://www.w3.org/2000/10/XMLSchema"
    XSD3        = "http://www.w3.org/2001/XMLSchema"
    XSD_LIST    = [ XSD1, XSD2, XSD3 ]
    XSI1        = "http://www.w3.org/1999/XMLSchema-instance"
    XSI2        = "http://www.w3.org/2000/10/XMLSchema-instance"
    XSI3        = "http://www.w3.org/2001/XMLSchema-instance"
    XSI_LIST    = [ XSI1, XSI2, XSI3 ]
    BASE        = XSD3


class XSLT:
    """XSLT, XSL Transformations

    XSLT (16-Nov-1999) is a W3C Recommendation.  It is specified in
    http://www.w3.org/TR/xslt/
	BASE -- the basic namespace defined by this specification
    """

    BASE        = "http://www.w3.org/1999/XSL/Transform"


class XPATH:
    """XPATH, XML Path Language

    XPATH (16-Nov-1999) is a W3C Recommendation.  It is specified in
    http://www.w3.org/TR/xpath.  This class is currently empty.
    """

    pass


class WSDL:
    """WSDL, Web Services Description Language

    WSDL (V1.1, 15-Mar-2001) is a W3C Note.  It is specified in
    http://www.w3.org/TR/wsdl
	BASE -- the basic namespace defined by this specification
	BIND_SOAP -- SOAP binding for WSDL
	BIND_HTTP -- HTTP GET and POST binding for WSDL
	BIND_MIME -- MIME binding for WSDL
    """

    BASE        = "http://schemas.xmlsoap.org/wsdl/"
    BIND_SOAP   = BASE + "soap/"
    BIND_HTTP   = BASE + "http/"
    BIND_MIME   = BASE + "mime/"
