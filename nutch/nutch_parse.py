from __future__ import absolute_import, division, print_function

import nutchpy
import pprint
import re


def generate_url_data( node_path, include_content = True ):
    """
    Parse the raw data fetched by nutch and generate
    the data that we need.
    """

    seq_reader = nutchpy.SequenceReader()
    data = seq_reader.read(node_path)

    for d in data:
        meta, content = d[1].split( 'Content:\n' )
        meta = d[1].split("\n")
        mime = None

        for m in meta:
            if m.startswith("contentType: "):
                # Skip the 'contentType: '
                mime = m[13:]

        if mime is None:
            print( "[Warning] No Content Type found for url: {0} ".format( d[0] ) )

        if not include_content:
            content = None

        yield {"url":d[0], 'mime': mime, 'content': content}


if __name__ == '__main__':

    # replace this with the path of your data file
    node_path = "/Users/dingshuoqing/codes/cs572/nutch/runtime/local/crawl2/merged/20150219172533/content/part-00000/data"
    pp = pprint.PrettyPrinter(indent=4)

    mime_types = {}

    for data in generate_url_data( node_path ):

        mime = data['mime']
        if mime not in mime_types:
            mime_types[mime] = []

        mime_types[mime].append( data['url'] )

        # Do something with the data
        # pp.pprint(data)

    print( mime_types.keys() )
