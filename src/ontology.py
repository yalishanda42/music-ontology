"""A music onthology."""

import owlready2 as owl

onto =  owl.get_ontology("file://ontology.owl")

with onto:
    # class Song(owl.Thing):
    #     pass

    class Track(owl.Thing):
        pass

    class Artist(owl.Thing):
        pass

    class Album(owl.Thing):
        pass

    class LP(owl.Thing):
        pass

    class EP(Album):
        pass

    class Single(Album):
        pass

    class Genre(owl.Thing):
        pass

    class Playlist(owl.Thing):
        pass

onto.save()