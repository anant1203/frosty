from .informationschema import InformationSchema

class PackagesColumnList:
    _view=InformationSchema._packages_view
    _package_name="PACKAGE_NAME"
    _version="VERSION"
    _language="LANGUAGE"
    _created="CREATED"

class InformationSchemaPackages:
    def __init__(self):
        self.columns=PackagesColumnList()
