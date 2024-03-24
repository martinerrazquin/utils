import unittest
from utils.collections import ListDictBuilder

class TestListDictBuilder(unittest.TestCase):
    def test_build_complete_keys_passed(self):
        c1 = [1,2,3,4]
        c2 = ['a','b','c','d']
        c3 = [True, False, True, False]
        keys = ['X',5,('a','b')]
        
        expected = {k:c for k,c in zip(keys,(c1,c2,c3))}

        x = ListDictBuilder(keys)
        for x1,x2,x3 in zip(c1,c2,c3):
            item = {k:x for k,x in zip(keys, (x1,x2,x3))}
            x.append(item)
        result = x.export()
        self.assertDictEqual(expected, result)

    def test_build_complete_keys_inferred(self):
        c1 = [1,2,3,4]
        c2 = ['a','b','c','d']
        c3 = [True, False, True, False]
        keys = ['X',5,('a','b')]
        
        expected = {k:c for k,c in zip(keys,(c1,c2,c3))}

        x = ListDictBuilder()
        for x1,x2,x3 in zip(c1,c2,c3):
            item = {k:x for k,x in zip(keys, (x1,x2,x3))}
            x.append(item)
        result = x.export()
        self.assertDictEqual(expected, result)

    def test_mismatch_raises_when_enabled_extra(self):
        x = ListDictBuilder({'X','Y'}, raise_mismatch=True)
        with self.assertRaises(KeyError) as s:
            x.append({'X':1,'Y':2,'Z':4})
    
    def test_mismatch_raises_when_enabled_missing(self):
        x = ListDictBuilder({'X','Y'}, raise_mismatch=True)
        with self.assertRaises(KeyError) as s:
            x.append({'X':1})

    def test_mismatch_raises_when_disabled_missing(self):
        x = ListDictBuilder({'X','Y'}, raise_mismatch=False)
        with self.assertRaises(KeyError) as s:
            x.append({'X':1}) 
    
    def test_mismatch_no_raise_when_disabled_extra(self):
        x = ListDictBuilder({'X','Y'}, raise_mismatch=False)
        try:
            x.append({'X':1,'Y':2,'Z':4})
        except KeyError:
            self.fail("KeyError was wrongfully raised.")
