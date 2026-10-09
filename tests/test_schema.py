import unittest,copy
from support import load
from core import validate

class SchemaTests(unittest.TestCase):
    def test_repository_metadata_valid(self):self.assertEqual(validate(load()),[])
    def test_missing_field_rejected(self):
        db=load();del db['clips'][0]['publish_approved'];self.assertTrue(validate(db))
    def test_unknown_classification_rejected(self):
        db=load();db['clips'][0]['claim_class']='converted';self.assertTrue(validate(db))
    def test_string_boolean_rejected(self):
        db=load();db['approvals']['publication_approved']='true';self.assertTrue(validate(db))
    def test_duplicate_identifiers_rejected(self):
        db=load();db['clips'].append(copy.deepcopy(db['clips'][0]));self.assertTrue(validate(db))
    def test_negative_timecode_rejected(self):
        db=load();db['clips'][0].update(source_in_ms=-1,source_out_ms=20);self.assertTrue(validate(db))
