import html
import math
import re
from gevent import monkey


def stub(*args, **kwargs):
	pass


monkey.patch_all = stub

from cartmigration.libs.utils import *

from cartmigration.models.cart.bigcommerce import LeCartBigcommerce


class LeCartBigcommercev3(LeCartBigcommerce):
	LIST_CUSTOMER_GROUP_MAP = {1: 11, 2: 12, 3: 13, 4: 14, 5: 15, 6: 16, 7: 17, 8: 18, 9: 19, 10: 20, 11: 21, 12: 22, 13: 23, 14: 24, 15: 25, 16: 26, 17: 27, 18: 28, 19: 29, 20: 30, 21: 31, 22: 32, 23: 33, 24: 34, 25: 35, 26: 36, 27: 37, 28: 38, 29: 39, 30: 40, 31: 41, 32: 42, 33: 43, 34: 44, 35: 45, 36: 46, 37: 47, 38: 48, 39: 49, 40: 50, 41: 51, 42: 52, 43: 53, 44: 54, 45: 55, 46: 56, 47: 57, 48: 58, 49: 59, 50: 60, 51: 61, 52: 62, 53: 63, 54: 64, 55: 65, 56: 66, 57: 67, 58: 68, 59: 69, 60: 70, 61: 71, 62: 72, 63: 73, 64: 74, 65: 75, 66: 76, 67: 77, 68: 78, 69: 79, 70: 80, 71: 81, 72: 82, 73: 83, 74: 84, 75: 85, 76: 86, 77: 87, 78: 88, 79: 89, 80: 90, 81: 91, 82: 92, 83: 93, 84: 94, 85: 95, 86: 96, 87: 97, 88: 98, 89: 99, 90: 100, 92: 101, 93: 102, 94: 103, 95: 104, 96: 105, 97: 106, 98: 107, 99: 108, 100: 109, 101: 110, 102: 111, 103: 112, 104: 113, 105: 114, 106: 115, 107: 116, 108: 117, 109: 118, 110: 119, 111: 120, 112: 121, 113: 122, 114: 123, 115: 124, 116: 125, 117: 126, 118: 127, 119: 128, 120: 129, 121: 130, 122: 131, 123: 132, 124: 133, 125: 134, 126: 135, 127: 136, 128: 137, 129: 138, 130: 139, 131: 140, 132: 141, 133: 142, 134: 143, 135: 144, 136: 145, 137: 146, 138: 147, 139: 148, 140: 149, 141: 150, 142: 151, 143: 152, 144: 153, 145: 154, 146: 155, 147: 156, 148: 157, 149: 158, 150: 159, 151: 160, 152: 161, 153: 162, 154: 163, 155: 164, 156: 165, 157: 166, 158: 167, 159: 168, 160: 169, 161: 170, 162: 171, 163: 172, 164: 173, 165: 174, 166: 175, 167: 176, 168: 177, 169: 178, 170: 179, 171: 180, 172: 181, 173: 182, 174: 183, 175: 184, 176: 185, 177: 186, 178: 187, 179: 188, 180: 189, 181: 190, 182: 191, 183: 192, 184: 193, 185: 194, 186: 195, 187: 196, 188: 197, 189: 198, 190: 199, 191: 200, 192: 201, 193: 202, 194: 203, 195: 204, 196: 205, 197: 206, 198: 207, 199: 208, 200: 209, 201: 210, 202: 211, 203: 212, 204: 213, 205: 214, 206: 215, 207: 216, 208: 217, 209: 218, 210: 219, 211: 220, 212: 221, 215: 222, 216: 223, 217: 224, 218: 225, 219: 226, 220: 227, 221: 228, 222: 229, 223: 230, 224: 231, 225: 232, 226: 233, 227: 234, 228: 235, 229: 236, 230: 237, 231: 238, 232: 239, 233: 240, 234: 241, 235: 242, 236: 243, 237: 244, 238: 245, 239: 246, 240: 247, 241: 248, 242: 249, 243: 250, 244: 251, 245: 252, 246: 253, 248: 254}

	# todo: clear
	def clear_target_products(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_manufacturers',
			'msg': ''
		}
		self._notice['target']['clear'] = next_clear
		if not self._notice['config']['products']:
			return next_clear
		while True:
			try:
				product_data = self.api_v3('/catalog/products?page=1&limit=10')
				if product_data:
					product_data = json_decode(product_data)
					if product_data and len(product_data['data']):
						api_delete_pro = self.api_v3('/catalog/products?is_visible=true', None, 'Delete')
						api_delete_pro = self.api_v3('/catalog/products?is_visible=false', None, 'Delete')
					else:
						return next_clear
				else:
					return next_clear
			except Exception:
				self.log_traceback()
				return next_clear
		return next_clear


	def clear_target_manufacturers(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_categories',
			'msg': ''
		}
		self._notice['target']['clear'] = next_clear
		if not self._notice['config']['manufacturers']:
			return next_clear
		brands = self.api_v3('/catalog/brands')
		if brands:
			brands = json_decode(brands)
			if brands['data'] and to_len(brands['data']) > 0:
				for brand in brands['data']:
					try:
						res = self.api_v3('/catalog/brands/' + to_str(brand['id']), None, 'Delete')
					except Exception:
						self.log_traceback()
						return next_clear
		return next_clear


	def clear_target_categories(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_orders',
			'msg': ''
		}
		self._notice['target']['clear'] = next_clear
		if not self._notice['config']['categories']:
			return next_clear
		try:
			api_delete_categories = self.api_v3('/catalog/categories?is_visible=false', None, 'Delete')
			api_delete_categories = self.api_v3('/catalog/categories?is_visible=true', None, 'Delete')
		except Exception:
			self.log_traceback()
			return next_clear
		return next_clear


	def clear_target_customers(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_reviews',
			'msg': ''
		}
		self._notice['target']['clear'] = next_clear
		if not self._notice['config']['customers']:
			return next_clear
		check = True
		while check:
			customer_data = self.api_v3('/customers?page=1&sort=id&limit=50')
			if customer_data:
				customer_data = json_decode(customer_data)
				if customer_data and customer_data.get('data') and to_len(customer_data.get('data')) > 0:
					customer_ids = duplicate_field_value_from_list(customer_data['data'], 'id')
					customer_id_con = self.list_to_in_condition(customer_ids)
					customer_id_con = customer_id_con.replace('(', '').replace(')', '')
					if to_len(customer_data['data']) < 50:
						check = False
					try:
						api_delete_customers = self.api_v3('/customers?id:in=' + customer_id_con, None, 'Delete')
					except Exception:
						self.log_traceback()
						return next_clear
				else:
					return next_clear
			else:
				return next_clear
		return next_clear


	# TODO: Clear target demo data

	def clear_target_taxes_demo(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_manufacturers_demo',
		}

		self._notice['target']['clear_demo'] = next_clear
		return self._notice['target']['clear_demo']


	def clear_target_manufacturers_demo(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_categories_demo',
		}
		self._notice['target']['clear_demo'] = next_clear
		if not self._notice['config']['manufacturers']:
			return next_clear
		where = {
			'migration_id': self._migration_id,
			'type': self.TYPE_MANUFACTURER
		}
		manufacturers = self.select_obj(TABLE_MAP, where)
		manufacturers_ids = list()
		if manufacturers['result'] == 'success':
			manufacturers_ids = duplicate_field_value_from_list(manufacturers['data'], 'id_desc')
		if not manufacturers_ids:
			return next_clear
		for manufacturer_id in manufacturers_ids:
			try:
				res = self.api_v3('/catalog/brands/' + to_str(manufacturer_id), None, 'Delete')
			except Exception:
				self.log_traceback()
				return next_clear
		return next_clear


	def clear_target_categories_demo(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_products_demo',
		}
		self._notice['target']['clear_demo'] = next_clear
		if not self._notice['config']['categories']:
			return next_clear
		where = {
			'migration_id': self._migration_id,
			'type': self.TYPE_CATEGORY
		}
		categories = self.select_obj(TABLE_MAP, where)
		category_ids = list()
		if categories['result'] == 'success':
			category_ids = duplicate_field_value_from_list(categories['data'], 'id_desc')
		if not category_ids:
			return next_clear
		for category_id in category_ids:
			api_delete_categories = self.api_v3('/catalog/categories/' + to_str(category_id), None, 'Delete')
		return next_clear


	def clear_target_products_demo(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_orders_demo',
		}
		self._notice['target']['clear_demo'] = next_clear
		if not self._notice['config']['products']:
			return next_clear
		where = {
			'migration_id': self._migration_id,
			'type': self.TYPE_PRODUCT
		}
		products = self.select_obj(TABLE_MAP, where)
		product_ids = list()
		if products['result'] == 'success':
			product_ids = duplicate_field_value_from_list(products['data'], 'id_desc')
		if not product_ids:
			return next_clear
		for product_id in product_ids:
			api_delete_pro = self.api_v3('/catalog/products/' + to_str(product_id), None, 'Delete')
		return next_clear


	def clear_target_customers_demo(self):
		next_clear = {
			'result': 'process',
			'function': 'clear_target_orders_demo',
		}
		self._notice['target']['clear_demo'] = next_clear
		if not self._notice['config']['customers']:
			return next_clear
		where = {
			'migration_id': self._migration_id,
			'type': self.TYPE_CUSTOMER
		}
		customers = self.select_obj(TABLE_MAP, where)
		customer_ids = list()
		if customers['result'] == 'success':
			customer_ids = duplicate_field_value_from_list(customers['data'], 'id_desc')
		if not customer_ids:
			return next_clear
		for customer_id in customer_ids:
			api_delete_customers = self.api_v3('/customers/' + to_str(customer_id), None, 'Delete')
		return next_clear


	# TODO: MANUFACTURER
	def prepare_manufacturers_import(self):
		return self


	def prepare_manufacturers_export(self):
		return self


	def get_manufacturers_main_export(self):
		imported = self._notice['process']['manufacturers']['imported']
		id_src = to_int(self._notice['process']['manufacturers']['id_src'])
		limit = self._notice['setting']['manufacturers']
		page = math.floor(math.floor(to_decimal(imported) / to_decimal(limit))) + 1
		api_brands = self.api_v3('/catalog/brands?page=' + to_str(page) + '&sort=id&limit=' + to_str(limit))
		brands = json_decode(api_brands)
		if not brands or not brands.get('data') or to_len(brands['data']) == 0:
			return response_error(self.console_error("Could not get manufacturers data from Bigcommerce"))
		return response_success(brands['data'])


	def get_manufacturers_ext_export(self, manufacturers):
		return response_success()


	def convert_manufacturer_export(self, manufacturer, manufacturers_ext):
		manufacturer_data = self.construct_manufacturer()
		manufacturer_data['id'] = manufacturer['id']
		manufacturer_data['name'] = manufacturer['name']
		manufacturer_data['meta_title'] = manufacturer.get('page_title')
		manufacturer_data['meta_keyword'] = ', '.join(manufacturer['meta_keywords']) if manufacturer.get('meta_keywords') and to_len(manufacturer['meta_keywords']) > 0 else ''
		manufacturer_data['meta_description'] = manufacturer.get('meta_description')
		if manufacturer['image_url']:
			manufacturer_data['thumb_image']['url'] = manufacturer['image_url']
			manufacturer_data['thumb_image']['path'] = ''
		manufacturer_data['url'] = manufacturer['custom_url']['url'] if manufacturer.get('custom_url') and 'url' in manufacturer['custom_url'] else None
		manufacturer_data['created_at'] = get_current_time()
		manufacturer_data['updated_at'] = get_current_time()
		for language_id, language_label in self._notice['src']['languages'].items():
			manufacturer_language_data = dict()
			manufacturer_language_data['name'] = manufacturer['name']
			manufacturer_data['languages'][language_id] = manufacturer_language_data
		return response_success(manufacturer_data)


	def get_manufacturer_id_import(self, convert, manufacturer, manufacturers_ext):
		return manufacturer['id']


	def check_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return True if self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['id'], convert['code']) else False


	def router_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success('manufacturer_import')


	def before_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success()


	def manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		manufacturers_data = {
			'name': to_str(convert['name'])[:255],
			'page_title': to_str(convert['meta_title'])[:255],
			'meta_keywords': [to_str(convert.get('meta_keyword', ''))],
			'meta_description': to_str(convert.get('meta_description', '')),
		}
		# if convert['thumb_image']['url'] or convert['thumb_image']['path']:
		# 	image_process = self.process_image_before_import(convert['thumb_image']['url'], convert['thumb_image']['path'])
		# 	if image_process['url']:
		# 		manufacturers_data['image_url'] = to_str(image_process['url']).replace(' ', '%20')
		if convert.get('url') and convert.get('url') != '':
			manufacturers_data['custom_url'] = {
				'url': '/' + to_str(convert['url']).lstrip('/'),
				'is_customized': True,
			}
		response = self.api_v3('/catalog/brands', manufacturers_data, 'Post')
		if (not response or response == '') and manufacturers_data['image_url']:
			check_image = self.image_exist(manufacturers_data['image_url'])
			if not check_image:
				del manufacturers_data['image_url']
				response = self.api_v3('/catalog/brands', manufacturers_data, 'Post')
		response_data = json_decode(response)
		while response_data and 'status' in response_data and to_str(response_data['status']) == '409':
			manufacturers_data['name'] = manufacturers_data['name'] + '-1'
			response = self.api_v3('/catalog/brands', manufacturers_data, 'Post')
			response_data = json_decode(response)
		if isinstance(response, dict):
			if 'status' in response_data and to_str(response_data['status']) in ['400', '422']:
				return response_error('Manufacturers ' + to_str(convert['id']) + 'import fail. Error: ' + to_str(response_data['title']))
		if not response_data or 'data' not in response_data or to_len(response_data['data']) == 0:
			return response_error("Manufacturer " + to_str(convert['id']) + " import false!")
		self.insert_map(self.TYPE_MANUFACTURER, convert['id'], response_data['data']['id'], convert['code'])
		return response_success(response_data['data']['id'])


	def after_manufacturer_import(self, manufacturer_id, convert, manufacturer, manufacturers_ext):
		return response_success()


	def addition_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
		return response_success()


	# TODO: CATEGORY
	def prepare_categories_import(self):
		return self


	def prepare_categories_export(self):
		return self


	def get_categories_main_export(self):
		imported = self._notice['process']['categories']['imported']
		id_src = to_int(self._notice['process']['categories']['id_src'])
		limit = self._notice['setting']['categories']
		page = math.floor(math.floor(to_decimal(imported) / to_decimal(limit))) + 1
		api_categories = self.api_v3('/catalog/categories?page=' + to_str(page) + '&sort=id&limit=' + to_str(limit))
		categories_data = json_decode(api_categories)
		if not categories_data or categories_data == '' or not categories_data.get('data') or to_len(categories_data['data']) == 0:
			return response_error(self.console_error("Could not get category data from Bigcommerce"))
		return response_success(categories_data['data'])


	def get_categories_ext_export(self, categories):
		return response_success()


	def convert_category_export(self, category, categories_ext):
		category_data = self.construct_category()
		parent = self.construct_category_parent()
		parent['id'] = 0
		if to_int(category['parent_id']) > 0:
			parent = self.get_category_parent(category['parent_id'])
			if parent['result'] == 'success':
				parent = parent['data']

		category_data['id'] = category['id']
		category_data['parent'] = parent
		category_data['active'] = True if category['is_visible'] else False
		if category['image_url'] or to_str(category['image_url']) != '':
			category_data['thumb_image']['url'] = category['image_url']
			category_data['thumb_image']['path'] = ''
		category_data['sort_order'] = category['sort_order']
		category_data['created_at'] = get_current_time()
		category_data['updated_at'] = get_current_time()
		category_data['category'] = category
		category_data['categoriesExt'] = categories_ext
		category_data['name'] = self.remove_html(category['name'])
		category_data['meta_title'] = category['page_title']
		category_data['meta_keyword'] = ', '.join(category['meta_keywords']) if category.get('meta_keywords') and to_len(category['meta_keywords']) > 0 else ''
		category_data['meta_description'] = category['meta_description']
		category_data['description'] = to_str(category['description']).replace('%%GLOBAL_ShopPath%%', self._notice['src']['cart_url'].strip('/')).replace('%%GLOBAL_CdnStorePath%%', self._cart_url.strip('/'))
		for language_id, label in self._notice['src']['languages'].items():
			category_language_data = self.construct_category_lang()
			category_language_data['name'] = self.remove_html(category['name'])
			category_language_data['meta_title'] = category['page_title']
			category_language_data['meta_keyword'] = ', '.join(category['meta_keywords']) if category.get('meta_keywords') and to_len(category['meta_keywords']) > 0 else ''
			category_language_data['meta_description'] = category['meta_description']
			category_language_data['description'] = to_str(category['description']).replace('%%GLOBAL_ShopPath%%', self._notice['src']['cart_url'].strip('/')).replace('%%GLOBAL_CdnStorePath%%', self._cart_url.strip('/'))
			category_data['languages'][language_id] = category_language_data

		detect_seo = self.detect_seo()
		category_data['seo'] = getattr(self, 'categories_' + detect_seo)(category, categories_ext)
		return response_success(category_data)


	def get_category_parent(self, parent_id):
		api_categories = self.api_v3('/catalog/categories/' + to_str(parent_id))
		categories_data = json_decode(api_categories)
		if not categories_data or not categories_data.get('data') or to_len(categories_data['data']) == 0:
			return response_error(self.console_error("Could not get category parent data from Bigcommerce"))
		categories = response_success([categories_data['data']])
		category = categories_data['data']
		categories_ext = self.get_categories_ext_export(categories)
		parent_data = self.convert_category_export(category, categories_ext)
		return parent_data


	def get_category_id_import(self, convert, category, categories_ext):
		return category['id']


	def check_category_import(self, convert, category, categories_ext):
		return self.get_map_field_by_src(self.TYPE_CATEGORY, convert['id'], convert['code'])


	def router_category_import(self, convert, category, categories_ext):
		return response_success('category_import')


	def before_category_import(self, convert, category, categories_ext):
		return response_success()


	def category_import(self, convert, category, categories_ext):
		parent_id = 0
		active = True if convert['active'] else False
		if convert['parent'] and 'id' in convert['parent'] and (convert['parent']['id'] or convert['parent']['code']) and convert['id'] != convert['parent']['id']:
			parent_import = self.import_category_parent(convert['parent'])
			if parent_import['result'] == 'success' and parent_import['data']:
				parent_id = parent_import['data']
				if not parent_import['active']:
					active = False
		category_name = self.strip_html_tag(get_value_by_key_in_dict(convert, 'name', ''))
		cat_data = {
			'parent_id': parent_id if parent_id else 0,
			'name': category_name[0:50],
			'description': get_value_by_key_in_dict(convert, 'description', ' '),
			'page_title': get_value_by_key_in_dict(convert, 'meta_title', ''),
			'search_keywords': get_value_by_key_in_dict(convert, 'meta_keyword', '')[:254],
			'meta_keywords': get_value_by_key_in_dict(convert, 'meta_keyword', '').split(','),
			'meta_description': get_value_by_key_in_dict(convert, 'meta_description', ''),
			'sort_order': to_int(get_value_by_key_in_dict(convert, 'sort_order', 0)),
			'is_visible': active,
		}
		if '&lt;' in cat_data['description']:
			cat_data['description'] = to_str(cat_data['description']).replace('&lt;', '<')
		if '&gt;' in cat_data['description']:
			cat_data['description'] = to_str(cat_data['description']).replace('&gt;', '>')
		if '&quot;' in cat_data['description']:
			cat_data['description'] = to_str(cat_data['description']).replace('&quot;', '"')
		if self._notice['config']['seo']:
			if 'seo' in convert and convert['seo']:
				default_url = get_row_value_from_list_by_field(convert['seo'], 'default', True, 'request_path')
				default_url = to_str(default_url).replace(' ', '-')
				default_url = to_str(default_url).replace('--', '-')
				if default_url:
					cat_data['custom_url'] = {
						'url': '/' + default_url.lstrip('/'),
						'is_customized': True
					}
				else:
					for seo_url in convert['seo']:
						if seo_url['request_path']:
							cat_data['custom_url'] = {
								'url': '/' + seo_url['request_path'].lstrip('/'),
								'is_customized': True
							}
							break

		# if convert['thumb_image']['url'] or convert['thumb_image']['path']:
		# 	image_process = self.process_image_before_import(convert['thumb_image']['url'], convert['thumb_image']['path'])
		# 	if image_process['url']:
		# 		cat_data['image_url'] = to_str(image_process['url']).replace(' ', '%20')

		response = self.api_v3('/catalog/categories', cat_data, 'Post')
		old_name = cat_data['name']
		if (not response or response == '') and cat_data['image_url']:
			check_image = self.image_exist(cat_data['image_url'])
			if not check_image:
				del cat_data['image_url']
				response = self.api_v3('/catalog/brands', cat_data, 'Post')
		response_data = json_decode(response)
		n = 0
		while response_data and 'status' in response_data and to_str(response_data['status']) == '409' and n < 5:
			n += 1
			index = to_str(to_int(time.time()))
			max_len = 49 - len(index)
			new_name = old_name[0:max_len] + ' ' + to_str(index)
			cat_data['name'] = new_name
			response = self.api_v3('/catalog/categories', cat_data, 'Post')
			response_data = json_decode(response)
		if 'status' in response_data and to_str(response_data['status']) in ['400', '422']:
			return response_error('Category ' + to_str(convert['id']) + 'import fail. Error: ' + to_str(response_data['title']))
		if not response_data or 'data' not in response_data or to_len(response_data['data']) == 0:
			return response_error('Category ' + to_str(convert['id']) + 'import fail.')

		# image
		if convert['thumb_image']:
			image_process = self.process_image_before_import(convert['thumb_image']['url'], convert['thumb_image']['path'])
			if image_process['url']:
				img_data = {'image_url': image_process['url']}
				a = self.api_img_cate('/catalog/categories/' + to_str(response_data['data']['id']), img_data, 'put')

		self.insert_map(self.TYPE_CATEGORY, convert['id'], response_data['data']['id'], convert['code'], response_data['data']['name'], active)
		res = response_success(response_data['data']['id'])
		res['active'] = active
		return res


	def import_category_parent(self, convert_parent):
		check_parent_imported = self.select_map(self._migration_id, self.TYPE_CATEGORY, convert_parent['id'], None, convert_parent['code'])
		category = get_value_by_key_in_dict(convert_parent, 'category', dict())
		categories_ext = get_value_by_key_in_dict(convert_parent, 'categories_ext', dict())
		if check_parent_imported:
			res = response_success(check_parent_imported['id_desc'])
			res['active'] = check_parent_imported['value']
			return res
		return self.category_import(convert_parent, category, categories_ext)


	def addition_category_import(self, convert, category, categories_ext):
		return response_success()


	# TODO: PRODUCT
	def prepare_products_import(self):
		return self


	def prepare_products_export(self):
		return self


	def get_products_main_export(self):
		imported = self._notice['process']['products']['imported']
		limit = self._notice['setting']['products']
		id_src = to_int(self._notice['process']['products']['id_src'])
		page = math.floor(int(imported) / to_int(limit)) + 1
		products = self.api_v3('/catalog/products?id:greater=' + to_str(id_src) + '&sort=id&limit=' + to_str(limit))
		products_data = json.loads(products)
		if not products or not products_data or to_str(products_data) == '' or not products_data.get('data') or to_len(products_data['data']) == 0:
			return response_error(self.console_error("Could not get Product data from Bigcommerce"))
		return response_success(products_data['data'])


	def get_product_by_id(self, product_id):
		product = self.api_v3('/catalog/products/' + to_str(product_id))
		product_data = json.loads(product)
		if not product or not product_data or to_str(product) == '' or not product.get('data'):
			return response_error(self.console_error("Could not get Product data from Bigcommerce"))
		product_data = [product_data['data']]
		return response_success(product_data)


	def get_products_ext_export(self, products):
		result = dict()
		for product in products['data']:
			result[product['id']] = dict()

			api_discount = self.api_v3('/catalog/products/' + to_str(product['id']) + '/bulk-pricing-rules')
			discount_rules = json_decode(api_discount)
			if api_discount and discount_rules and discount_rules.get('data'):
				discount_rules = discount_rules['data']
			else:
				discount_rules = list()

			api_images = self.api_v3('/catalog/products/' + to_str(product['id']) + '/images')
			images = json_decode(api_images)
			if api_images and images and images.get('data'):
				images = images['data']
			else:
				images = list()

			api_cus_field = self.api_v3('/catalog/products/' + to_str(product['id']) + '/custom-fields')
			cus_fields = json_decode(api_cus_field)
			if api_cus_field and cus_fields and cus_fields.get('data'):
				cus_fields = cus_fields['data']
			else:
				cus_fields = list()

			api_options = self.api_v3('/catalog/products/' + to_str(product['id']) + '/options')
			options_data = json_decode(api_options)
			if api_options and options_data and options_data.get('data'):
				options_data = options_data['data']
			else:
				options_data = list()

			api_variants = self.api_v3('/catalog/products/' + to_str(product['id']) + '/variants')
			api_data = json_decode(api_variants)
			if api_variants and api_data and api_data.get('data'):
				variants_data = api_data['data']
				while 'next' in api_data['meta']['pagination']['links']:
					api_variants = self.api_v3('/catalog/products/' + to_str(product['id']) + '/variants' +
					                           api_data['meta']['pagination']['links']['next'])
					api_data = json_decode(api_variants)
					if api_variants and api_data and api_data.get('data'):
						variants_data = [*variants_data, *api_data['data']]
			else:
				variants_data = list()

			api_rules = self.api_v3('/catalog/products/' + to_str(product['id']) + '/modifiers')
			rules_data = json_decode(api_rules)
			if api_rules and rules_data and rules_data.get('data'):
				rules_data = rules_data['data']
			else:
				rules_data = list()

			complex_rules = self.api_v3('/catalog/products/' + to_str(product['id']) + '/complex-rules')
			complex_data = json_decode(complex_rules)
			if complex_rules and complex_data and complex_data.get('data'):
				complex_data = complex_data['data']
			else:
				complex_data = list()

			result[product['id']]['options'] = options_data
			result[product['id']]['variants'] = variants_data
			result[product['id']]['modifiers'] = rules_data
			result[product['id']]['discount_rules'] = discount_rules
			result[product['id']]['images'] = images
			result[product['id']]['custom_fields'] = cus_fields
			result[product['id']]['complex_rules'] = complex_data

		return response_success(result)


	def convert_product_export(self, product, products_ext):
		products_ext_data = products_ext['data'][product['id']]
		product_data = self.construct_product()
		product_data['id'] = product['id']
		product_data['type'] = 'simple'
		product_data['sku'] = product['sku']
		product_data['upc'] = product.get('upc')
		product_data['weight'] = get_value_by_key_in_dict(product, 'weight', '')
		product_data['length'] = get_value_by_key_in_dict(product, 'depth', '')
		product_data['width'] = get_value_by_key_in_dict(product, 'width', '')
		product_data['height'] = get_value_by_key_in_dict(product, 'height', '')
		product_data['status'] = True if product['is_visible'] == 1 else False
		product_data['qty'] = get_value_by_key_in_dict(product, 'inventory_level', 0)
		product_data['manage_stock'] = False if product['inventory_tracking'] in {'none', 'variant'} else True
		product_data['created_at'] = convert_format_time(product['date_created'], "%a, %d %b %Y %H:%M:%S %z")
		product_data['updated_at'] = convert_format_time(product['date_modified'], "%a, %d %b %Y %H:%M:%S %z")
		product_data['name'] = product['name']
		product_data['description'] = to_str(get_value_by_key_in_dict(product, 'description', '')).replace('%%GLOBAL_ShopPath%%', self._cart_url.strip('/')).replace('%%GLOBAL_CdnStorePath%%', self._cart_url.strip('/'))
		product_data['short_description'] = ''
		product_data['meta_description'] = get_value_by_key_in_dict(product, 'meta_description', '')
		product_data['meta_title'] = get_value_by_key_in_dict(product, 'page_title', '')
		product_data['meta_keyword'] = ', '.join(product['meta_keywords']) if product.get('meta_keywords') and to_len(product['meta_keywords']) > 0 else ''
		product_data['tags'] = get_value_by_key_in_dict(product, 'search_keywords', '')
		product_data['is_featured'] = get_value_by_key_in_dict(product, 'is_featured', False)
		product_data['url_key'] = product['custom_url']['url'].replace('/', '')
		product_data['cost'] = to_decimal(product['cost_price'])

		if to_decimal(product['sale_price']) > 0:
			product_data['price'] = to_decimal(product['retail_price']) if product['retail_price'] and to_decimal(product['retail_price']) > 0 else product['price']
			product_data['special_price']['price'] = to_decimal(product['sale_price'])
		elif to_decimal(product['retail_price']) > 0 and to_decimal(product['retail_price']) > to_decimal(product['price']):
			product_data['price'] = to_decimal(product['retail_price'])
			product_data['special_price']['price'] = to_decimal(product['price'])
		else:
			product_data['price'] = to_decimal(product['price'])

		list_attributes = {
			'bin_picking_number': 'BIN picking number',
			'warranty': 'Warranty Infomation',
			'upc': 'Product UPC/EAN'
		}
		for attribute_code, attribute_label in list_attributes.items():
			if product.get(attribute_code):
				attribute_data = self.construct_product_attribute()
				attribute_data['option_code'] = attribute_code
				attribute_data['option_mode'] = 'backend'
				attribute_data['option_name'] = attribute_label
				attribute_data['option_type'] = 'text' if attribute_code != 'warranty' else 'textarea'
				attribute_data['option_value_code'] = ''
				attribute_data['option_value_name'] = product.get(attribute_code)
				product_data['attributes'].append(attribute_data)

		product_data['tax']['id'] = product['tax_class_id'] if product['tax_class_id'] else None
		product_data['tax']['code'] = 'Default Tax Class' if not product['tax_class_id'] else None

		if to_int(product['brand_id']) > 0:
			api_man = self.api_v3('/catalog/brands/' + to_str(product['brand_id']))
			if api_man:
				man_data = json_decode(api_man)
				if man_data and man_data.get('data') and to_len(man_data['data']) > 0:
					product_data['manufacturer']['name'] = man_data['data']['name']
				product_data['manufacturer']['id'] = product['brand_id']

		if product['categories']:
			for product_category in product['categories']:
				product_category_data = self.construct_product_category()
				product_category_data['id'] = product_category
				product_data['categories'].append(product_category_data)

		if product['related_products']:
			for relate in product['related_products']:
				if to_str(relate) == '-1':
					continue
				relation = self.construct_product_relation()
				relation['id'] = relate
				relation['type'] = self.PRODUCT_RELATE
				product_data['relate']['children'].append(relation)

		if to_len(products_ext_data['discount_rules']) > 0:
			for rule in products_ext_data['discount_rules']:
				rule_data = self.construct_product_tier_price()
				rule_data['qty'] = to_int(rule['quantity_min'])
				rule_data['price'] = to_decimal(rule['amount'])
				rule_data['price_type'] = rule['type']
				product_data['tier_prices'].append(rule_data)

		if products_ext_data['custom_fields']:
			for custom_field in products_ext_data['custom_fields']:
				attribute_data = self.construct_product_attribute()
				attribute_data['option_code'] = custom_field['name']
				attribute_data['option_mode'] = 'backend'
				attribute_data['option_name'] = custom_field['name']
				attribute_data['option_type'] = 'text'
				attribute_data['option_value_code'] = ''
				attribute_data['option_value_name'] = custom_field['value']
				product_data['attributes'].append(attribute_data)

		if products_ext_data['images']:
			for image in products_ext_data['images']:
				if 'url_zoom' in image and image['url_zoom']:
					real_path = re.sub("/\?.+/", "", to_str(image['url_zoom']))
					real_path = real_path[:real_path.find('?')]
					if image['is_thumbnail'] == 1:
						product_data['thumb_image']['label'] = image.get('description')
						product_data['thumb_image']['url'] = real_path
						product_data['thumb_image']['path'] = ''
					else:
						product_image_data = self.construct_product_image()
						product_image_data['label'] = image.get('description')
						product_image_data['url'] = real_path
						product_image_data['path'] = ''
						product_data['images'].append(product_image_data)

		# Migrate custom option
		if products_ext_data['modifiers']:
			option_datas = list()
			for modifier in products_ext_data['modifiers']:
				option_data = self.construct_product_option()
				option_data['id'] = modifier['id']
				if modifier['type'] in ['text', 'multi_line_text']:
					conf_type = self.OPTION_TEXT
				elif modifier['type'] == 'file':
					conf_type = self.OPTION_FILE
				elif modifier['type'] == 'checkbox':
					conf_type = self.OPTION_CHECKBOX
				else:
					conf_type = self.OPTION_SELECT

				option_data['code'] = modifier['name']
				option_data['option_code'] = modifier['name']
				option_data['option_type'] = conf_type
				option_data['option_name'] = modifier['display_name']
				option_data['sort_order'] = modifier['sort_order']
				option_data['required'] = True if modifier.get('required') else False
				if modifier['option_values']:
					for modifier_value in modifier['option_values']:
						option_value_data = self.construct_product_option_value()
						option_value_data['id'] = modifier_value['id']
						option_value_data['code'] = modifier_value['label']
						option_value_data['option_value_code'] = modifier_value['label']
						option_value_data['option_value_name'] = modifier_value['label']
						option_value_data['sort_order'] = modifier_value['sort_order']
						if modifier_value['adjusters']:
							option_value_data['option_value_price'] = modifier_value['adjusters']['price'].get('adjuster_value', 0.0000) if modifier_value['adjusters'].get('price') else 0.0000
							option_value_data['thumb_image']['url'] = modifier_value['adjusters'].get('image_url', '')
						option_data['values'].append(option_value_data)
						if products_ext_data['complex_rules']:
							for rule in products_ext_data['complex_rules']:
								for condition in rule['conditions']:
									if condition['modifier_value_id'] == modifier_value['id']:
										option_value_data['option_value_price'] = (rule['price_adjuster']['adjuster_value'] - product_data['price']) if rule['price_adjuster'] else product_data['price']
				product_data['options'].append(option_data)
		# 	option_datas.append(option_data)
		# childrens = self.convert_option_to_child(option_datas, product_data)
		# for children in childrens:
		# 	product_data['children'].append(children)
		# variant
		if products_ext_data['variants'] and products_ext_data['options']:
			manager_stock = True
			if product['inventory_tracking'] != 'variant':
				manager_stock = False
			for variant in products_ext_data['variants']:

				option_value_id_list = list()
				extra_price = 0
				child = self.construct_product_child()
				child['id'] = variant['id']
				child['name'] = product_data['name']
				child['status'] = True if not variant['purchasing_disabled'] else False
				child['sku'] = variant['sku']
				child['thumb_image']['url'] = variant['image_url']
				child['thumb_image']['path'] = ''
				child['qty'] = variant['inventory_level']
				child['manage_stock'] = manager_stock
				child['price'] = get_value_by_key_in_dict(variant, 'price', product_data['price'])
				child['special_price']['price'] = get_value_by_key_in_dict(variant, 'sale_price', product['sale_price'])
				child['weight'] = get_value_by_key_in_dict(variant, 'weight', 0.0000)
				child['width'] = get_value_by_key_in_dict(variant, 'width', 0.0000)
				child['height'] = get_value_by_key_in_dict(variant, 'height', 0.0000)
				child['length'] = get_value_by_key_in_dict(variant, 'depth', 0.0000)
				child['upc'] = get_value_by_key_in_dict(variant, 'upc', 0.0000)
				child['mpn'] = get_value_by_key_in_dict(variant, 'mpn', 0.0000)
				child['created_at'] = convert_format_time(product_data['created_at'])
				child['updated_at'] = convert_format_time(product_data['updated_at'])
				if variant['option_values'] and to_len(variant['option_values']) > 0:
					for option_variant in variant['option_values']:
						option = get_row_from_list_by_field(products_ext_data['options'], 'id', option_variant['option_id'])
						if option:
							if option['type'] in ['text', 'multi_line_text']:
								conf_type = self.OPTION_TEXT
							elif option['type'] == 'file':
								conf_type = self.OPTION_FILE
							elif option['type'] == 'checkbox':
								conf_type = self.OPTION_CHECKBOX
							else:
								conf_type = option.get('type')
							if not conf_type:
								conf_type = self.OPTION_SELECT
							variant_attr = self.construct_product_child_attribute()
							variant_attr['option_id'] = option_variant['option_id']
							variant_attr['option_code'] = option['name']
							variant_attr['option_code_save'] = option['name']
							variant_attr['option_name'] = option['display_name']
							variant_attr['option_type'] = conf_type
							if option['option_values']:
								option_value = get_row_from_list_by_field(option['option_values'], 'id', option_variant['id'])
								if option_value:
									variant_attr['option_value_id'] = option_variant['id']
									option_value_id_list.append(option_variant['id'])
									variant_attr['option_value_name'] = option_value['label']
									variant_attr['option_value_code'] = option_value['label']
									variant_attr['option_value_code_save'] = option_value['label']
									if conf_type == 'swatch':
										variant_attr['option_value_sort_order'] = option_value['sort_order']
										if option_value.get('value_data'):
											variant_attr['option_value_value_data'] = option_value['value_data']
								else:
									option_value = get_row_from_list_by_field(variant['option_values'], 'id', option_variant['id'])
									if option_value:
										variant_attr['option_value_name'] = option_value['label']
										variant_attr['option_value_code'] = option_value['label']
										variant_attr['option_value_code_save'] = option_value['label']
							child['attributes'].append(variant_attr)
				if products_ext_data['complex_rules']:
					for rule in products_ext_data['complex_rules']:
						tmp = 1
						for condition in rule['conditions']:
							if condition['modifier_value_id'] not in option_value_id_list:
								tmp = 0
								break
						if tmp == 1:
							child['price'] = rule['price_adjuster']['adjuster_value'] + child['price']
				product_data['children'].append(child)
				product_data['type'] = self.PRODUCT_CONFIG
				if products_ext_data.get('options'):
					product_data['options_src'] = products_ext_data.get('options')

		detect_seo = self.detect_seo()
		product_data['seo'] = getattr(self, 'products_' + detect_seo)(product, products_ext)
		return response_success(product_data)


	def get_product_id_import(self, convert, product, products_ext):
		return product['id']


	def check_product_import(self, convert, product, products_ext):
		product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
		if product_id:
		# self.log(convert, 'pro_convert')
		# self.log(products_ext, 'pro_convert')
			if convert['children'] and convert['options_src']:
				# options = convert['children'][0].get('attributes')
				# if options:
				# 	option_map_dic = dict()
				# 	check = None
				# 	for op in options:
				# 		option_map_dic[op.get('option_name')] = op.get('option_type')
				# 		if op.get('option_type') == 'swatch':
							# check = op.get('option_name')
				# 	pro_option_tar_api = self.api_v3('/catalog/products/' + to_str(product_id) + '/options')
				# 	# if pro_option_tar_api:
				# 	# 	pro_option_tar_data = json_decode(pro_option_tar_api).get('data')
				# 	# 	if pro_option_tar_data:
				# 	# 		for pro_op in pro_option_tar_data:
				# 	# 			if check and pro_op.get('display_name') in option_map_dic.keys():
				# 	# 				update_option = {
				# 	# 					"id": pro_op['id'],
				# 	# 					"product_id": product_id,
				# 	# 					"type": option_map_dic[pro_op['display_name']],
				# 	# 				}
				# 	# 				self.log(f"{convert['id']} | {update_option}", 'update_option')
				# 	# 				self.api_v3('/catalog/products/' + to_str(product_id) + '/options/' + to_str(pro_op['id']), update_option, 'put')

				options = convert['options_src']
				if options:
					option_map_dic = dict()
					check = None
					option_values_swatch = None
					for op in options:
						# option_map_dic[op.get('option_name')] = op.get('option_type')
						if op.get('type') == 'swatch':
							check = op.get('display_name')
							option_values_swatch = op.get('option_values')
					if not option_values_swatch:
						return True
					self.log(f"{convert['id']} | {product_id} | {option_values_swatch}", 'option_values_swatch')
					pro_option_tar_api = self.api_v3('/catalog/products/' + to_str(product_id) + '/options')
					if pro_option_tar_api:
						pro_option_tar_data = json_decode(pro_option_tar_api).get('data')
						if pro_option_tar_data:
							for pro_op in pro_option_tar_data:
								list_option_values = list()
								if check and pro_op.get('display_name') == check:
									option_id = pro_op.get('id')
									if option_id:
										pro_option_detail_tar_api = self.api_v3('/catalog/products/' + to_str(product_id) + '/options/' + to_str(option_id))
										if pro_option_detail_tar_api:
											pro_option_detail_tar_api_data = json_decode(pro_option_detail_tar_api).get('data')
											option_values_data = pro_option_detail_tar_api_data.get('option_values')
										pro_option_detail_tar_api_data['type'] = 'swatch'
										if not option_values_data:
											continue
										
										for index, op_val in enumerate(option_values_data):
											option_value_data_src = list(filter(lambda x: x['label'] == op_val.get('label'), option_values_swatch))[0]
											op_val_id = option_value_data_src.get('id')
											update_option_value = {
												"id": op_val['id'],
												"sort_order": op_val.get('sort_order'),
												"label": option_value_data_src.get('label'),
												"is_default": option_value_data_src.get('is_default'),
												"value_data": dict()
											}

											if option_value_data_src.get('value_data'):
												image_url = option_value_data_src.get('value_data').get('image_url')
												if not image_url:
													continue
												image_url_tar = self.insert_image_desc(image_url)
												if not image_url_tar:
													update_option_value['value_data'] = None
												else:
													update_option_value['value_data']['image_url'] = image_url_tar
											list_option_values.append(update_option_value)
										pro_option_detail_tar_api_data['option_values'] = list_option_values
											
										self.api_v3('/catalog/products/' + to_str(product_id) + '/options/' + to_str(pro_op['id']), pro_option_detail_tar_api_data, 'put')
										self.log(f"{convert['id']} | {product_id} | {pro_option_detail_tar_api_data}", 'option_update_data')
										self.log(f"{convert['id']} | {product_id}", 'option_update')

												# self.log(f"{convert['id']} | {update_option}", "")
												# self.api_v3('/catalog/products/' + to_str(product_id) + '/options/' + to_str(option_id), update_option_value, 'put')
										# self.log(f"{convert['id']} | {update_option}", 'update_option')
										# self.api_v3('/catalog/products/' + to_str(product_id) + '/options/' + to_str(pro_op['id']), update_option, 'put')

				# option_list = self.convert_child_to_option(convert['children'])
				# if not option_list:
				# 	return response_error('Cannot convert option')
				# for option in option_list:
				# 	option_data = {
				# 		'product_id': product_id,
				# 		'type': 'dropdown',
				# 		'option_values': list()
				# 	}
				# 	for k, option_value in enumerate(option['values']):
				# 		option_value_data = {
				# 			'label': option_value['option_value_name'],
				# 			'sort_order': k,
				# 			'is_default': True if option_value.get('is_default') else False
				# 		}
				# 		option_data['option_values'].append(option_value_data)
				# 	response = self.api_v3('/catalog/products/' + to_str(product_id) + '/options', option_data, 'Post')
				# 	response = json_decode(response)
				# 	if response and response.get('data'):
				# 		option_code = (option['option_code'] if option['option_code'] else self.convert_attribute_code(option['option_name'])) + '-pro-' + to_str(product_id)
				# 		self.insert_map(self.TYPE_ATTR, option['id'], response['data']['id'], option_code)
				# 		for k, option_value in enumerate(option['values']):
				# 			option_value_code = (option_value['option_value_code'] if option_value['option_value_code'] else self.convert_attribute_code(option_value['option_value_name'])) + '-pro-' + to_str(product_id)
				# 			option_value_id = get_row_value_from_list_by_field(response['data']['option_values'], 'sort_order', k, 'id')
				# 			if option_value_id:
				# 				self.insert_map(self.TYPE_ATTR_VALUE, option_value['id'], option_value_id, option_value_code)
				# 	else:
				# 		self.log(response.get('title'), 'option_error')

				# for children in convert['children']:
				# 	children_sku = children['sku']
				# 	if not children_sku:
				# 		children_sku = self.convert_attribute_code(self.strip_html_tag(children['name'], True))
				# 	if not children_sku:
				# 		children_sku = to_int(time.time())

				# 	upc_data = get_value_by_key_in_dict(children, 'upc', get_value_by_key_in_dict(children, 'barcode', ''))
				# 	if get_value_by_key_in_dict(children, 'ean', '') and not upc_data:
				# 		upc_data = get_value_by_key_in_dict(children, 'ean', '')
				# 	elif get_value_by_key_in_dict(children, 'ean', '') and upc_data:
				# 		upc_data = upc_data + "/" + get_value_by_key_in_dict(children, 'ean', '')
				# 	child_data = {
				# 		'price': to_decimal(children['price']) if children['price'] and to_decimal(children['price']) > 0.000 else 0,
				# 		'weight': to_decimal(children['weight']) if children['weight'] and to_decimal(children['weight']) > 0 else 0,
				# 		'width': to_decimal(children['width']),
				# 		'height': to_decimal(children['height']),
				# 		'depth': to_decimal(children['length']),
				# 		'purchasing_disabled': True if not children['status'] else False,
				# 		'upc': upc_data,
				# 		'inventory_level': to_int(to_decimal(children['qty'])) if to_decimal(children['qty']) > 0 else 0,
				# 		'product_id': product_id,
				# 		'sku': children_sku,
				# 		'option_values': list()
				# 	}
				# 	if children['special_price']['price'] and (self.to_timestamp(children['special_price']['end_date']) > time.time() or (children['special_price']['end_date'] == '0000-00-00' or children['special_price']['end_date'] == '0000-00-00 00:00:00') or children['special_price']['end_date'] == '' or children['special_price']['end_date'] == None):
				# 		child_data['sale_price'] = to_decimal(children['special_price']['price'])
				# 	for attr in children['attributes']:
				# 		attr_code = (attr['option_code'] if attr['option_code'] else self.convert_attribute_code(attr['option_name'])) + '-pro-' + to_str(product_id)
				# 		attr_id = self.get_map_field_by_src(self.TYPE_ATTR, attr['option_id'], attr_code)
				# 		if not attr_id:
				# 			attr_id = self.get_map_field_by_src(self.TYPE_ATTR, None, attr_code)
				# 		attr_value_code = (attr['option_value_code'] if attr['option_value_code'] else self.convert_attribute_code(attr['option_value_name'])) + '-pro-' + to_str(product_id)
				# 		attr_value_id = self.get_map_field_by_src(self.TYPE_ATTR_VALUE, attr['option_value_id'], attr_value_code)
				# 		if not attr_value_id:
				# 			attr_value_id = self.get_map_field_by_src(self.TYPE_ATTR_VALUE, None, attr_value_code)
				# 		if not attr_id or not attr_value_id:
				# 			continue
				# 		else:
				# 			option_value_data = {
				# 				'id': attr_value_id,
				# 				'option_id': attr_id
				# 			}
				# 			child_data['option_values'].append(option_value_data)
				# 	if not child_data['option_values'] or to_len(child_data['option_values']) == 0:
				# 		continue
				# 	response_child = self.api_v3('/catalog/products/' + to_str(product_id) + '/variants', child_data, 'Post')
				# 	response_child = json_decode(response_child)
				# 	if response_child and response_child.get('data'):
				# 		self.insert_map(self.TYPE_CHILD, children['id'], response_child['data']['id'], children['code'])
				# 		if response_child['data']['id'] and children['thumb_image']['url']:
				# 			data_img = {
				# 				"image_url": children['thumb_image']['url']
				# 			}
				# 			self.api_v3(f"catalog/products/{product_id}/variants/{response_child['data']['id']}/image", data_img, 'post')
				# 	else:
				# 		self.log(response_child.get('title'), 'children_error')

		return True #self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])


	def update_latest_data_product(self, product_id, convert, product, products_ext):
		product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
		if not product_id:
			return response_error(to_str(convert['id']) + ' not in map')
		product_data = dict()
		product_data['status_id'] = 10
		categories = list()
		if convert['categories']:
			for category in convert['categories']:
				category_id = self.get_map_field_by_src(self.TYPE_CATEGORY, category['id'], category['code'])
				if category_id:
					categories.append(category_id)
		# if convert['children']:
		# 	products = self.api_v3('/catalog/products.json?min_id=' + to_str(product_id))
		# 	if not products:
		# 		return response_error(self.console_error("Could not get Product data from Bigcommerce"))
		# 	products_data = json.loads(products)
		# 	for product in products_data:
		# 		if 'resource' in product['skus'] and product['skus']['resource']:
		# 			api_skus = self.api_v3(product['skus']['resource'] + '.json')
		# 			if api_skus:
		# 				sku_data = json.loads(api_skus)
		# 				for sku in sku_data:
		# 					for children in convert['children']:
		# 						if sku['sku']==children['sku']:
		# 							product_data = {
		# 								"inventory_level": children['qty'],
		# 							}
		# 							self.api_v3('/catalog/products/' + to_str(sku['product_id']) + '/skus/' + to_str(sku['id']), product_data, 'PUT')
		product_data = {
			'name': self.strip_html_tag(convert['name']),
			'sku': convert['sku'],
			'price': convert['price'] if convert['price'] else 0,
			'sale_price': to_decimal(convert['special_price']['price']),
			'inventory_level': to_int(to_decimal(convert['qty'])) if to_decimal(convert['qty']) > 0 else 0,
			'is_visible': True if convert['status'] else False,
			'availability': 'available' if convert['status'] else 'disabled',
			'inventory_tracking': 'simple' if 'manage_stock' in convert and convert['manage_stock'] else 'none',
			'categories': categories,
		}
		if 'seo' in convert and self._notice['config']['seo']:
			default_url = get_row_value_from_list_by_field(convert['seo'], 'default', True, 'request_path')
			if default_url:
				default_url = to_str(default_url).replace(' ', '-')
				default_url = to_str(default_url).replace('--', '-').replace('%', '')
				product_data['custom_url'] = {
					'url': '/' + default_url.lstrip('/'),
					'is_customized': True,
				}
			else:
				for seo_url in convert['seo']:
					if seo_url['request_path']:
						product_data['custom_url'] = {
							'url': '/' + to_str(re.sub(r"\s+", "", seo_url['request_path'])).strip('/').replace(' ', '-').replace('--', '-').replace(' -', '-'),
							'is_customized': True,
						}
						break
		self.api_v3('/catalog/products/' + to_str(product_id), product_data, 'PUT')
		return response_success(product_id)


	def channel_sync_inventory(self, product_id, convert, product, products_ext, settings = {}):
		price_setting = settings.get('price')
		qty_setting = settings.get('qty')
		product_data = dict()
		if price_setting:
			product_data.update({
				'price': convert['price'] if convert['price'] else 0,
				'sale_price': to_decimal(convert['special_price']['price']),
			})
		if qty_setting:
			product_data.update({
				'inventory_level': to_int(to_decimal(convert['qty'])) if to_decimal(convert['qty']) > 0 else 0,
				'inventory_tracking': 'simple' if 'manage_stock' in convert and convert['manage_stock'] else 'none',
			})
		if product_data:
			self.api_v3('/catalog/products/' + to_str(product_id), product_data, 'PUT')
		return response_success()


	def update_product_after_demo(self, product_id, convert, product, products_ext):
		categories = list()
		if convert['categories']:
			for category in convert['categories']:
				category_id = self.get_map_field_by_src(self.TYPE_CATEGORY, category['id'], category['code'])
				if category_id:
					categories.append(category_id)

		if not categories:
			category_id = self.get_map_field_by_src(self.TYPE_CATEGORY, 23031991)
			if not category_id:
				root_cate = False
				cat_lit_id = False
				cat_lit = self.api_v3("/catalog/categories?name=LitExtension")
				if cat_lit:
					cat_lit_decode = json.loads(cat_lit)
					if cat_lit_decode and cat_lit_decode.get('data') and isinstance(cat_lit_decode['data'], list):
						cat_lit_id = cat_lit_decode['data'][0].get('id')
						if cat_lit_id:
							self.insert_map(self.TYPE_CATEGORY, 7101994, cat_lit_id)
				if not cat_lit_id:
					cat_data = {
						'name': "LitExtension",
						'parent_id': 0,
						'description': 'This category is created for the product which was in an empty category',
						'is_visible': False
					}
					response_cat = self.api_v3('/catalog/categories', cat_data, 'Post')
					response_cat = json_decode(response_cat)
					if response_cat and response_cat.get('data'):
						response_cat_data = response_cat['data']
						if 'id' in response_cat_data:
							root_cate = True
							self.insert_map(self.TYPE_CATEGORY, 7101994, response_cat_data['id'])
							cat_lit_id = response_cat_data['id']

				category_id = cat_lit_id

			if category_id:
				categories.append(category_id)
		manufacturer_id = False
		if convert['manufacturer']['id'] or convert['manufacturer']['code']:
			manufacturer_id = self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['manufacturer']['id'], convert['manufacturer']['code'])
			if not manufacturer_id:
				manufacturer_id = self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['manufacturer']['id'], None)
		elif convert['manufacturer']['name']:
			manufacturer_id = self.get_map_field_by_src(self.TYPE_MANUFACTURER, None, convert['manufacturer']['name'])
			if not manufacturer_id:
				man_data = {
					'name': convert['manufacturer']['name']
				}
				manufacturer = self.api_v3('/catalog/brands', man_data, 'Post')
				manufacturer = json_decode(manufacturer)
				if manufacturer and manufacturer.get('data'):
					manufacturer_data = manufacturer['data']
					self.insert_map(self.TYPE_MANUFACTURER, None, manufacturer_data['id'], convert['manufacturer']['name'])
					manufacturer_id = manufacturer_data['id']
		product_data = {
			'categories': categories,
		}
		if manufacturer_id:
			product_data['brand_id'] = manufacturer_id
		self.api('/products/' + to_str(product_id), product_data, 'PUT')
		return response_success()


	def router_product_import(self, convert, product, products_ext):
		return response_success('product_import')


	def before_product_import(self, convert, product, products_ext):
		return response_success()


	def product_import(self, convert, product, products_ext):
		categories = list()
		if convert['categories']:
			for category in convert['categories']:
				category_id = self.get_map_field_by_src(self.TYPE_CATEGORY, category['id'], category['code'])
				if category_id:
					categories.append(category_id)

		manufacturer_id = False
		if convert['manufacturer']['id'] or convert['manufacturer']['code']:
			manufacturer_id = self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['manufacturer']['id'], convert['manufacturer']['code'])
			if not manufacturer_id:
				manufacturer_id = self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['manufacturer']['id'], None)
		elif convert['manufacturer']['name']:
			manufacturer_id = self.get_map_field_by_src(self.TYPE_MANUFACTURER, None, convert['manufacturer']['name'])
			if not manufacturer_id:
				man_data = {
					'name': convert['manufacturer']['name']
				}
				manufacturer = self.api_v3('/catalog/brands', man_data, 'Post')
				manufacturer = json_decode(manufacturer)
				if manufacturer and manufacturer.get('data'):
					manufacturer_data = manufacturer['data']
					self.insert_map(self.TYPE_MANUFACTURER, None, manufacturer_data['id'], convert['manufacturer']['name'])
					manufacturer_id = manufacturer_data['id']

		upc_data = get_value_by_key_in_dict(convert, 'upc', get_value_by_key_in_dict(convert, 'barcode', ''))
		if get_value_by_key_in_dict(convert, 'ean', '') and not upc_data:
			upc_data = get_value_by_key_in_dict(convert, 'ean', '')
		elif get_value_by_key_in_dict(convert, 'ean', '') and upc_data:
			upc_data = upc_data + "/" + get_value_by_key_in_dict(convert, 'ean', '')

		product_sku = convert['sku']
		if not product_sku:
			product_sku = self.convert_attribute_code(self.strip_html_tag(convert['name'], True))
		if not product_sku:
			product_sku = to_int(time.time())

		tracking = 'product' if 'manage_stock' in convert and convert['manage_stock'] else 'none'
		if convert['children']:
			tracking = 'variant'

		product_data = {
			'name': self.strip_html_tag(convert['name']),
			'type': 'physical',
			'sku': product_sku,
			'description': self.convert_link_image_description(convert['description']),
			'price': to_decimal(convert['price']) if convert['price'] and to_decimal(convert['price']) > 0.000 else 0,
			'categories': categories,
			'availability': 'available' if convert['status'] else 'disabled',
			'weight': to_decimal(convert['weight']) if convert['weight'] and to_decimal(convert['weight']) > 0 else 0,
			'width': to_decimal(convert['width']),
			'height': to_decimal(convert['height']),
			'depth': to_decimal(convert['length']),
			'inventory_tracking': tracking,
			'is_visible': True if convert['status'] else False,
			'inventory_level': to_int(to_decimal(convert['qty'])) if to_decimal(convert['qty']) > 0 else 0,
			'upc': upc_data,
			'meta_keywords': get_value_by_key_in_dict(convert, 'meta_keyword', '').split(','),
			'meta_description': get_value_by_key_in_dict(convert, 'meta_description', ''),
			'page_title': to_str(get_value_by_key_in_dict(convert, 'meta_title', ''))[:255].replace('|', ' ').replace('  ', ' '),
			'search_keywords': get_value_by_key_in_dict(convert, 'meta_keyword', ''),
		}

		if convert['special_price']['price'] and (self.to_timestamp(convert['special_price']['end_date']) > time.time() or (convert['special_price']['end_date'] == '0000-00-00' or convert['special_price']['end_date'] == '0000-00-00 00:00:00') or convert['special_price']['end_date'] == '' or convert['special_price']['end_date'] == None):
			product_data['sale_price'] = to_decimal(convert['special_price']['price'])
		if convert.get('sort_order'):
			product_data['sort_order'] = convert.get('sort_order')
		product_data['description'] = html.unescape(convert['short_description']) + '<br>' + html.unescape(product_data['description']) if product_data['description'] else ''
		if manufacturer_id:
			product_data['brand_id'] = manufacturer_id

		lit_relate = list()
		if convert['relate']['children']:
			for relate_id in convert['relate']['children']:
				relate_desc_id = self.get_map_field_by_src(self.TYPE_PRODUCT, relate_id['id'])
				if relate_desc_id:
					lit_relate.append(to_int(relate_desc_id))
			if lit_relate:
				product_data['related_products'] = lit_relate

		if self._notice['config']['seo']:
			if 'seo' in convert and convert['seo']:
				default_url = get_row_value_from_list_by_field(convert['seo'], 'category_id', None, 'request_path')
				default_url = to_str(default_url).replace('--', '-')
				default_url = re.sub(r"\s+", "", default_url)
				default_url = re.sub(r"[^a-zA-Z0-9\.\-\_\/]", '', default_url)
				if default_url:
					product_data['custom_url'] = {
						'url': '/' + default_url.lstrip('/'),
						'is_customized': True,
					}
				else:
					for seo_url in convert['seo']:
						if seo_url['request_path']:
							request_path = re.sub(r"[^a-zA-Z0-9\.\-\_\/]", '', seo_url['request_path'])
							product_data['custom_url'] = {
								'url': '/' + to_str(re.sub(r"\s+", "", request_path)).strip('/').replace(' ', '-').replace('--', '-').replace(' -', '-'),
								'is_customized': True,
							}
							break

		response = self.api_v3('/catalog/products', product_data, 'Post')
		response_data = json_decode(response)
		while response_data and 'status' in response_data and to_str(response_data['status']) == '409' and response_data['title'].find("The product name is a duplicate") != -1:
			new_name = self.strip_html_tag(product_data['name']) + '-' + to_str(to_int(time.time()))
			product_data['name'] = new_name
			response = self.api_v3('/catalog/products', product_data, 'Post')
			response_data = json_decode(response)
		while response_data and 'status' in response_data and to_str(response_data['status']) == '409' and response_data['title'].find("The product sku is a duplicate") != -1:
			new_sku = to_str(product_data['sku']) + '-' + to_str(to_int(time.time()))
			product_data['sku'] = new_sku
			response = self.api_v3('/catalog/products', product_data, 'Post')
			response_data = json_decode(response)
		if 'status' in response_data and to_str(response_data['status']) in ['400', '422']:
			return response_error('Product ' + to_str(convert['id']) + 'import fail. Error: ' + to_str(response_data['title']))
		if not response_data or 'data' not in response_data or to_len(response_data['data']) == 0:
			return response_error('Product ' + to_str(convert['id']) + ' import fail.' + to_str(response_data['title']))

		self.insert_map(self.TYPE_PRODUCT, convert['id'], response_data['data']['id'], convert['code'], product_data['sku'], json_encode({'relate_prd': lit_relate, 'qty': convert['qty']}))
		return response_success(response_data['data']['id'])


	def after_product_import(self, product_id, convert, product, products_ext):
		if self._notice['config']['seo_301'] or self._notice['config']['seo']:
			if 'seo' in convert and convert['seo']:
				# get site id
				if 'site_id' not in self._notice:
					site_data = json_decode(self.api_v3('sites', None, 'get'))
					if site_data.get('data'):
						site_id = site_data['data'][0]['id']
						self._notice['site_id'] = site_id

				for seo_url in convert['seo']:
					seo_data = [
						{
							"from_path": '/' + to_str(seo_url['request_path']).lstrip('/'),
							"site_id": self._notice['site_id'] if 'site_id' in self._notice else 1000,
							"to": {
								"type": "product",
								"entity_id": product_id
							}
						}
					]
					self.api_v3('storefront/redirects', seo_data, 'put')

		if convert['relate']['parent']:
			for relate_id2 in convert['relate']['parent']:
				relate_desc = self.select_map(self._migration_id, self.TYPE_PRODUCT, relate_id2['id'])
				if relate_desc:
					relate_parent = list()
					value = json_decode(relate_desc['value'])
					if value and value['relate_prd']:
						relate_parent = value['relate_prd']
					qty = value['qty'] if value and value['qty'] else ''
					relate_parent.append(to_int(product_id))
					data_update = {
						'related_products': relate_parent
					}
					self.update_map(self.TYPE_PRODUCT, relate_id2['id'], None, None, None, json_encode({'relate_prd': relate_parent, 'qty': qty}))
					# self.api('/products/' + to_str(relate_desc['id_desc']), data_update, 'PUT')
					self.api_v3('/catalog/products/' + to_str(relate_desc['id_desc']), data_update, 'PUT')

		if convert['short_description']:
			attr_data = {
				'name': 'Short Description',
				'value': to_str(convert['short_description'])[0:250]
			}
			self.api_v3('/catalog/products/' + to_str(product_id) + '/custom-fields', attr_data, 'Post')

		if convert['attributes']:
			for attr in convert['attributes']:
				if not attr['option_value_name'] or attr['option_name'] == 'Description' or attr['option_name'] == 'Short Description':
					continue
				attr_data = {
					'name': attr['option_name'],
					'value': attr['option_value_name'][0:250]
				}
				self.api_v3('/catalog/products/' + to_str(product_id) + '/custom-fields', attr_data, 'Post')

		if convert['thumb_image']:
			image_process = self.process_image_before_import(convert['thumb_image']['url'], convert['thumb_image']['path'])
			if image_process['url']:
				img_data = dict()
				img_data['image_url'] = image_process['url'].replace('https', 'http')
				img_data['is_thumbnail'] = True
				img_data['description'] = convert['thumb_image']['label'] if convert['thumb_image']['label'] else ''
				a = self.api_v3('/catalog/products/' + to_str(product_id) + '/images', img_data, 'Post')

		if convert['images']:
			for image in convert['images']:
				image_process = self.process_image_before_import(image['url'], image['path'])
				if image_process['url']:
					img_data = dict()
					img_data['image_url'] = image_process['url'].replace('https', 'http')
					img_data['is_thumbnail'] = False
					img_data['description'] = image['label'] if image['label'] else ''
					a = self.api_v3('/catalog/products/' + to_str(product_id) + '/images', img_data, 'Post')

		if convert['tier_prices']:
			list_qty = list()
			tier_prices = dict()
			for tier_price in convert['tier_prices']:
				qty = to_int(tier_price['qty'])
				if qty not in list_qty:
					list_qty.append(qty)
					tier_prices[qty] = tier_price
			list_qty.sort()
			bulk_prices = list()
			for index, qty in enumerate(list_qty):
				if index < to_len(to_str(qty)) - 1:
					max_qty = list_qty[index + 1] - 1 if index + 1 < to_len(list_qty) else pow(10, to_len(to_str(qty))) - 1
				else:
					max_qty = pow(10, to_len(to_str(qty))) - 1
				bulk_price = {
					"quantity_min": to_int(qty),
					"quantity_max": max_qty,
					"type": "percent" if convert['tier_prices'][index].get('price_type') == 'percent' else 'fixed',
					"amount": to_decimal(convert['tier_prices'][index]['price'])
				}
				bulk_prices.append(bulk_price)
			self.api_v3('/catalog/products/' + to_str(product_id) + '/bulk-pricing-rules', bulk_prices, 'Post')

		if convert['options']:
			for option in convert['options']:
				if option['option_type'] == self.OPTION_CHECKBOX:
					option_type = 'checkbox'
				elif option['option_type'] == self.OPTION_FILE:
					option_type = 'file'
				elif option['option_type'] == self.OPTION_TEXT:
					option_type = 'text'
				elif option['option_type'] == 'textarea':
					option_type = 'multi_line_text'
				elif option['option_type'] == self.OPTION_RADIO:
					option_type = 'radio_buttons'
				else:
					option_type = 'dropdown'
				option_data = {
					"type": option_type,
					"required": option['required'],
					"sort_order": option['sort_order'] if option.get('sort_order') else 0,
					"config": {},
					"display_name": option['option_name'],
					'option_values': list()
				}
				for k, value in enumerate(option['values']):
					image_process = dict()
					if value['thumb_image']['url'] or value['thumb_image']['path']:
						image_process = self.process_image_before_import(value['thumb_image']['url'], value['thumb_image']['path'])
					value_data = {
						'is_default': True if value.get('is_default') else False,
						'label': value['option_value_name'],
						'sort_order': k,
						'adjusters': {
							'image_url': image_process['url'] if image_process and image_process.get('url') else '',
							'price': None if not value['option_value_price'] else {
								'adjuster': 'relative',
								'adjuster_value': to_decimal(value['option_value_price']),
							},
							'purchasing_disabled': {
								'message': '',
								'status': False
							},
							'weight': None
						}
					}
					option_data['option_values'].append(value_data)
				response_option = self.api_v3('/catalog/products/' + to_str(product_id) + '/modifiers', option_data, 'Post')
				response_option = json_decode(response_option)
				if response_option and response_option.get('data'):
					option_code = (option['option_code'] if option['option_code'] else self.convert_attribute_code(option['option_name'])) + '-pro-' + to_str(product_id)
					self.insert_map(self.TYPE_OPTION, option['id'], response_option['data']['id'], option_code)
					for k, option_value in enumerate(option['values']):
						option_value_code = (option_value['option_value_code'] if option_value['option_value_code'] else self.convert_attribute_code(option_value['option_value_name'])) + '-pro-' + to_str(product_id)
						option_value_id = get_row_value_from_list_by_field(response_option['data']['option_values'], 'sort_order', k, 'id')
						if option_value_id:
							self.insert_map(self.TYPE_OPTION_VALUE, option_value['id'], option_value_id, option_value_code)
				else:
					self.log(response_option.get('title'), 'option_error')

		if convert['children']:
			option_list = self.convert_child_to_option(convert['children'])
			if not option_list:
				return response_error('Cannot convert option')
			for option in option_list:
				option_data = {
					'product_id': product_id,
					'display_name': option['option_name'],
					'type': 'dropdown',
					'option_values': list()
				}
				for k, option_value in enumerate(option['values']):
					option_value_data = {
						'label': option_value['option_value_name'],
						'sort_order': k,
						'is_default': True if option_value.get('is_default') else False
					}
					option_data['option_values'].append(option_value_data)
				response = self.api_v3('/catalog/products/' + to_str(product_id) + '/options', option_data, 'Post')
				response = json_decode(response)
				if response and response.get('data'):
					option_code = (option['option_code'] if option['option_code'] else self.convert_attribute_code(option['option_name'])) + '-pro-' + to_str(product_id)
					self.insert_map(self.TYPE_ATTR, option['id'], response['data']['id'], option_code)
					for k, option_value in enumerate(option['values']):
						option_value_code = (option_value['option_value_code'] if option_value['option_value_code'] else self.convert_attribute_code(option_value['option_value_name'])) + '-pro-' + to_str(product_id)
						option_value_id = get_row_value_from_list_by_field(response['data']['option_values'], 'sort_order', k, 'id')
						if option_value_id:
							self.insert_map(self.TYPE_ATTR_VALUE, option_value['id'], option_value_id, option_value_code)
				else:
					self.log(response.get('title'), 'option_error')

			for children in convert['children']:
				children_sku = children['sku']
				if not children_sku:
					children_sku = self.convert_attribute_code(self.strip_html_tag(children['name'], True))
				if not children_sku:
					children_sku = to_int(time.time())

				upc_data = get_value_by_key_in_dict(children, 'upc', get_value_by_key_in_dict(children, 'barcode', ''))
				if get_value_by_key_in_dict(children, 'ean', '') and not upc_data:
					upc_data = get_value_by_key_in_dict(children, 'ean', '')
				elif get_value_by_key_in_dict(children, 'ean', '') and upc_data:
					upc_data = upc_data + "/" + get_value_by_key_in_dict(children, 'ean', '')
				child_data = {
					'price': to_decimal(children['price']) if children['price'] and to_decimal(children['price']) > 0.000 else 0,
					'weight': to_decimal(children['weight']) if children['weight'] and to_decimal(children['weight']) > 0 else 0,
					'width': to_decimal(children['width']),
					'height': to_decimal(children['height']),
					'depth': to_decimal(children['length']),
					'purchasing_disabled': True if not children['status'] else False,
					'upc': upc_data,
					'inventory_level': to_int(to_decimal(children['qty'])) if to_decimal(children['qty']) > 0 else 0,
					'product_id': product_id,
					'sku': children_sku,
					'option_values': list()
				}
				if children['special_price']['price'] and (self.to_timestamp(children['special_price']['end_date']) > time.time() or (children['special_price']['end_date'] == '0000-00-00' or children['special_price']['end_date'] == '0000-00-00 00:00:00') or children['special_price']['end_date'] == '' or children['special_price']['end_date'] == None):
					child_data['sale_price'] = to_decimal(children['special_price']['price'])
				for attr in children['attributes']:
					attr_code = (attr['option_code'] if attr['option_code'] else self.convert_attribute_code(attr['option_name'])) + '-pro-' + to_str(product_id)
					attr_id = self.get_map_field_by_src(self.TYPE_ATTR, attr['option_id'], attr_code)
					if not attr_id:
						attr_id = self.get_map_field_by_src(self.TYPE_ATTR, None, attr_code)
					attr_value_code = (attr['option_value_code'] if attr['option_value_code'] else self.convert_attribute_code(attr['option_value_name'])) + '-pro-' + to_str(product_id)
					attr_value_id = self.get_map_field_by_src(self.TYPE_ATTR_VALUE, attr['option_value_id'], attr_value_code)
					if not attr_value_id:
						attr_value_id = self.get_map_field_by_src(self.TYPE_ATTR_VALUE, None, attr_value_code)
					if not attr_id or not attr_value_id:
						continue
					else:
						option_value_data = {
							'id': attr_value_id,
							'option_id': attr_id
						}
						child_data['option_values'].append(option_value_data)
				if not child_data['option_values'] or to_len(child_data['option_values']) == 0:
					continue
				response_child = self.api_v3('/catalog/products/' + to_str(product_id) + '/variants', child_data, 'Post')
				response_child = json_decode(response_child)
				if response_child and response_child.get('data'):
					self.insert_map(self.TYPE_CHILD, children['id'], response_child['data']['id'], children['code'])
					if response_child['data']['id'] and children['thumb_image']['url']:
						data_img = {
							"image_url": children['thumb_image']['url']
						}
						self.api_v3(f"catalog/products/{product_id}/variants/{response_child['data']['id']}/image", data_img, 'post')
				else:
					self.log(response_child.get('title'), 'children_error')

		return response_success()


	def addition_product_import(self, convert, product, products_ext):
		return response_success()


	# TODO: CUSTOMER
	def prepare_customers_import(self):
		return self


	def prepare_customers_export(self):
		return self


	# def get_customers_main_export(self):
	# 	imported = self._notice['process']['customers']['imported']
	# 	limit = self._notice['setting']['customers']
	# 	id_src = to_int(self._notice['process']['customers']['id_src']) + 1
	# 	# page = math.floor(int(imported) / to_int(limit)) + 1
	# 	# customers_api = self.api_v3('/customers?page=' + to_str(page) + '&sort=id&limit=' + to_str(limit) + '&include=addresses')
	# 	# customers = json.loads(customers_api)
	# 	# if not customers_api or not customers or to_str(customers) == '' or not customers.get('data') or to_len(customers['data']) == 0:
	# 	# 	return response_error(self.console_error("Could not get Product data from Bigcommerce"))
	# 	# return response_success(customers['data'])
	# 	customers_api = self.api('/customers.json?min_id=' + to_str(id_src) + '&sort=id&limit=' + to_str(limit))
	# 	if not customers_api:
	# 		return response_error(self.console_error("Could not get data Customer from Bigcommerce"))
	# 	customers = json.loads(customers_api)
	# 	return response_success(customers)
	#
	# def get_customers_ext_export(self, customers):
	# 	return response_success()
	#
	# def convert_customer_export(self, customer, customers_ext):
	# 	customer_data = self.construct_customer()
	# 	customer_data['id'] = customer['id']
	# 	customer_data['group_id'] = customer['customer_group_id']
	# 	customer_data['code'] = customer['email']
	# 	customer_data['email'] = customer['email']
	# 	customer_data['first_name'] = customer['first_name']
	# 	customer_data['last_name'] = customer['last_name']
	# 	customer_data['active'] = True
	# 	customer_data['created_at'] = convert_format_time(customer['date_created'], "%a, %d %b %Y %H:%M:%S %z")
	# 	customer_data['updated_at'] = convert_format_time(customer['date_modified'], "%a, %d %b %Y %H:%M:%S %z")
	# 	customer_data['phone'] = customer['phone']
	# 	# customer_data['is_subscribed'] = customer['accepts_marketing']
	# 	cus_address = customer.get('addresses')
	# 	if cus_address:
	# 		key = 0
	# 		for cus_add in cus_address:
	# 			address_data = self.construct_customer_address()
	# 			address_data['id'] = cus_add['id']
	# 			address_data['first_name'] = cus_add['first_name']
	# 			address_data['last_name'] = cus_add['last_name']
	# 			address_data['address_1'] = cus_add['address1']
	# 			address_data['address_2'] = cus_add['address2']
	# 			address_data['city'] = cus_add['city']
	# 			address_data['postcode'] = cus_add['postal_code']
	# 			address_data['telephone'] = cus_add['phone']
	# 			address_data['company'] = cus_add['company']
	# 			address_data['country']['country_code'] = cus_add['country_code']
	# 			address_data['country']['code'] = cus_add['country_code']
	# 			address_data['country']['name'] = cus_add['country']
	# 			address_data['state']['code'] = self._get_state_code_from_name(cus_add['state_or_province'])
	# 			address_data['state']['state_code'] = self._get_state_code_from_name(cus_add['state_or_province'])
	# 			address_data['state']['name'] = cus_add['state_or_province']
	# 			if key == 0:
	# 				address_data['default']['billing'] = True
	# 				address_data['default']['shipping'] = True
	# 			key += 1
	# 			customer_data['address'].append(address_data)
	#
	# 	return response_success(customer_data)
	#
	# def get_customer_id_import(self, convert, customer, customers_ext):
	# 	return customer['id']

	def check_customer_import(self, convert, customer, customers_ext):
		# self.log(convert, 'cus_convert')
		# self.log(customer, 'cus_convert')
		customer_id = self.get_map_field_by_src(self.TYPE_CUSTOMER, convert['id'], convert['code'])
		if customer_id and convert['group_id']:
			update_customer_group_data = [{
				'id': customer_id,
				'customer_group_id': self.LIST_CUSTOMER_GROUP_MAP[to_int(convert['group_id'])] if self.LIST_CUSTOMER_GROUP_MAP.get(to_int(convert['group_id'])) else None
			}]
			self.api_v3('/customers', update_customer_group_data, 'PUT')
			self.log(f"{convert['id']} | {customer_id} | {update_customer_group_data}", 'cus_update_cus_group')
		return True #if self.get_map_field_by_src(self.TYPE_CUSTOMER, convert['id'], convert['code']) else False


	def router_customer_import(self, convert, customer, customers_ext):
		return response_success('customer_import')


	def before_customer_import(self, convert, customer, customers_ext):
		return response_success()


	def customer_import(self, convert, customer, customers_ext):
		first_name = convert['first_name']
		last_name = convert['last_name']
		email = convert['email']
		phone = convert['phone']
		if not phone:
			phone = convert['address'][0]['telephone'] if convert['address'] else '000000000'
		if not first_name and not last_name and not email:
			response_error(self.warning_import_entity('Customer', convert['id'], convert['code'], " missing data"))
		email_exp = to_str(email).split('@')
		if not first_name:
			if last_name:
				first_name = last_name
			else:
				first_name = email_exp[0]
		if not last_name:
			if first_name:
				last_name = first_name
			else:
				last_name = email_exp[0]
		cus_data = [
			{
				"first_name": first_name[:100],
				"last_name": last_name[:100],
				"email": convert['email'] if convert['email'] else to_str(convert['first_name']).lower().replace(' ', '') + to_str(convert['last_name']).lower().replace(' ', '') + '@gmail.com',
				"phone": phone[:48] if phone else '000000000',
				"company": get_value_by_key_in_dict(convert['address'][0], 'company', '') if convert['address'] and to_len(convert['address']) > 0 else '',
				"accepts_product_review_abandoned_cart_emails": True if convert.get('is_subscribed') else False
			}
		]
		response = self.api_v3('/customers', cus_data, 'Post')
		response = json_decode(response)
		if response.get('title') == 'This email address is already in use by a customer.':
			cus_data = [
				{
					"first_name": first_name,
					"last_name": last_name,
					"phone": to_str(convert['phone'])[:48] if convert['phone'] else '000000000',
				}
			]
			if convert['first_name'] == convert['last_name']:
				cus_data[0]['email'] = to_str(convert['first_name']).lower().replace(' ', '').strip() + '@gmail.com'
			elif convert['first_name'] and convert['last_name']:
				cus_data[0]['email'] = to_str(convert['first_name']).lower().strip() + to_str(convert['last_name']).lower().strip() + '@gmail.com'
			elif convert['first_name'] and not convert['last_name']:
				cus_data[0]['email'] = to_str(convert['first_name']).lower().strip() + '@gmail.com'
			else:
				cus_data[0]['email'] = to_str(convert['last_name']).lower().strip() + '@gmail.com'

			response = self.api_v3('/customers', cus_data, 'Post')
			response = json_decode(response)

		if response.get('title'):
			return response_error(self.warning_import_entity('Customer', convert['id'], convert['code'], response['title'] + ' Reason: ' + to_str(response.get('errors'))))

		if response.get('errors'):
			self.log_primary('customers', response['errors'], convert['id'], convert['code'])
			return response_error(self.warning_import_entity('Customer', convert['id'], convert['code'], response['errors'] + ' Reason: ' + to_str(response.get('errors'))))

		response_data = response['data']
		if response_data and to_len(response_data) > 0 and 'id' in response_data[0]:
			id_desc = response_data[0]['id']
			self.insert_map(self.TYPE_CUSTOMER, convert['id'], id_desc, convert['code'])
			return response_success(id_desc)
		else:
			return response_error(self.warning_import_entity('Customer', convert['id'], convert['code']))


	def after_customer_import(self, customer_id, convert, customer, customers_ext):
		first_name = convert['first_name']
		last_name = convert['last_name']
		email = convert['email']
		if not first_name and not last_name and not email:
			response_error(self.warning_import_entity('Customer', convert['id'], convert['code'], " missing data"))
		email_exp = to_str(email).split('@')
		if not first_name:
			if last_name:
				first_name = last_name
			else:
				first_name = email_exp[0]
		if not last_name:
			if first_name:
				last_name = first_name
			else:
				last_name = email_exp[0]
		address_src = convert['address']
		for address in address_src:
			cus_add = [
				{
					'first_name': address['first_name'] if address['first_name'] else first_name,
					'last_name': address['last_name'] if address['last_name'] else last_name,
					'phone': address['telephone'] if address['telephone'] else '000000000',
					'address1': address['address_1'] if address['address_1'] else 'street 1',
					'address2': address['address_2'] if address['address_2'] else ' ',
					'city': address['city'],
					'company': get_value_by_key_in_dict(address, 'company', ''),
					'address_type': 'residential',
					'customer_id': customer_id,
					'postal_code': get_value_by_key_in_dict(address, 'postcode', '')
				}
			]

			if address['state']['name'] and self.validate_state(address['state']['name']):
				cus_add[0]['state_or_province'] = address['state']['name']
			else:
				cus_add[0]['state_or_province'] = self._get_state_name_from_code(address['state']['state_code'] if address['state']['state_code'] else address['state']['code']) if address['state']['code'] or address['state']['state_code'] else 'Alabama'

			if address['country']['name']:
				if address['country']['name'] == 'Vietnam':
					cus_add[0]['country_code'] = 'VN'
				else:
					cus_add[0]['country_code'] = address['country']['country_code'] if address['country']['country_code'] else address['country']['code']
			else:
				cus_add[0]['country_code'] = self.get_country_code_by_name(address['country']['name'] if address['country']['name'] else '')

			response = self.api_v3('/customers/addresses', cus_add, 'Post')

		return response_success()


	def addition_customer_import(self, convert, customer, customers_ext):
		return response_success()


	# TODO: BLOCK
	def prepare_blogs_import(self):
		return response_success()


	def prepare_blogs_export(self):
		return self


	def get_blogs_main_export(self):
		imported = self._notice['process']['blogs']['imported']
		id_src = to_int(self._notice['process']['blogs']['id_src']) + 1
		limit = self._notice['setting']['blogs']
		page = math.floor(to_decimal(imported) / to_decimal(limit)) + 1
		blog_api = self.api('/blog/posts.json?page=' + to_str(page) + '&sort=id&limit=' + to_str(limit))
		if not blog_api:
			return create_response('pass')
		blog = json.loads(blog_api)
		return response_success(blog)


	def get_blogs_ext_export(self, blocks):
		return response_success()


	def convert_blog_export(self, block, blocks_ext):
		block_data = self.construct_blog_post()
		block_data['id'] = block['id']
		block_data['name'] = block['title']
		block_data['title'] = block['title']
		block_data['description'] = block['body']
		block_data['content'] = self.replace_bigcommerce_url(block['body'])
		block_data['short_description'] = get_value_by_key_in_dict(block, 'summary', ' ')
		block_data['status'] = block['is_published']
		block_data['meta_title'] = block['title']
		block_data['meta_description'] = block['meta_description']
		block_data['meta_keywords'] = block['meta_keywords']
		block_data['url_key'] = to_str(block['url']).replace('/', '')
		block_data['tags'] = ','.join(block['tags']) if block['tags'] else ''
		block_data['created_at'] = convert_format_time(block['published_date']['date'], "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S")
		block_data['updated_at'] = convert_format_time(block['published_date']['date'], "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S")
		if block['thumbnail_path']:
			block_data['thumb_image']['url'] = self._notice['src']['cart_url']
			block_data['thumb_image']['path'] = block['thumbnail_path']
		return response_success(block_data)


	def get_blog_id_import(self, convert, block, blocks_ext):
		return block['id']


	def check_blog_import(self, convert, block, blocks_ext):
		return True if self.get_map_field_by_src(self.TYPE_BLOG, convert['id']) else False


	def router_blog_import(self, convert, block, blocks_ext):
		return response_success('block_import')


	def before_blog_import(self, convert, block, blocks_ext):
		return response_success()


	def blog_import(self, convert, block, blocks_ext):

		# get product blog
		product_id = self.get_id_product_blog()
		body = get_value_by_key_in_dict(convert, 'content', ' ')
		body = self.convert_link_image_description(body)
		blog_data = {
			# 'id': self.strip_html_tag(get_value_by_key_in_dict(convert, 'id', '')),
			'title': self.strip_html_tag(get_value_by_key_in_dict(convert, 'title', '')),
			'body': body,
			'meta_keywords': get_value_by_key_in_dict(convert, 'meta_keywords', ''),
			'meta_description': get_value_by_key_in_dict(convert, 'meta_description', ''),
			'is_published': convert['status'],
			'url': '/' + get_value_by_key_in_dict(convert, 'url_key', '0'),
			# 'tags': get_value_by_key_in_dict(convert, 'tags', ' '),
		}
		if convert.get('tags'):
			blog_data['tags'] = convert['tags'].split(',')
		if convert.get('created_at'):
			blog_data['published_date'] = convert_format_time(convert['created_at'], '%Y-%m-%d %H:%M:%S', "%a, %d %b %Y %H:%M:%S %z") + '+0000'
		blog_result = self.api_post('/blog/posts', blog_data)
		if not blog_result or blog_result.get('result') == 'error' or not blog_result.get('data') or not blog_result['data'].get('id'):
			return response_error(convert['id'] + ' import false: ' + blog_result.get('msg'))
		self.insert_map(self.TYPE_BLOG, convert['id'], blog_result['data']['id'])
		return response_success(blog_result['data']['id'])


	def after_blog_import(self, block_id, convert, block, blocks_ext):
		return response_success()


	def addition_blog_import(self, convert, block, blocks_ext):
		return response_success()


	# TODO: REVIEW

	def check_review_import(self, convert, review, reviews_ext):
		return True if self.get_map_field_by_src(self.TYPE_REVIEW, convert['id'], convert['code']) else False


	def router_review_import(self, convert, review, reviews_ext):
		return response_success('review_import')


	def before_review_import(self, convert, review, reviews_ext):
		return response_success()


	def review_import(self, convert, review, reviews_ext):
		product_id = False
		if convert['product']['id'] or convert['product']['code']:
			product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['product']['id'])

		if not product_id:
			return response_error(self.warning_import_entity('Review', convert['id'], convert['code'], 'product of review not exists.'))

		data = dict()
		data['name'] = convert['customer']['name']
		# data['email'] = ''
		title_change = 'Title of review ' + to_str(convert['id'])
		data['title'] = convert['title'] if convert['title'] else title_change
		data['text'] = convert['content']
		# data['date_reviewed'] = email.utils.format_datetime(datetime.datetime.strptime(convert['created_at'], '%Y-%m-%d %H:%M:%S')) if convert['created_at'] else email.utils.format_datetime(datetime.datetime.strptime(get_current_time(), '%Y-%m-%d %H:%M:%S'))
		data['date_reviewed'] = to_str(convert_format_time(convert['created_at'], '%Y-%m-%d %H:%M:%S')).replace(' ', 'T') + '+00:00'
		data['rating'] = to_int(to_decimal(self.calculate_average_rating(convert['rating']))) if to_int(to_decimal(self.calculate_average_rating(convert['rating']))) > 0 else 1
		rv_status = {
			2: 'pending',  # pedding
			1: 'approved',  # approved
			3: 'disapproved'  # not approved
		}
		data['status'] = get_value_by_key_in_dict(rv_status, to_int(convert['status']), 'pending')
		response = self.api_v3('/catalog/products/' + to_str(product_id) + '/reviews', data, 'Post')
		if response:
			response_data = json_decode(response)
			if response_data and response_data.get('data'):
				self.insert_map(self.TYPE_REVIEW, convert['id'], response_data['data']['id'], convert['code'])
				return response_success(response_data['data']['id'])
			else:
				return response_error(self.warning_import_entity('Review', convert['id'], convert['code'], response_data.get('title')))
		else:
			return response_error(self.warning_import_entity('Review', convert['id'], convert['code']))


	def after_review_import(self, review_id, convert, review, reviews_ext):
		return response_success()


	def addition_review_import(self, convert, review, reviews_ext):
		return response_success()


	# api code

	def api_v3(self, path, data = None, api_type = "get"):
		client_id = self._notice[self._type]['config']['api']['client_id'].strip()
		api_token = self._notice[self._type]['config']['api']['api_token'].strip()
		api_path = self._notice[self._type]['config']['api']['api_path'].strip()
		header = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		}
		header['X-Auth-Client'] = client_id
		header['X-Auth-Token'] = api_token
		url = api_path.rstrip('/') + '/' + path.strip().lstrip('/')
		method = 'request_by_' + to_str(api_type).lower()
		if isinstance(data, dict) or isinstance(data, list):
			data = json.dumps(data)
		return getattr(self, method)(url, data, header)


	def api_img_cate(self, path, data = None, api_type = "get"):
		api_token = self._notice[self._type]['config']['api']['api_token'].strip()
		api_path = self._notice[self._type]['config']['api']['api_path'].strip()
		header = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		}
		header['X-Auth-Token'] = api_token
		url = api_path.rstrip('/') + '/' + path.strip().lstrip('/')
		method = 'request_by_' + to_str(api_type).lower()
		if isinstance(data, dict) or isinstance(data, list):
			data = json.dumps(data)
		return getattr(self, method)(url, data, header)


	def get_province_from_country(self, country_code, province_name = None):
		result = {
			'name': '',
			'code': ''
		}
		method = 'request_by_get'
		countries_js = getattr(self, method)('https:#www.shopify.com/services/countries.json', None, {"Content-Type": "application/json"})
		countries_data = json.loads(countries_js)
		# if preg_match('/^var Countries = (.*?)/ms', countriesJs, matches)) {
		# countriesData = json_decode(matches[1], 1)
		# }
		if countries_data:
			for country in countries_data:
				if country['code'] == country_code:
					country_provinces = list()
					if 'provinces' in country:
						country_provinces = country['provinces']
					if province_name:
						for p in country_provinces:
							if p['name'].index(province_name) != -1 or province_name.index(p['name']) != -1:
								result = p
					if not result['code'] and country_provinces:
						result = self.py_reset(country_provinces)
		return result


	def calculate_average_rating(self, rates, default = 'default'):
		rate = get_row_from_list_by_field(rates, 'rate_code', default)
		if rate and 'rate' in rate:
			return rate['rate']
		rate_total = 0
		count = to_len(rates) if rates else 0
		for _rate in rates:
			rate_total = rate_total + to_decimal(_rate['rate'])
		average = to_decimal(rate_total / count)
		if average > 5:
			return 5
		else:
			return math.ceil(average)


	def _get_state_name_from_code(self, code):
		all_states = self.STATES
		code = to_str(code).upper()
		if code and to_str(code) in all_states:
			return all_states[code]
		return ' '


	def _get_state_code_from_name(self, name):
		all_states = self.STATES
		if name:
			for code, state_name in all_states.items():
				if to_str(name).lower() == to_str(state_name).lower():
					return code
		return name


	def detect_seo(self):
		return 'default_seo'


	def categories_default_seo(self, category, categories_ext):
		result = list()
		type_seo = self.SEO_DEFAULT
		if self._notice['support'].get('seo_301') and self._notice['config'].get('seo_301'):
			type_seo = self.SEO_301
		seo_cate = self.construct_seo_category()
		seo_cate['request_path'] = to_str(category['custom_url']['url']).strip('/')
		seo_cate['default'] = True
		seo_cate['store_id'] = 1
		seo_cate['type'] = type_seo
		result.append(seo_cate)
		return result


	def products_default_seo(self, product, products_ext):
		result = list()
		type_seo = self.SEO_DEFAULT
		if self._notice['support'].get('seo_301') and self._notice['config'].get('seo_301'):
			type_seo = self.SEO_301
		seo_product = self.construct_seo_product()
		seo_product['request_path'] = to_str(product['custom_url']['url']).strip('/')
		seo_product['default'] = True
		seo_product['store_id'] = 1
		seo_product['type'] = type_seo
		result.append(seo_product)
		return result


	def replace_bigcommerce_url(self, body_html):
		if not to_str(body_html):
			return ''
		body_html = to_str(body_html).replace('%%GLOBAL_ShopPath%%', self._cart_url.rstrip('/'))
		return body_html


	def validate_state(self, state_name):
		if not to_str(state_name):
			return True
		state = list(map(lambda x: x.lower(), list(self.STATES.values())))
		return to_str(state_name).lower() in state


	def remove_html(self, text):
		if not self._notice['config'].get('strip_html') or not text:
			return text
		text = re.sub('<[^<]+?>', '', text)
		return text


	def get_country_code_by_name(self, name):
		try:
			countries = json.loads(self.COUNTRIES)
			if name:
				for code, state_name in countries.items():
					if to_str(name).lower() == to_str(state_name).lower():
						return code
		except Exception as e:
			return ''
		return ''


	def get_id_product_blog(self):
		product_id = self.get_map_field_by_src('blog_product', 5081996, 'LitBlog')
		if not product_id:
			get_exists = self.api_v3('/catalog/products?name=LitBlog', None, 'Get')
			get_exists_json = json_decode(get_exists)
			if get_exists_json['data']:
				product_data = get_exists_json['data'][0]
				product_id = to_int(product_data['id'])
				self.insert_map('blog_product', 5081996, product_id, 'LitBlog', product_data['sku'])
				return product_id
			categories = list()
			category_id = self.get_map_field_by_src(self.TYPE_CATEGORY, 7101994)
			if not category_id:
				cat_lit_id = False
				cat_lit = self.api_v3("/catalog/categories?name=LitExtension")
				if cat_lit:
					cat_lit_decode = json_decode(cat_lit)
					if cat_lit_decode and cat_lit_decode.get('data') and isinstance(cat_lit_decode['data'], list):
						cat_lit_id = cat_lit_decode['data'][0].get('id')
						if cat_lit_id:
							self.insert_map(self.TYPE_CATEGORY, 7101994, cat_lit_id)
				if not cat_lit_id:
					cat_data = {
						'name': "LitExtension",
						'parent_id': 0,
						'description': 'This category is created for the product which was in an empty category',
						'is_visible': False
					}
					response_cat = self.api_v3('/catalog/categories', cat_data, 'Post')
					response_cat = json_decode(response_cat)
					if response_cat and response_cat.get('data'):
						response_cat_data = response_cat['data']
						if 'id' in response_cat_data:
							root_cate = True
							self.insert_map(self.TYPE_CATEGORY, 7101994, response_cat_data['id'])
							cat_lit_id = response_cat_data['id']
				category_id = cat_lit_id

			if category_id:
				categories.append(category_id)

			product_data = {
				"name": "LitBlog",
				"price": "0.00",
				"categories": categories,
				"weight": 0,
				"type": "physical",
				'sku': to_str(to_int(time.time())),
				'availability': 'disabled'
			}
			response = self.api_v3('/catalog/products', product_data, 'Post')
			response = json_decode(response)
			product_id = response['data']['id']
			self.insert_map('blog_product', 5081996, product_id, 'LitBlog', product_data['sku'])
		if not product_id:
			response_error('Can not create product for blog')
		return product_id


	def convert_link_image_description(self, description):
		# get product blog
		product_id = self.get_id_product_blog()
		match = re.findall(r"<img[^>]+>", to_str(description))
		links = list()
		if match:
			for img in match:
				img_src = re.findall(r"(src=[\"'](.*?)[\"'])", to_str(img))
				if not img_src:
					continue
				img_src = img_src[0]
				if img_src[1] in links:
					continue
				links.append(img_src[1])
				# post image
				data_post = {
					'image_url': img_src[1],
					'is_thumbnail': False,
					'description': ''
				}
				res = self.api_v3('/catalog/products/' + to_str(product_id) + '/images', data_post, 'post')
				# self.log(res, 'res')
				res = json_decode(res)
				if res.get('status') in [422, 400, 404]:
					self.log('Image error: ' + img_src[1], 'image_error')
				else:
					url_image_target = res['data']['url_zoom']
					description = description.replace(img_src[1], url_image_target)
		return description

	def insert_image_desc(self, image):
		# get product blog
		product_id = self.get_id_product_blog()
		# match = re.findall(r"<img[^>]+>", to_str(description))
		# links = list()
		# if match:
		# 	for img in match:
		# img_src = re.findall(r"(src=[\"'](.*?)[\"'])", to_str(image))
		# if not img_src:
		# 	continue
		# img_src = img_src[0]
		# if img_src[1] in links:
		# 	continue
		# links.append(img_src[1])
		# post image
		data_post = {
			'image_url': image,
			'is_thumbnail': False,
			'description': ''
		}
		res = self.api_v3('/catalog/products/' + to_str(product_id) + '/images', data_post, 'post')
		# self.log(res, 'res')
		res = json_decode(res)
		if res.get('status') in [422, 400, 404]:
			self.log('Image error: ' + img_src[1], 'image_error')
		else:
			url_image_target = res['data']['url_zoom']
			# url_image_target = res['data']['url_zoom']
			# description = description.replace(img_src[1], url_image_target)
		return url_image_target


	def api_get_customer_groups(self, path, data = None, api_type = "get", header = {"Content-Type": "application/json"}):
		# time.sleep(0.5)
		client_id = self._notice[self._type]['config']['api']['client_id'].strip()
		api_token = self._notice[self._type]['config']['api']['api_token'].strip()
		header = {
			'Accept': 'application/json',
			'Content-Type': 'application/json',
		}
		if (not self._notice[self.get_type()]['config'].get('api_version') and not self.version) or to_int(self._notice[self.get_type()]['config'].get('api_version')) == 3 or self.version == 3:
			header['X-Auth-Client'] = client_id
			header['X-Auth-Token'] = api_token
		url = self.get_api_url() + path.strip()
		# if 'modifiers' in url and 'catalog' in url:
			# url = url.replace('/v2/', '/v3/')
		url = 'https://api.bigcommerce.com/stores/1rz45mi4ur/v2/customer_groups'
		method = 'request_by_' + to_str(api_type).lower()
		if isinstance(data, dict) or isinstance(data, list):
			data = json.dumps(data)
		return getattr(self, method)(url, data, header)
