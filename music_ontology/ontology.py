"""A music onthology."""

import owlready2 as owl

class MusicOntologyProvider:
    """Provides methods for creating, loading and saving the music ontology."""

    def __init__(self, base_iri: str = "file://ontology.owl"):
        self.base_iri = base_iri

    def create(self) -> owl.Ontology:
        """Create the ontology from scratch and return it."""

        onto =  owl.get_ontology(self.base_iri)

        with onto:
            # Atomic Classes

            class Track(owl.Thing): pass

            class Artist(owl.Thing): pass

            class Album(owl.Thing): pass

            class Genre(owl.Thing): pass

            # Properties

            class has_track_artist(Track >> Artist):
                python_name = "artists"

            class has_album_artist(Album >> Artist):
                python_name = "artists"

            class has_length_in_milliseconds(Track >> int, owl.FunctionalProperty):
                python_name = "length_in_milliseconds"

            class has_genre(Track >> Genre):
                python_name = "genres"

            # TODO: change this to `has_publishing_date`
            class has_year(Album >> int, owl.FunctionalProperty):
                python_name = "year"

            class has_track(Album >> Track):
                python_name = "tracks"

            class is_from_album(Track >> Album, owl.FunctionalProperty):
                inverse_property = has_track
                python_name = "album"

            class has_album_in_discography(Artist >> Album):
                inverse_property = has_album_artist
                python_name = "albums"

            # More classes

            VA = Artist("Various Artists")

            class VA_Album(Album):
                equivalent_to = [Album & has_album_artist.value(VA)]

            # class EP(Album): pass

            # class Single(Album): pass

            # Some individuals examples

            rock = Genre("Rock")
            hard_rock = Genre("Hard Rock")
            prog_rock = Genre("Progressive Rock")

            rush = Artist("Rush")

            tom_sawyer = Track(
                "Tom Sawyer",
                artists=[rush],
                length_in_milliseconds=276000,
                genres=[prog_rock, hard_rock, rock]
            )
            red_barchetta = Track(
                "Red Barchetta",
                artists=[rush],
                length_in_milliseconds=370000,
                genres=[prog_rock, hard_rock, rock]
            )
            yyz = Track(
                "YYZ",
                artists=[rush],
                length_in_milliseconds=265000,
                genres=[prog_rock, hard_rock, rock]
            )
            limelight = Track(
                "Limelight",
                artists=[rush],
                length_in_milliseconds=259000,
                genres=[prog_rock, hard_rock, rock]
            )
            camera_eye = Track(
                "Camera Eye",
                artists=[rush],
                length_in_milliseconds=658000,
                genres=[prog_rock, hard_rock, rock]
            )
            witch_hunt = Track(
                "Witch Hunt",
                artists=[rush],
                length_in_milliseconds=285000,
                genres=[prog_rock, hard_rock, rock]
            )
            vital_signs = Track(
                "Vital Signs",
                artists=[rush],
                length_in_milliseconds=286000,
                genres=[prog_rock, hard_rock, rock]
            )

            moving_pictures = Album(
                "Moving Pictures",
                artists=[rush],
                year=1981,
                tracks=[
                    tom_sawyer,
                    red_barchetta,
                    yyz,
                    limelight,
                    camera_eye,
                    witch_hunt,
                    vital_signs,
                ]
            )

        return onto

    def load(self) -> owl.Ontology:
        """Load the ontology."""
        return owl.get_ontology(self.base_iri).load()


if __name__ == "__main__":
    provider = MusicOntologyProvider()
    onto = provider.create()
    onto.save()