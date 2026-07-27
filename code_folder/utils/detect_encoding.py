import chardet

def detect_encoding(filepath):
    """returns the encoding of the given file"""
    with open(filepath, 'rb') as file:
        detector = chardet.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']