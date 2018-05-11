import sys, yaml
import re
from os.path import exists

import logging
logger = logging.getLogger('off365.util')
#logger.setLevel(logging.DEBUG)

def f(format_string):
    context = {}
    calling_frame = sys._getframe().f_back
    context.update(calling_frame.f_globals)
    context.update(calling_frame.f_locals)
    if 'self' in calling_frame.f_locals:
        context.update(vars(calling_frame.f_locals['self']))
    return format_string.format(**context)

def get_input_docs(attr, keyName=None, key=None, is_key=lambda x: False, is_collection=lambda k,v: len(v) > 1):
    """
    read input documents
    """
    docs = []

    if key is None:
        #assert len(attr), "What do you want to post? use '-' for reading from stdin"

        if len(attr) and "-" == attr[0]:
            attr = attr[1:]
            key = "-"

    logger.debug("key: %s", key)
    logger.debug("attr: %s", attr)

    def load_from_file(f=sys.stdin):
        for doc in yaml.load_all(f):
            if isinstance(doc, list):
                for d in doc:
                    docs.append(d)
            else:
                # have dictionary
                (k,val) = doc.items()[0]

                if isinstance(val, dict) and is_key(k):
                    # there are multiple documents with dn as keys
                    for k,v in doc.items():
                        if keyName is not None:
                            if keyName not in v:
                                v[keyName] = k

                        docs.append(v)
                else:
                    # doc itself is the entry
                    docs.append(doc)

    if key == "-":
        load_from_file()

    else:
        entry = {}
        if keyName is not None:
            entry[keyName] = key

        ATTR = re.compile(r'^(\$?[\w-]+)[:+]?=(.*)')
        for a in attr:
            logger.debug("handle argument: %s", a)

            if exists(a):
                logger.debug("is file: %s", a)

                if len(entry):
                    docs.append(entry)
                    entry = {}

                with open(a, 'r') as f:
                    load_from_file(f)
                continue

            m = ATTR.match(a)
            if m:
                (name, value) = m.groups()
                if name not in entry:
                    entry[name] = []
                if not isinstance(value, basestring):
                    value = unicode(value)
                entry[name].append(value)

        for k,v in entry.items():
            if not is_collection(k,v):
                entry[k] = v[0]

        if len(entry):
            docs.append(entry)

    logger.debug("docs: %s", docs)
    if not len(docs):
        docs = [{}]

    return docs
