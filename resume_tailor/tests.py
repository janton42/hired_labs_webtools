from django.test import TestCase

from .models import Location, Participant

class LocationTests(TestCase):
    def test_add_loc(self):
        loc = Location(\
        city='San Mateo',\
        state='CA',\
        country='United States'\
        )
        out_str = '{}, {}, {}'.format(loc.city, loc.state, loc.country)

        self.assertEqual(out_str,\
        'San Mateo, CA, United States')

class ParticipantTests(TestCase):
    def test_add_participant(self):
        person = Participant(\
        user ='admin',\
        loc ='MD',\
        phone =9817289198,\
        linkedin ='https://www.linkedin.com/in/powlkjfkjpk',\
        )
        out_str = '{}, {}, {}, {}'.format(\
        person.user,\
        person.loc,\
        person.phone,\
        person.linkedin
        )

        self.assertEqual(out_str,\
        'sam_54, MD, 9817289198')
