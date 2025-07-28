#!/usr/bin/env python3
"""
SSML (Speech Synthesis Markup Language) is a subset of XML specifically
designed for controlling synthesis. You can see examples of how the SSML
should be parsed in the unit tests below.
"""

#
 # Conventional auto-complete and Intellisense are allowed.
#
# DO NOT USE ANY PRE-EXISTING XML PARSERS FOR THIS TASK - lxml, ElementTree, etc.
# You may use online references to understand the SSML specification, but DO NOT read
# online references for implementing an XML/SSML parser.
#


from dataclasses import dataclass
from typing import List, Union, Dict

SSMLNode = Union["SSMLText", "SSMLTag"]


@dataclass
class SSMLTag:
    name: str
    attributes: dict[str, str]
    children: list[SSMLNode]

    def __init__(
        self, name: str, attributes: Dict[str, str] = {}, children: List[SSMLNode] = []
    ):
        self.name = name
        self.attributes = attributes
        self.children = children


@dataclass
class SSMLText:
    text: str

    def __init__(self, text: str):
        self.text = text

def parseSSML(ssml: str) -> SSMLNode:
    i = 0
    n = len(ssml)
    head_tag =''

    def skip_whitespace():
        nonlocal i
        while i < n and ssml[i].isspace():
            i += 1
        if i==n:
            raise

    def parse_text(start_tag:str) -> SSMLText:
        nonlocal i
        start = i
        while i < n and ssml[i] != '<':
            i += 1
        if i==n:
            raise
        text = unescapeXMLChars(ssml[start:i])
        return SSMLText(text)

    def _check_end_tag(start_tag:str):
        nonlocal i
        i+=2 #skip </
        end_tag = ''
        while i<n and ssml[i] != '>':
            end_tag+=ssml[i]
            i+=1
        if start_tag!=end_tag:
            raise

    def parse_tag() -> SSMLTag:
        nonlocal i
        nonlocal head_tag
        assert ssml[i] == '<'
        i += 1
        skip_whitespace()

        # Read tag name
        tag_name = ""
        while i < n and ssml[i].isalnum():
            tag_name += ssml[i]
            i += 1
        if i==n:
            raise
        
        if head_tag=='':
            if tag_name!='speak':
                raise
            head_tag=tag_name

        skip_whitespace()

        # Read attributes
        attributes = {}
        while i < n and ssml[i] not in ['/', '>']:
            skip_whitespace()
            attr_name = ""
            while i < n and ssml[i] not in ['=', '>', '/'] and not ssml[i].isspace():
                attr_name += ssml[i]
                i += 1

            skip_whitespace()
            if attr_name=="":
                raise
            if i < n and ssml[i] == '=':
                i += 1  # Skip '='
                skip_whitespace()

                quote = ssml[i]
                if quote!='"':
                    raise
                i += 1  # Skip opening quote
                attr_val = ""
                while i < n and ssml[i] != quote:
                    attr_val += ssml[i]
                    i += 1
                if i==n:
                    raise
                i += 1  # Skip closing quote
                attributes[attr_name] = attr_val
            elif ssml[i]!='=':
                raise
        # Self-closing tag
        if i==n:
            raise
        if ssml[i] == '/':
            i += 2  # skip '/>'
            return SSMLTag(tag_name, attributes, [])
        skip_whitespace()
        if ssml[i]!='>':
            raise
        i += 1  # Skip '>'
        children = []
        while True:
            if ssml[i:i+2] == "</":
                j = i + 2
                while j < n and ssml[j].isspace():
                    j += 1
                end_tag_name = ""
                while j < n and ssml[j].isalnum():
                    end_tag_name += ssml[j]
                    j += 1
                while j < n and ssml[j].isspace():
                    j += 1
                if j < n and ssml[j] == '>' :
                    if end_tag_name == tag_name:
                        i = j + 1  # Move past the closing tag
                        if end_tag_name=='speak' and i<n:
                            raise
                        break
                    else:
                        raise
            if ssml[i] == '<':
                children.append(parse_tag())
            else:
                children.append(parse_text(tag_name))

        return SSMLTag(tag_name, attributes, children)

    skip_whitespace()

    if ssml[i] == '<':
        return parse_tag()
    else:
        raise


def ssmlNodeToText(node: SSMLNode) -> str:
    if isinstance(node, SSMLText):
        return escapeXMLChars(node.text)
    elif isinstance(node, SSMLTag):
        attrs = ' '.join(f'{k}="{v}"' for k, v in node.attributes.items())
        opening = f"<{node.name}" + (f" {attrs}" if attrs else "") + ">"
        children = ''.join(ssmlNodeToText(child) for child in node.children)
        closing = f"</{node.name}>"
        return opening + children + closing
    return ''

def unescapeXMLChars(text: str) -> str:
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def escapeXMLChars(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;").replace("&", "&amp;")

# Example usage:
# ssml_string = '<speak>Hello, <break time="500ms"/>world!</speak>'
# parsed_ssml = parseSSML(ssml_string)
# text = ssmlNodeToText(parsed_ssml)
# print(text)