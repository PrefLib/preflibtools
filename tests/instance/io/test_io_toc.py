from unittest import TestCase

from preflibtools.instances import OrdinalInstance


class TestAnalysis(TestCase):
    def test_read_old(self):
        old_toc_str = """12
            1,Cathal Boland F.G. 
            2,Clare Daly S.P. 
            3,Mick Davis S.F. 
            4,Jim Glennon F.F. 
            5,Ciaran Goulding Non-P 
            6,Michael Kennedy F.F. 
            7,Nora Owen F.G. 
            8,Eamonn Quinn Non-P 
            9,Sean Ryan Lab 
            10,Trevor Sargent G.P. 
            11,David Henry Walshe C.C. Csp 
            12,G.V. Wright F.F. 
            43942,43942,19297
            800,{12,6},4,{1,2,3,5,7,8,9,10,11}
            680,4,6,12,{1,2,3,5,7,8,9,10,11}
            506,6,12,4,{1,2,3,5,7,8,9,10,11}
            486,12,4,6,{1,2,3,5,7,8,9,10,11}
            429,6,4,12,{1,2,3,5,7,8,9,10,11}
            367,4,12,6,{1,2,3,5,7,8,9,10,11}
            343,10,{1,2,3,4,5,6,7,8,9,11,12}
            278,2,{1,3,4,5,6,7,8,9,10,11,12}
            251,9,{1,2,3,4,5,6,7,8,10,11,12}
            194,9,10,2,{1,3,4,5,6,7,8,11,12}
            177,4,{1,2,3,5,6,7,8,9,10,11,12}
            172,2,9,10,{1,3,4,5,6,7,8,11,12}"""
        instance = OrdinalInstance()
        instance.parse_old(old_toc_str.split("\n"))
        assert instance.orders[0] == ((12, 6), (4,), (1, 2, 3, 5, 7, 8, 9, 10, 11))
        assert instance.orders[6] == ((10,), (1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12))
