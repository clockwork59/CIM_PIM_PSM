"""CIM Namespace Registry — single source of truth for all RDF prefixes."""
from rdflib import Namespace

CIM       = Namespace("https://cim.medical/ontology/v3.4#")
CIM_EQUIP = Namespace("https://cim.medical/ontology/v3.4/equipment#")
CIM_SPACE = Namespace("https://cim.medical/ontology/v3.4/space#")
CIM_FLOW  = Namespace("https://cim.medical/ontology/v3.4/flow#")
CIM_CTRL  = Namespace("https://cim.medical/ontology/v3.4/control#")
CIM_C     = Namespace("https://cim.medical/ontology/v4.0/conceptual#")
CIM_MED   = Namespace("https://cim.medical/ontology/v4.0/medium#")
CIM_PT    = Namespace("https://cim.medical/ontology/v4.0/point#")
CIM_D     = Namespace("https://cim.medical/ontology/v4.0/design#")
CIM_F     = Namespace("https://cim.medical/ontology/v4.0/foundational#")
CIM_REF   = Namespace("https://cim.medical/ontology/v4.0/reference#")
CIM_O     = Namespace("https://cim.medical/ontology/v4.0/operational#")
BFO       = Namespace("http://purl.obolibrary.org/obo/BFO_")
RO        = Namespace("http://purl.obolibrary.org/obo/RO_")
FSO       = Namespace("https://w3id.org/fso#")
S223      = Namespace("http://data.ashrae.org/standard223#")
SOSA      = Namespace("http://www.w3.org/ns/sosa/")
BRICK     = Namespace("https://brickschema.org/schema/Brick#")

# Dict for rdflib initNs / graph.bind
ALL_NS = {
    "cim":       CIM,
    "cim-equip": CIM_EQUIP,
    "cim-space": CIM_SPACE,
    "cim-flow":  CIM_FLOW,
    "cim-ctrl":  CIM_CTRL,
    "cim-c":     CIM_C,
    "cim-med":   CIM_MED,
    "cim-pt":    CIM_PT,
    "cim-d":     CIM_D,
    "cim-f":     CIM_F,
    "cim-ref":   CIM_REF,
    "cim-o":     CIM_O,
    "bfo":       BFO,
    "ro":        RO,
    "fso":       FSO,
    "s223":      S223,
    "sosa":      SOSA,
    "brick":     BRICK,
}
