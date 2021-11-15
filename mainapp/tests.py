# from django.test import TestCase
#
# from mainapp.models import ProductCategory, Product
# from django.test.client import Client
#
#
# class TestMainSmokeTest(TestCase):
#     status_code_success = 200
#
#     def SetUp(self) -> None:
#         category = ProductCategory.objects.create(name='Test')
#         Product.objects.create(category=category, name='product_test', price=100)
#         Product.objects.create(category=category, name='product_test_1', price=50)
#
#         self.client = Client()
#
#     # def test_product_pages(self):
#     #     response = self.client.get('/')
#     #     self.assertEqual(response.status_code, self.status_code_success)
#
#     # def test_products_product(self):
#     #     for product_item in Product.objects.all():
#     #         response = self.client.get(f'/products/detail/{product_item.pk}/')
#     #         self.assertEqual(response.status_code, self.status_code_success)
#
#     def test_product_basket(self):
#         response = self.client.get('/users/profile/')
#         self.assertEqual(response.status_code, 302)
#
#     def TearDown(self) -> None:
#         pass
