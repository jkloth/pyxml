from xml.dom import INDEX_SIZE_ERR, DOMSTRING_SIZE_ERR , HIERARCHY_REQUEST_ERR
from xml.dom import WRONG_DOCUMENT_ERR, INVALID_CHARACTER_ERR, NO_DATA_ALLOWED_ERR
from xml.dom import NO_MODIFICATION_ALLOWED_ERR, NOT_FOUND_ERR, NOT_SUPPORTED_ERR
from xml.dom import INUSE_ATTRIBUTE_ERR, INVALID_STATE_ERR, SYNTAX_ERR
from xml.dom import INVALID_MODIFICATION_ERR, NAMESPACE_ERR, INVALID_ACCESS_ERR

g_errorMessages = {
    INDEX_SIZE_ERR: "DOM Error Code %i: Index error accessing NodeList or NamedNodeMap",
    DOMSTRING_SIZE_ERR: "DOM Error Code %i: DOMString exceeds maximum size.",
    HIERARCHY_REQUEST_ERR: "DOM Error Code %i: Node manipulation results in invalid parent/child relationship.",
    WRONG_DOCUMENT_ERR: "DOM Error Code %i: ",
    INVALID_CHARACTER_ERR: "DOM Error Code %i: ",
    NO_DATA_ALLOWED_ERR: "DOM Error Code %i: ",
    NO_MODIFICATION_ALLOWED_ERR: "DOM Error Code %i: Attempt to modify a read-only attribute.",
    NOT_FOUND_ERR: "DOM Error Code %i: ",
    NOT_SUPPORTED_ERR: "DOM Error Code %i: DOM feature not supported.",
    INUSE_ATTRIBUTE_ERR: "DOM Error Code %i: Illegal operation on an attribute while in use by an element.",
    INVALID_STATE_ERR: "DOM Error Code %i: ",
    SYNTAX_ERR: "DOM Error Code %i: ",
    INVALID_MODIFICATION_ERR: "DOM Error Code %i: ",
    NAMESPACE_ERR: "DOM Error Code %i: Namespace operation results in malformed or invalid name or name declaration.",
    INVALID_ACCESS_ERR: "DOM Error Code %i: ",
    }

