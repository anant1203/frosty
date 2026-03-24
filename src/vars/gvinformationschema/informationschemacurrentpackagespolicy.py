from .informationschema import InformationSchema

class CurrentPackagesPolicyColumnList:
    _view=InformationSchema._current_packages_policy_view
    _policy_name="POLICY_NAME"
    _allowlist="ALLOWLIST"
    _comment="COMMENT"

class InformationSchemaCurrentPackagesPolicy:
    def __init__(self):
        self.columns=CurrentPackagesPolicyColumnList()
