class trs_base_object(object):
    def __init__(self):
        pass


class pdf_file(trs_base_object):
    def __init__(self, pdf_path):
        super().__init__()
        self.doc = None
        self.path = pdf_path

    def set_document(self, doc):
        self.doc = doc

    def get_document(self):
        return self.doc



class pdf_page(trs_base_object):
    def __init__(self):
        super().__init__()
