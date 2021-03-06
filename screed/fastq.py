import DBConstants

FieldTypes = (('name', DBConstants._INDEXED_TEXT_KEY),
              ('annotations', DBConstants._STANDARD_TEXT),
              ('sequence', DBConstants._STANDARD_TEXT),
              ('accuracy', DBConstants._STANDARD_TEXT))

def fastq_iter(handle):
    """
    Iterator over the given FASTQ file handle returning records. handle
    is a handle to a file opened for reading
    """
    data = {}
    line = handle.readline().strip()
    while line:
        if not line.startswith('@'):
            raise IOError("Bad FASTQ format: no '@' at beginning of line")

        # Try to grab the name and (optional) annotations
        try:
            data['name'], data['annotations'] = line[1:].split(' ',1)
        except ValueError: # No optional annotations
            data['name'] = line[1:]
            data['annotations'] = ''
            pass

        # Extract the sequence lines
        sequence = []
        line = handle.readline().strip()
        while not line.startswith('+'):
            sequence.append(line)
            line = handle.readline().strip()

        data['sequence'] = ''.join(sequence)

        # Extract the accuracy lines
        accuracy = []
        line = handle.readline().strip()
        seqlen = len(data['sequence'])
        aclen = 0
        while not line == '' and aclen < seqlen:
            accuracy.append(line)
            aclen += len(line)
            line = handle.readline().strip()

        data['accuracy'] = ''.join(accuracy)
        if len(data['sequence']) != len(data['accuracy']):
            raise IOError('sequence and accuracy strings must be '\
                          'of equal length')

        yield data
