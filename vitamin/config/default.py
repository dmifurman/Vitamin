from helpers.tweak import Section, LazyList

Main = Section({
    "REGISTERED_MODULES":
    LazyList(["lazy://vitamin.modules.url::RequestManager"]),
    
    "REGISTERED_INTERFACES":
    LazyList(["lazy://vitamin.interfaces::IModuleURL"]),
    
    "PRODUCTION_CHAIN":
    ["IModuleURL"]
})

Loader = Section({
    "NEXT_NODE":"lazy://vitamin.core::VtCore"
})

URL = Section({
    "ROUTES":
    {"/" : "index",
     "/user_{name}/{action[show|hide]}" : "user"}
})

Database = Section({
    "PROVIDER" : "lazy://sqlite3",
    "LOCATION" : ":memory:",
    "USER" : "root",
    "PASSWD" : "",
    "CONNECT_WITH" : ("LOCATION",),
    "DEFINITIONS" : "lazy://vitamin.modules.database.sqlbuilder.definitions::Definitions"
})

Templates = Section({
    "LOADER" : "lazy://vitamin.modules.tpl.loaders.file::FileLoader",
    "TEMPLATE_FOLDER" : ".",
    "TEMPLATE_EXTENSION" : ".html",
    "TEMPLATE_TESTS_PACKAGE" : "lazy://vitamin.modules.tpl.tests.templates"
})

