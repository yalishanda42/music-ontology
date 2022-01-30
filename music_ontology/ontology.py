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

            class MusicalEnsemble(Artist): pass

            class Album(owl.Thing): pass

            class EP(Album): pass

            class Single(Album): pass

            class Compilation(Album): pass

            class Genre(owl.Thing): pass

            class Lyrics(owl.Thing): pass

            # Properties

            class has_track_artist(Track >> Artist):
                python_name = "artists"

            class has_album_artist(Album >> Artist, owl.FunctionalProperty):
                python_name = "artist"

            class has_length_in_milliseconds(Track >> int, owl.FunctionalProperty):
                python_name = "length_in_milliseconds"

            class has_genre(Track >> Genre):
                python_name = "genres"

            class has_year(Album >> int, owl.FunctionalProperty):
                python_name = "year"

            class has_track(Album >> Track):
                python_name = "tracks"

            class appears_in_album(Track >> Album):
                inverse_property = has_track
                python_name = "albums"

            class has_album_in_discography(Artist >> Album):
                inverse_property = has_album_artist
                python_name = "discography"

            class has_group_member(MusicalEnsemble >> Artist):
                python_name = "members"

            class is_member_of_group(Artist >> MusicalEnsemble):
                inverse_property = has_group_member
                python_name = "groups"

            class has_lyrics(Track >> Lyrics, owl.FunctionalProperty):
                python_name = "lyrics"

            class are_of_track(Lyrics >> Track, owl.FunctionalProperty):
                inverse_property = has_lyrics
                python_name = "track"

            class written_by(Lyrics >> Artist):
                python_name = "written_by"

            class has_written_lyrics(Artist >> Lyrics):
                inverse_property = written_by
                python_name = "lyrics_written"

            class text(Lyrics >> str, owl.FunctionalProperty):
                python_name = "text"

            # More classes

            VA = Artist("Various Artists")

            class VA_Album(Album):
                equivalent_to = [Album & has_album_artist.value(VA)]

            class Duet(MusicalEnsemble):
                equivalent_to = [MusicalEnsemble & has_group_member.exactly(2)]

            class Trio(MusicalEnsemble):
                equivalent_to = [MusicalEnsemble & has_group_member.exactly(3)]

            class Quartet(MusicalEnsemble):
                equivalent_to = [MusicalEnsemble & has_group_member.exactly(4)]

            class Quintet(MusicalEnsemble):
                equivalent_to = [MusicalEnsemble & has_group_member.exactly(5)]

            class BigBand(MusicalEnsemble):
                equivalent_to = [MusicalEnsemble & has_group_member.min(10)]

            class InstrumentalTrack(Track):
                equivalent_to = [Track & owl.Not(has_lyrics.some(Lyrics))]

            class InstrumentalAlbum(Album):
                equivalent_to = [Album & has_track.only(InstrumentalTrack)]

            # Some individuals examples

            rock = Genre("Rock")
            hard_rock = Genre("Hard Rock")
            prog_rock = Genre("Progressive Rock")

            geddy = Artist("Geddy Lee")
            alex = Artist("Alex Lifeson")
            neil = Artist("Neil Peart")

            rush = Artist("Rush", members=[
                geddy,
                alex,
                neil,
            ])

            tom_sawyer = Track(
                "Tom Sawyer",
                artists=[rush],
                length_in_milliseconds=276000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Tom Sawyer' Lyrics",
                    text="A modern day warrior\nMean mean stride\nToday's Tom Sawyer\nMean mean pride",
                    written_by=[neil, Artist("Pye Dubois")]
                )
            )
            red_barchetta = Track(
                "Red Barchetta",
                artists=[rush],
                length_in_milliseconds=370000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Red Barchetta' Lyrics",
                    text="My uncle has a country place\nThat no one knows about",
                    written_by=[neil]
                )
            )
            yyz = Track(
                "YYZ",
                artists=[rush],
                length_in_milliseconds=265000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=None
            )
            limelight = Track(
                "Limelight",
                artists=[rush],
                length_in_milliseconds=259000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Limelight' Lyrics",
                    text="Living on a lighted stage\nApproaches the unreal",
                    written_by=[neil]
                )
            )
            camera_eye = Track(
                "Camera Eye",
                artists=[rush],
                length_in_milliseconds=658000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Camera Eye' Lyrics",
                    text="Grim faced and forbidding, their faces closed tight\nAn angular mass of New Yorkers",
                    written_by=[neil]
                )
            )
            witch_hunt = Track(
                "Witch Hunt",
                artists=[rush, Artist("Hugh Syme")],
                length_in_milliseconds=285000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Witch Hunt' Lyrics",
                    text="The night is black, without a moon\nThe air is thick and still",
                    written_by=[neil]
                )
            )
            vital_signs = Track(
                "Vital Signs",
                artists=[rush],
                length_in_milliseconds=286000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Vital Signs' Lyrics",
                    text="Unstable condition\nA symptom of life\nIn mental and environmental change",
                    written_by=[neil]
                )
            )

            moving_pictures = Album(
                "Moving Pictures",
                artist=rush,
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