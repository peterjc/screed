import DBConstants

FieldTypes = (('name', DBConstants._INDEXED_TEXT_KEY),
              ('description', DBConstants._STANDARD_TEXT),
              ('sequence', DBConstants._SLICEABLE_TEXT))

def fasta_iter(handle):
    """
    Iterator over the given FASTA file handle, returning records. handle
    is a handle to a file opened for reading
    """
    data = {}

    line = handle.readline()
    while line:
        line = line.strip()
        if not line.startswith('>'):
            raise IOError("Bad FASTA format: no '>' at beginning of line")

        # Try to grab the name and optional description
        try:
            data['name'], data['description'] = line[1:].split(' ', 1)
        except ValueError: # No optional description
            data['name'] = line[1:]
            data['description'] = ''
            pass

        data['name'] = data['name'].strip()
        data['description'] = data['description'].strip()

        # Collect sequence lines into a list
        sequenceList = []
        line = handle.readline()
        while line and not line.startswith('>'):
            sequenceList.append(line.strip())
            line = handle.readline()

        data['sequence'] = ''.join(sequenceList)
        yield data
