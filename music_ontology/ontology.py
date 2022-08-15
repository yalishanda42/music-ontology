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

            class SoloArtist(Artist): pass

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

            class has_group_member(MusicalEnsemble >> SoloArtist):
                python_name = "members"

            class is_member_of_group(SoloArtist >> MusicalEnsemble):
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

            geddy = SoloArtist("Geddy Lee")
            alex = SoloArtist("Alex Lifeson")
            neil = SoloArtist("Neil Peart")

            rush = MusicalEnsemble("Rush", members=[
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
                    written_by=[neil, SoloArtist("Pye Dubois")]
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
                artists=[rush, SoloArtist("Hugh Syme")],
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

            song2112 = Track(
                "2112",
                artists=[rush],
                length_in_milliseconds=1234000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'2112' Lyrics",
                    text="And the Meek shall inherit the Earth...",
                    written_by=[neil]
                )
            )

            bangkok = Track(
                "A Passage to Bangkok",
                artists=[rush],
                length_in_milliseconds=212000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'A Passage to Bangkok' Lyrics",
                    text="Our first stop is in Bogota\nTo check Colombian fields",
                    written_by=[neil]
                )
            )

            twilight_zone = Track(
                "The Twilight Zone",
                artists=[rush],
                length_in_milliseconds=196000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'The Twilight Zone' Lyrics",
                    text="A pleasant faced man steps up to greet you\nHe smiles and says he's pleased to meet you",
                    written_by=[neil]
                )
            )

            lessons = Track(
                "Lessons",
                artists=[rush],
                length_in_milliseconds=231000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Lessons' Lyrics",
                    text="Sweet memories flashing very quickly by\nReminding me and giving me a reason why",
                    written_by=[alex]
                )
            )

            tears = Track(
                "Tears",
                artists=[rush],
                length_in_milliseconds=210000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Tears' Lyrics",
                    text="All of the seaons\nAnd all of the days\nAll of the reasons\nWhy I've felt this way",
                    written_by=[geddy]
                )
            )

            something_for_nothing = Track(
                "Something For Nothing",
                artists=[rush],
                length_in_milliseconds=239000,
                genres=[prog_rock, hard_rock, rock],
                lyrics=Lyrics(
                    "'Something For Nothing' Lyrics",
                    text="Waiting for the winds of change\nTo sweep the clouds away",
                    written_by=[neil]
                )
            )

            album2112 = Album(
                "2112",
                artist=rush,
                year=1976,
                tracks=[
                    song2112,
                    bangkok,
                    twilight_zone,
                    lessons,
                    tears,
                    something_for_nothing,
                ]
            )

            metal = Genre("Metal")
            prog_metal = Genre("Progressive Metal")

            portnoy = SoloArtist("Mike Portnoy")
            petrucci = SoloArtist("John Petrucci")
            myung = SoloArtist("John Myung")
            rudess = SoloArtist("Jordan Rudess")
            labrie = SoloArtist("James LaBrie")

            dream_theater = MusicalEnsemble("Dream Theater", members=[
                portnoy, petrucci, myung, rudess, labrie
            ])

            as_i_am = Track(
                "As I Am",
                artists=[dream_theater],
                length_in_milliseconds=467000,
                genres=[prog_metal, metal],
                lyrics=Lyrics(
                    "'As I Am' Lyrics",
                    text="Don't tell me what's in\nTell me how to write",
                    written_by=[petrucci]
                )
            )

            this_dying_soul = Track(
                "This Dying Soul",
                artists=[dream_theater],
                length_in_milliseconds=687000,
                genres=[prog_metal, metal],
                lyrics=Lyrics(
                    "'This Dying Soul' Lyrics",
                    text="Hello mirror\nSo glad to see you my friend, it's been a while",
                    written_by=[portnoy]
                )
            )

            endless_sacrifice = Track(
                "Endless Sacrifice",
                artists=[dream_theater],
                length_in_milliseconds=684000,
                genres=[prog_metal, metal],
                lyrics=Lyrics(
                    "'Endless Sacrifice' Lyrics",
                    text="Cold, lying in my bed\nStaring into darkness",
                    written_by=[petrucci]
                )
            )

            honor_thy_father = Track(
                "Honor Thy Father",
                artists=[dream_theater],
                length_in_milliseconds=614000,
                genres=[prog_metal, metal],
                lyrics=Lyrics(
                    "'Honor Thy Father' Lyrics",
                    text="We're taught unconditional love\nThe blood is thicker than water",
                    written_by=[portnoy]
                )
            )

            vacant = Track(
                "Vacant",
                artists=[dream_theater],
                length_in_milliseconds=117000,
                genres=[prog_metal, metal],
                lyrics=Lyrics(
                    "'Vacant' Lyrics",
                    text="Hey you, hey you\nI'm right here",
                    written_by=[labrie]
                )
            )

            stream_of_consciousness = Track(
                "Stream of Consciousness",
                artists=[dream_theater],
                length_in_milliseconds=676000,
                genres=[prog_metal, metal]
            )

            in_the_name_of_god = Track(
                "In the Name of God",
                artists=[dream_theater],
                length_in_milliseconds=856000,
                genres=[prog_metal, metal],
                lyrics=Lyrics(
                    "'In the Name of God' Lyrics",
                    text="How can this be?\nWhy is he the chosen one?",
                    written_by=[petrucci]
                )
            )

            train_of_thought = Album(
                "Train of Thought",
                artist=dream_theater,
                year=2003,
                tracks=[
                    as_i_am,
                    this_dying_soul,
                    endless_sacrifice,
                    honor_thy_father,
                    vacant,
                    stream_of_consciousness,
                    in_the_name_of_god,
                ]
            )

            instrumental_rock = Genre("Instrumental Rock")

            levin = SoloArtist("Tony Levin")

            lte = MusicalEnsemble("Liquid Tension Experiment", members=[
                portnoy, petrucci, levin, rudess
            ])

            paradigm_shift = Track(
                "Paradigm Shift",
                artists=[lte],
                length_in_milliseconds=535000,
                genres=[instrumental_rock, prog_metal]
            )

            osmosis = Track(
                "Osmosis",
                artists=[lte],
                length_in_milliseconds=206000,
                genres=[instrumental_rock, prog_metal]
            )

            kindred_spirits = Track(
                "Kindred Spirits",
                artists=[lte],
                length_in_milliseconds=389000,
                genres=[instrumental_rock, prog_metal]
            )

            the_stretch = Track(
                "The Stretch",
                artists=[lte],
                length_in_milliseconds=120000,
                genres=[instrumental_rock, prog_metal]
            )

            freedom_of_speech = Track(
                "Freedom of Speech",
                artists=[lte],
                length_in_milliseconds=559000,
                genres=[instrumental_rock, prog_metal]
            )

            chris_and_kevins_excellent_adventure = Track(
                "Chris and Kevin's Excellent Adventure",
                artists=[lte],
                length_in_milliseconds=141000,
                genres=[instrumental_rock, prog_metal]
            )

            state_of_grace = Track(
                "State of Grace",
                artists=[lte],
                length_in_milliseconds=856000,
                genres=[instrumental_rock, prog_metal]
            )

            universal_mind = Track(
                "Universal Mind",
                artists=[lte],
                length_in_milliseconds=301000,
                genres=[instrumental_rock, prog_metal]
            )

            three_minute_warning = Track(
                "Three Minute Warning",
                artists=[lte],
                length_in_milliseconds=1716000,  # a long long boii
                genres=[instrumental_rock, prog_metal]
            )

            liquid_tension_experiment_album = Album(
                "Liquid Tension Experiment I",
                artist=lte,
                year=1999,
                tracks=[
                    paradigm_shift,
                    osmosis,
                    kindred_spirits,
                    the_stretch,
                    freedom_of_speech,
                    chris_and_kevins_excellent_adventure,
                    state_of_grace,
                    universal_mind,
                    three_minute_warning,
                ]
            )

            # Disjoints

            owl.AllDisjoint([EP, Single, Compilation])
            owl.AllDisjoint([SoloArtist, MusicalEnsemble])

            # Distinct individuals

            owl.AllDifferent(Artist.instances())
            owl.AllDifferent(SoloArtist.instances())
            owl.AllDifferent(MusicalEnsemble.instances())
            owl.AllDifferent(Album.instances())
            owl.AllDifferent(EP.instances())
            owl.AllDifferent(Single.instances())
            owl.AllDifferent(Compilation.instances())
            owl.AllDifferent(Track.instances())
            owl.AllDifferent(Lyrics.instances())
            owl.AllDifferent(Genre.instances())

        return onto

    def load(self) -> owl.Ontology:
        """Load the ontology."""
        return owl.get_ontology(self.base_iri).load()


if __name__ == "__main__":
    provider = MusicOntologyProvider()
    onto = provider.create()
    onto.save()
