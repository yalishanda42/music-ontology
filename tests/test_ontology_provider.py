import unittest

from music_ontology.ontology import MusicOntologyProvider
import owlready2 as owl

class OntologyTests(unittest.TestCase):
    def test_create_save_load_produces_same_ontology(self):
        """Test that create, save, load produces the same ontology."""

        sut = MusicOntologyProvider()

        ontology = sut.create()
        ontology.save()
        ontology2 = sut.load()

        self.assertEqual(ontology, ontology2)

    def test_inverse_property(self):
        """Test that inverse properties are correctly set."""

        provider = MusicOntologyProvider()
        onto = provider.load()
        yyz = onto["YYZ"]
        moving_pictures = onto["Moving Pictures"]

        self.assertEqual(yyz.album, moving_pictures)
        self.assertTrue(yyz in moving_pictures.tracks)


if __name__ == "__main__":
    unittest.main()