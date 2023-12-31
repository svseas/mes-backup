from odoo.tests.common import TransactionCase
from datetime import date
from odoo.tests import tagged
from odoo.exceptions import ValidationError
from psycopg2 import IntegrityError


class TestManufacturingOrder(TransactionCase):
    # Class variable to count the number of tests passed
    tests_passed = 0
    test_failed = False  # A flag to indicate if a test failed
    total_tests = 0

    def setUp(self):
        super(TestManufacturingOrder, self).setUp()

        # Mocked records
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
        })

        # Getting the current user to use as the creator and approver for the BOM
        current_user = self.env.user

        # Required fields for the BOM model are included
        self.bom_1 = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_id': self.product.id,
            'ng_percent': 5.0,
            'created_by': current_user.id,
            'approved_by': current_user.id,
            'bom_uom': 'Units',
        })

        self.bom_2 = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_id': self.product.id,
            'ng_percent': 10.0,
            'created_by': current_user.id,
            'approved_by': current_user.id,
            'bom_uom': 'Units',
        })

        self.manufacturing_order = self.env['mes.manufacturing.order'].create({
            'name': 'Test MO',
            'code': 'MO001',
            'product': self.product.id,
            'bom': self.bom_1.id,
            'quantity': 10,
            'uom': 'Units',
            'date_start': date.today(),
            'date_end': date.today(),
        })

    def tearDown(self):
        # If test_failed is still False, then the test passed
        if not self.test_failed:
            TestManufacturingOrder.tests_passed += 1

    def test_onchange_product(self):
        try:
            # Setting product which triggers the onchange
            self.manufacturing_order.product = self.product.id

            # Trigger the onchange method manually
            self.manufacturing_order._onchange_product()

            # Assert that bom field is cleared
            self.assertFalse(self.manufacturing_order.bom)

            # Assert the domain is correct
            domain = self.manufacturing_order._onchange_product().get('domain', {}).get('bom', [])
            self.assertTrue(('id', 'in', [self.bom_1.id, self.bom_2.id]) in domain)
            # Print that the test passed
            print("test_onchange_product PASSED!")
        except AssertionError:
            # Print that the test failed
            print("test_onchange_product FAILED!")
            # Set the test_failed flag to True
            self.test_failed = True

    @classmethod
    def tearDownClass(cls):
        # This will be called at the very end, after all tests have run
        print(f"Total tests passed: {cls.tests_passed}")
