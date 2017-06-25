import os
import sys
import gzip

import fqutils.util as util

class Fastq:
    """
    Helper class to rapidly parse fastq/gz as raw text. 
    (Biopython's Bio.SeqIO.index() does not support gzip compression :'( )
    """

    pos = 0
    lineno = 0

    def __init__(self, filename, mode='r'):
        if 'r' in mode and not os.path.isfile(filename):
            sys.exit('%s is not a valid file path.' % filename)
        self.filename = filename
        self.mode = mode
        self.is_gzip = util.is_gzip(self.filename)
        self.handle = self.open()

    
    def __enter__(self):
        return self

    
    def __exit__(self, typee, value, traceback):
        self.close()


    def open(self):
        """
        Autodetect extension and return filehandle.
        """
        if self.is_gzip:
            self.mode = self.mode + 'b'
            return gzip.open(self.filename, mode=self.mode)
        else:
            return open(self.filename, self.mode)


    def close(self):
        self.handle.close()


    def get_read(self):
        """Get a fastq read. Returns None at EOF"""
        self.pos = self.handle.tell()
        read = []
        for i in range(4):  # assumes 4-line FASTQ
            line = self.handle.readline()
            if self.is_gzip:
                line = line.decode()
            if line == '' or line == b'':
                return None  # EOF
            read.append(line)
        self.lineno += 1
        return read


    def writelines(self, read):
        if self.is_gzip:
            read = [b.encode() for b in read]
        self.handle.writelines(read)

    
    def seek(self, position):
        """Jump to a particular file position"""
        self.handle.seek(position)
