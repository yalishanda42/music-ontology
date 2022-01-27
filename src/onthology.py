"""A music onthology."""

import owlready2 as owl

onto =  owl.get_ontology("https://allexks.github.com/music-onthology/onto.owl")

with onto:
    class Test(owl.Thing):
        def test(self): print("test")

test = Test("testy")

test.test()