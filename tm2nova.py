#!/usr/bin/env python3

import json
import os
import plistlib
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom

# TODO: this is lazy and incomplete; just a few to get started.
conversions = {
    "storage.modifier": "keyword",
    "constant.numeric": "value.number",
    "constant.language.boolean": "value.boolean",
    "support.function": "identifier.core.function",
    "entity.name": "identifier",
}


def element(parent, element_name, text=None, **attrs):
    e = ET.SubElement(parent, element_name, **attrs)
    if text:
        e.text = text
    return e


def fix(regex):
    return regex.replace("#", "\\#")


def convert(name):
    for old, new in conversions.items():
        name = name.replace(old, new)
    return name


def make_scope(root, info):
    if "include" in info:
        element(root, "include", syntax="self", collection=info["include"][1:])
    elif "patterns" in info and len(info) == 1:
        for p in info["patterns"]:
            make_scope(root, p)
    else:
        name = convert(info.get("name", "unnamed"))
        scope = element(root, "scope", name=name)
        if "match" in info:
            element(scope, "expression", fix(info["match"]))
            for key in ("captures", "beginCaptures"):
                if key in info:
                    for num, capinfo in info[key].items():
                        # Sometimes there's "patterns" here instead??
                        if "name" in capinfo:
                            element(scope, "capture", number=num, name=capinfo["name"])
        elif "begin" in info:
            sw = element(scope, "starts-with")
            element(sw, "expression", fix(info["begin"]))
            for key in ("captures", "beginCaptures"):
                if key in info:
                    for num, capinfo in info[key].items():
                        # Sometimes there's "patterns" here instead??
                        if "name" in capinfo:
                            element(sw, "capture", number=num, name=capinfo["name"])
            ew = element(scope, "ends-with")
            element(ew, "expression", fix(info["end"]))
            if "patterns" in info:
                ss = element(scope, "subscopes")
                for p in info["patterns"]:
                    if "include" in p:
                        make_scope(ss, p)


if __name__ == "__main__":
    filename = sys.argv[1]
    if filename.endswith("json"):
        spec = json.load(open(filename, "r"))
    else:
        spec = plistlib.load(open(filename, "rb"))

    lang = os.path.splitext(os.path.basename(filename))[0]
    root = ET.Element("syntax", name=lang)
    meta = element(root, "meta")
    element(meta, "name", lang)

    collections = element(root, "collections")
    for name, info in spec["repository"].items():
        collection = element(collections, "collection", name=name)
        make_scope(collection, info)

    scopes = element(root, "scopes")
    for idx, pat in enumerate(spec["patterns"]):
        make_scope(scopes, pat)

    # This is bad and I feel bad. ET should have built-in pretty printing.
    print(minidom.parseString(ET.tostring(root)).toprettyxml())
