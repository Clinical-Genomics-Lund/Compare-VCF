#!/usr/bin/env python

import vcfpy
import argparse
import gzip

print('Hello world!')


parser = argparse.ArgumentParser(description='Basic utility to remove redundant INFO field entries')
parser.add_argument('-i', '--input', help='Input VCF file', required=True)
parser.add_argument('-o', '--output', help='Output VCF file', required=True)
args = parser.parse_args()

print(args.input)

reader = vcfpy.Reader.from_path(args.input)
writer = vcfpy.Writer.from_path(args.output, reader.header)

for record in reader:
    writer.write_record(record)

#example = next(reader)
#info_dict = example.INFO
#print(keys(example))

#for record in reader:
#    print(record)
