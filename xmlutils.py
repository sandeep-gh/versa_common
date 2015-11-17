import xml.etree.ElementTree as ET
import xml.etree

#element is xml tree node
#keys are elements that are queried
#value is string literal

def check_if_xml_tree(data):
    if isinstance(data, xml.etree.ElementTree.Element):
        return True
    return False

def read_string(xml_str):
    return ET.fromstring(xml_str)

def read_file(xml_fn):
    xmldoc = ET.parse(xml_fn)
    return xmldoc

def tostring(root):
    return ET.dump(root)

def get_attr_list(root):
    #<root attr1='', attr2=''></root>
    return root.keys()


def get_value(root):
    if root is None:
        return None

    try:
     val = root.text.strip()
     return val
    except:
        return root.text

def get_elems(root, attrname, path_prefix=".//", uniq=False):
    all_attr_elems=root.findall(path_prefix+attrname)
    
    if len(all_attr_elems) == 0:
        return None
    if uniq:
        assert(len(all_attr_elems) == 1)
        return all_attr_elems[0]
    return all_attr_elems

def get_value_elems(root, attrname):
    values=[]
    for elem in get_elems(root, attrname):
        values.append(get_value(elem))
    return values

def get_value_elem(root, attrname, path_prefix='.//'):
    elem=get_elems(root, attrname, path_prefix=path_prefix, uniq=True)
    return get_value(elem)

                      

#<attr>value<attr9>
def get_value_by_attr(root, attrname):
    elem=get_elems(root, attrname, uniq=True)
    if elem is None:
        return None
    return elem.text.strip()
    


#<elemn><key>value</key></elemn>
def get_elem_by_key_value(xmldoc, elemn, key,value, uniq=False):
    all_elems = xmldoc.findall('.//'+elemn+'[' + key+ '=\'' +value+'\']') 
    if uniq:
        assert(len(all_elems) == 1)
        return all_elems[0]
    return all_elems

def get_uniq_elem_by_key_value(xmldoc, elemn, key,value):
    return get_elem_by_key_value(xmldoc, elemn, key,value, uniq=True)

def get_elems_by_parent_child(root, parent, child):
    #get all roots that are of type <parent><child></child></parent>
    return root.findall(".//"+parent+"/"+child)


#Give that element whose parent=parent and has one child element as <key>value</key>
def get_elems_by_parent_child_key_value(root,parent, child, key, value, uniq=False):
    #<parent>
    #  <child>
    #    <key>value</key>
    #  </child>
    #</parent>
    xpath_str=".//"+parent+"/"+child+"["+key+"=\'"+value+"\']"
    childnodes=root.findall(xpath_str)
    if uniq:
        if(len(childnodes) == 0):
            print xpath_str
            assert(0)
        assert(len(childnodes) == 1)
        return childnodes[0]
    return childnodes

def gen_node(node_label, node_text):
    '''
    create a new node
    '''
    node = ET.Element(node_label)
    node.text = node_text
    return node



class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element is not None:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    '''
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    '''
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if len(element):
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself 
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a 
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})
