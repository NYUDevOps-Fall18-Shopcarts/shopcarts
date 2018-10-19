# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Shopcart Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from app.model import Shopcart, DataValidationError, db
from app import app

DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')

######################################################################
#  T E S T   C A S E S
######################################################################

class TestPets(unittest.TestCase):

    """ Test Cases for Shopcarts """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Shopcart.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_serialize_a_shopcart_entry(self):
        """ Test serialization of a Shopcart """
        shopcart = Shopcart(user_id = 1, product_id = 1, quantity = 1, price = 12.00)
        data = shopcart.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('user_id', data)
        self.assertEqual(data['user_id'], 1)
        self.assertIn('product_id', data)
        self.assertEqual(data['product_id'], 1)
        self.assertIn('quantity', data)
        self.assertEqual(data['quantity'], 1)
        self.assertIn('price', data)
        self.assertEqual(data['price'], 12.00)

    def test_deserialize_a_shopcart_entry(self):
        """ Test deserialization of a Shopcart """
        data = {"user_id": 1, "product_id": 1, "quantity": 1, "price": 12.00}
        shopcart = Shopcart()
        shopcart.deserialize(data)
        self.assertNotEqual(shopcart, None)
        self.assertEqual(shopcart.user_id, 1)
        self.assertEqual(shopcart.product_id, 1)
        self.assertEqual(shopcart.quantity, 1)
        self.assertEqual(shopcart.price, 12.00)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        shopcart = Shopcart()
        self.assertRaises(DataValidationError, shopcart.deserialize, data)

    def test_find_shopcart_entry(self):
        """ Find a Shopcart by user_id and product_id """
        Shopcart(user_id=1, product_id=1, quantity=1, price=12.00).save()
        entry = Shopcart(user_id=1, product_id=2, quantity=1, price=15.00)
        entry.save()
        shopcart = Shopcart.find(entry.user_id, entry.product_id)
        self.assertIsNot(shopcart, None)
        self.assertEqual(shopcart.user_id, 1)
        self.assertEqual(shopcart.product_id, 2)
        self.assertEqual(shopcart.quantity, 1)
        self.assertEqual(shopcart.price, 15.00)

    def test_update_a_shopcart(self):
        """ Update a Shopcart """
        shopcart = Shopcart(user_id = 1, product_id = 1, quantity = 1, price = 12.00)
        shopcart.save()
        self.assertEqual(shopcart.user_id, 1)
        self.assertEqual(shopcart.product_id, 1)
        # Change it an save it
        shopcart.quantity = 3
        shopcart.save()
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        shopcart = Shopcart.find(shopcart.user_id, shopcart.product_id)
        self.assertIsNot(shopcart, None)
        self.assertEqual(shopcart.user_id, 1)
        self.assertEqual(shopcart.product_id, 1)
        self.assertEqual(shopcart.quantity, 3)
        self.assertEqual(shopcart.price, 12.00)

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
