import enum

class RiskTypeEnum(str, enum.Enum):
    AML = "AML"
    FRAUD = "FRAUD"
    CYBERSECURITY = "CYBERSECURITY"
    GOVERNANCE = "GOVERNANCE"
    PRIVACY = "PRIVACY"
    OPERATIONAL = "OPERATIONAL"
    COMPLIANCE = "COMPLIANCE"
    OTHER = "OTHER"


class JurisdictionEnum(str, enum.Enum):
    EU = "EU"
    FINLAND = "FINLAND"
    GLOBAL = "GLOBAL"
    OTHER = "OTHER"
