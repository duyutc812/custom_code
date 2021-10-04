# Add option value name of variants into tags in shopify
taggggs = list()
taggggs.append(child_option_value_data['option_value_name'])
if len(taggggs) > 0:
    tmp_tag = ','.join(set(taggggs))
    product_data['tags'] += ',' + tmp_tag


# log: 2021/02/03 13:57:17 : web,B2B,25kg,1kg

# Add metafield in Shopify

def check_product_import(self, convert, product, products_ext):
    pro_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
    if pro_id:
        product_data = self.api('products/' + to_str(pro_id) + '.json')
        value = convert['description'] + convert['short_description']
        pro_metafield = {
            "metafield": {
                "key": "Merge_Desc_Short_Desc",
                "value": value,
                "value_type": "string",
                "namespace": "global",
            }
        }
        update_desc = self.api('products/' + to_str(pro_id) + '/metafields.json', pro_metafield, 'Post')
        self.log(update_desc, 'update_desc')
    return self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])


# clear dữ liệu đã import vào map và site target:

if 'clear_product_imported' not in self._notice:
    self._notice['clear_product_imported'] = True
    self.clear_target_products_demo()


# update giá, sku, barcode, supplier woocommerce:
def check_manufacturer_import(self, convert, manufacturer, manufacturers_ext):
    # 1
    manu_id = self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['id'])
    if manu_id:
        value = self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['id'], manu_id, field='value')
        if not value:
            update_supplier_posts_data = {
                'post_author': 1,
                'post_date': get_current_time(),
                'post_date_gmt': get_current_time(),
                'post_content': '',
                'post_title': convert['name'],
                'post_excerpt': '',
                'post_status': 'publish',
                'comment_status': 'closed',
                'ping_status': 'closed',
                'post_password': '',
                'post_name': to_str(convert['name']).lower(),
                'to_ping': '',
                'pinged': '',
                'post_modified': get_current_time(),
                'post_modified_gmt': get_current_time(),
                'post_content_filtered': '',
                'post_parent': 0,
                'guid': '',
                'menu_order': 0,
                'post_type': 'atum_supplier',
                'post_mime_type': '',
                'comment_count': 0,
            }
            supplier_id = self.import_data_connector(
                self.create_insert_query_connector('posts', update_supplier_posts_data))
            self.import_data_connector(self.create_update_query_connector('posts', {
                'guid': 'https://amvitamins.flywheelsites.com/?post_type=atum_supplier&#038;p=' + to_str(supplier_id)},
                                                                          {'ID': supplier_id}))
            if supplier_id:
                update_map = self.update_map(self.TYPE_MANUFACTURER, convert['id'], None, manu_id, value=supplier_id)
                self.log(update_map, 'supplier_id.log')
        self.log(self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['id'], manu_id, field='value'),
                 'supplier_id.log')
    self.log(supplier_id, 'supplier_id.log')
    return True if self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['id']) else False


def check_product_import(self, convert, product, products_ext):
    product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'],
                                           lang=self._notice['target']['language_default'])
    if product_id:
        self.log(convert, 'convert_product')
        self.log(product_id, 'convert_product')
        # url_query = self.get_connector_url('query')
        # product_image_query = {
        # 'image': {
        # 	'type': 'select',
        # 	'query': "SELECT meta_value FROM _DBPRF_postmeta where meta_key = '_thumbnail_id' and post_id = " + to_str(product_id),
        # 	}
        # }
        # product_image_data = self.get_connector_data(url_query, {'serialize': True, 'query': json.dumps(product_image_query)})
        # if product_image_data['data']['image']:
        # 	pro_image_id = to_int(product_image_data['data']['image'][0]['meta_value'])
        # 	if pro_image_id:
        # 		self.import_data_connector(self.create_update_query_connector('posts', {'post_title': convert['name']}, {'id': to_str(pro_image_id)}))
        # 	self.log(pro_image_id, 'pro_image_id')
        # self.log(product_id, 'pro_image_id')
        check_product_atunm_exists = self.select_data_connector(
            self.create_select_query_connector('atum_product_data', {'product_id': product_id}))
        supp_id = self.get_map_field_by_src(self.TYPE_MANUFACTURER, convert['manufacturer']['id'], field='value')
        # self.log(check_product_atunm_exists, 'check_product_atunm_exists.log')
        if check_product_atunm_exists['data']:
            self.log(self.import_data_connector(self.create_update_query_connector('atum_product_data',
                                                                                   {'supplier_id': supp_id,
                                                                                    'purchase_price': convert[
                                                                                        'cost_price']},
                                                                                   {'product_id': product_id})),
                     'get_supp_id')
        else:
            self.log(self.import_data_connector(self.create_insert_query_connector('atum_product_data',
                                                                                   {'product_id': product_id,
                                                                                    'supplier_id': supp_id,
                                                                                    'purchase_price': convert[
                                                                                        'cost_price']})), 'get_supp_id')
        # self.log(convert['manufacturer']['id'], 'supp_id.log')
        # self.log(supp_id, 'supp_id.log')
        # self.log(product_id, 'product_id')
        self.log(self.import_data_connector(
            self.create_update_query_connector('postmeta', {'meta_value': convert['sku']},
                                               {'post_id': product_id, 'meta_key': '_sku'})), 'update_sku')

        # update Compare at price - regular_price
        if convert.get('price'):
            check_product_regular_price_exists = self.select_data_connector(
                self.create_select_query_connector('postmeta', {'post_id': product_id, 'meta_key': '_regular_price'}))
            if check_product_regular_price_exists['data']:
                self.log(self.import_data_connector(
                    self.create_update_query_connector('postmeta', {'meta_value': convert['price']},
                                                       {'post_id': product_id, 'meta_key': '_regular_price'})),
                    'update_regular_price')
            else:
                self.log(self.import_data_connector(self.create_insert_query_connector('postmeta',
                                                                                       {'post_id': product_id,
                                                                                        'meta_key': '_regular_price',
                                                                                        'meta_value': convert[
                                                                                            'price']})),
                         'insert_regular_price')

        # update Price - sale price
        if convert['special_price'].get('price'):
            check_product_sale_price_exists = self.select_data_connector(
                self.create_select_query_connector('postmeta', {'post_id': product_id, 'meta_key': '_sale_price'}))
            check_product_price_exists = self.select_data_connector(
                self.create_select_query_connector('postmeta', {'post_id': product_id, 'meta_key': '_price'}))
            if check_product_sale_price_exists['data'] and check_product_price_exists['data']:
                self.log(self.import_data_connector(self.create_update_query_connector('postmeta', {
                    'meta_value': convert['special_price'].get('price')}, {'post_id': product_id,
                                                                           'meta_key': '_sale_price'})),
                         'update_sale_price')
                self.log(self.import_data_connector(self.create_update_query_connector('postmeta', {
                    'meta_value': convert['special_price'].get('price')}, {'post_id': product_id,
                                                                           'meta_key': '_price'})), 'update_price')
            else:
                self.log(self.import_data_connector(self.create_insert_query_connector('postmeta',
                                                                                       {'post_id': product_id,
                                                                                        'meta_key': '_sale_price',
                                                                                        'meta_value': convert[
                                                                                            'special_price'].get(
                                                                                            'price')})),
                         'insert_sale_price')
                self.log(self.import_data_connector(self.create_insert_query_connector('postmeta',
                                                                                       {'post_id': product_id,
                                                                                        'meta_key': '_price',
                                                                                        'meta_value': convert[
                                                                                            'special_price'].get(
                                                                                            'price')})), 'insert_price')

        # update barcode
        check_product_barcode_meta_exists = self.select_data_connector(
            self.create_select_query_connector('postmeta', {'post_id': product_id, 'meta_key': 'oliver_barcode'}))
        if check_product_barcode_meta_exists['data']:
            self.log(self.import_data_connector(
                self.create_update_query_connector('postmeta', {'meta_value': convert['barcode']},
                                                   {'post_id': product_id, 'meta_key': 'oliver_barcode'})),
                'update_barcode')
        else:
            self.log(self.import_data_connector(self.create_insert_query_connector('postmeta', {'post_id': product_id,
                                                                                                'meta_key': 'oliver_barcode',
                                                                                                'meta_value': convert[
                                                                                                    'barcode']})),
                     'insert_barcode')

        # update gtin
        check_product_gtin = self.select_data_connector(
            self.create_select_query_connector('postmeta', {'post_id': product_id, 'meta_key': '_rank_math_gtin_code'}))
        if check_product_gtin['data']:
            self.log(self.import_data_connector(
                self.create_update_query_connector('postmeta', {'meta_value': convert['barcode']},
                                                   {'post_id': product_id, 'meta_key': '_rank_math_gtin_code'})),
                'update_gtin')
        else:
            self.log(self.import_data_connector(self.create_insert_query_connector('postmeta', {'post_id': product_id,
                                                                                                'meta_key': '_rank_math_gtin_code',
                                                                                                'meta_value': convert[
                                                                                                    'barcode']})),
                     'insert_gtin')

        # update stock
        stock_status = 'instock'
        if convert.get('is_in_stock'):
            stock_status = 'instock' if to_int(convert['qty']) else 'outofstock'
        else:
            stock_status = 'outofstock' if convert['manage_stock'] else 'instock'
        self.log(self.import_data_connector(
            self.create_update_query_connector('postmeta', {'meta_value': convert['qty']},
                                               {'post_id': product_id, 'meta_key': '_stock'})), 'update_stock_qty')
        self.log(self.import_data_connector(self.create_update_query_connector('postmeta', {'meta_value': stock_status},
                                                                               {'post_id': product_id,
                                                                                'meta_key': '_stock_status'})),
                 'update_stock_status')

        if convert.get('cost_price'):
            check_product_cost_meta_exists = self.select_data_connector(
                self.create_select_query_connector('postmeta', {'post_id': product_id, 'meta_key': 'product_cost'}))
            if check_product_cost_meta_exists['data']:
                self.log(self.import_data_connector(
                    self.create_update_query_connector('postmeta', {'meta_value': convert['cost_price']},
                                                       {'post_id': product_id, 'meta_key': 'product_cost'})),
                    'update_cost')
            else:
                self.log(self.import_data_connector(self.create_insert_query_connector('postmeta',
                                                                                       {'post_id': product_id,
                                                                                        'meta_key': 'product_cost',
                                                                                        'meta_value': convert[
                                                                                            'cost_price']})),
                         'insert_cost')

    # self.log(product_id, 'pro_woo_id.log')

    # return self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'], lang = self._notice['target']['language_default'])
    return True


# update price rules in bigcommerce 

def check_product_import(self, convert, product, products_ext):
    pro_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
    if pro_id and convert['tier_prices']:
        list_qty = list()
        tier_prices = dict()
        for tier_price in convert['tier_prices']:
            qty = to_int(tier_price['qty'])
            if qty not in list_qty:
                list_qty.append(qty)
                tier_prices[qty] = tier_price
        list_qty.sort()
        # bulk_prices = list()
        for index, qty in enumerate(list_qty):
            if index < len(list_qty) - 1:
                max_qty = list_qty[index + 1] - 1
            else:
                max_qty = 0
            bulk_price = {
                "quantity_min": to_int(qty),
                "quantity_max": max_qty,
                "type": "percent" if convert['tier_prices'][index].get('price_type') == 'percent' else 'fixed',
                "amount": to_decimal(convert['tier_prices'][index]['price'])
            }
            # a = bulk_prices.append(bulk_price)
            self.log(self.api_v3('/catalog/products/' + to_str(pro_id) + '/bulk-pricing-rules', bulk_price, 'Post'),
                     'update_bulk_pricing_rules')
        # self.log(bulk_prices, 'bulk_prices.log')
    self.log(convert, 'tar_convert_pro.log')
    return self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])


# update sale pice(product, product_variant) woocommerce

def check_product_import(self, convert, product, products_ext):
    pro_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'],
                                       lang=self._notice['target']['language_default'])
    if pro_id:
        children_list = list()
        option_list = list()
        if convert['children']:
            children_list = convert['children']
            if to_len(children_list) > 100:
                msg = 'Product '
                if convert['id']:
                    msg += 'id ' + to_str(convert['id'])
                elif convert['code']:
                    msg += 'code: ' + convert['code']
                msg += ": too much variant (" + to_str(to_len(children_list)) + ")"
                self.log(msg, 'variant')
            option_list = self.convert_child_to_option(children_list)
        else:
            if convert['options']:
                option_list = convert['options']
                if self.count_child_from_option(convert['options']) <= self.VARIANT_LIMIT:
                    children_list = self.convert_option_to_child(option_list, convert)
        if children_list:
            for key_child, product_child in enumerate(children_list):
                # self.insert_map(self.TYPE_CHILD, product_child['id'], children_id, product_child['code'])
                pro_child_id = self.get_map_field_by_src(self.TYPE_CHILD, product_child['id'], convert['code'],
                                                         lang=self._notice['target']['language_default'])
                children_meta = {
                    '_sale_price': product_child['special_price']['price'] if product_child['special_price'][
                                                                                  'price'] and (self.to_timestamp(
                        product_child['special_price']['end_date']) > time.time() or (product_child['special_price'][
                                                                                          'end_date'] == '0000-00-00' or
                                                                                      product_child['special_price'][
                                                                                          'end_date'] == '0000-00-00 00:00:00' or
                                                                                      product_child['special_price'][
                                                                                          'end_date'] == '' or
                                                                                      product_child['special_price'][
                                                                                          'end_date'] == None or
                                                                                      convert['special_price'][
                                                                                          'end_date'] == None)) else '',
                    '_price': product_child['special_price']['price'] if product_child['special_price']['price'] and (
                            self.to_timestamp(product_child['special_price']['end_date']) > time.time() or (
                            product_child['special_price']['end_date'] == '0000-00-00' or
                            product_child['special_price']['end_date'] == '0000-00-00 00:00:00' or
                            product_child['special_price']['end_date'] == '' or product_child['special_price'][
                                'end_date'] == None or convert['special_price']['end_date'] == None)) else
                    product_child['price'],
                }
                check_pro_child_sale = self.import_data_connector(
                    self.create_select_query_connector('postmeta',
                                                       {'post_id': pro_child_id,
                                                        'meta_key': '_sale_price'}))
                if check_pro_child_sale:
                    for key, value in children_meta.items():
                        self.import_data_connector(
                            self.create_update_query_connector('postmeta', {'meta_value': value},
                                                               {'post_id': pro_child_id, 'meta_key': key}))
                else:
                    for key, value in children_meta.items():
                        self.import_data_connector(
                            self.create_insert_query_connector('postmeta', {'post_id': pro_child_id, 'meta_key': key,
                                                                            'meta_value': value}))
                if product_child['special_price']['price'] and (
                        self.to_timestamp(product_child['special_price']['end_date']) > time.time() or (
                        product_child['special_price']['end_date'] != '0000-00-00' or product_child['special_price'][
                    'end_date'] != '0000-00-00 00:00:00' or convert['special_price']['end_date'] == None)) or \
                        product_child['special_price']['end_date'] == '':
                    if product_child['special_price']['start_date']:
                        children_meta['_sale_price_dates_from'] = self.to_timestamp(
                            product_child['special_price']['start_date'])
                    else:
                        children_meta['_sale_price_dates_from'] = None
                    if product_child['special_price']['end_date']:
                        children_meta['_sale_price_dates_to'] = self.to_timestamp(
                            product_child['special_price']['end_date'])
                    else:
                        children_meta['_sale_price_dates_to'] = None
                    check_sale_date_from = self.import_data_connector(
                        self.create_select_query_connector('postmeta',
                                                           {'post_id': pro_child_id,
                                                            'meta_key': '_sale_price_dates_from'}))
                    if check_sale_date_from:
                        self.import_data_connector(self.create_update_query_connector('postmeta', {
                            'meta_value': children_meta['_sale_price_dates_from']},
                                                                                      {'post_id': pro_child_id,
                                                                                       'meta_key': '_sale_price_dates_from'}))
                    else:
                        self.import_data_connector(self.create_insert_query_connector('postmeta',
                                                                                      {'post_id': pro_child_id,
                                                                                       'meta_key': '_sale_price_dates_from',
                                                                                       'meta_value': children_meta[
                                                                                           '_sale_price_dates_from']}))
                    check_sale_date_to = self.import_data_connector(
                        self.create_select_query_connector('postmeta',
                                                           {'post_id': pro_child_id,
                                                            'meta_key': '_sale_price_dates_to'}))
                    if check_sale_date_to:
                        self.import_data_connector(self.create_update_query_connector('postmeta',
                                                                                      {'meta_value': children_meta[
                                                                                          '_sale_price_dates_to']},
                                                                                      {'post_id': pro_child_id,
                                                                                       'meta_key': '_sale_price_dates_to'}))
                    else:
                        self.import_data_connector(self.create_insert_query_connector('postmeta',
                                                                                      {'post_id': pro_child_id,
                                                                                       'meta_key': '_sale_price_dates_to',
                                                                                       'meta_value': children_meta[
                                                                                           '_sale_price_dates_to']}))
    return True


# update product variants image shopify:
pro_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
if pro_id and convert['children']:
    dic_image = dict()
    image_id = None
    # data_images = json_decode(self.api('products/' + str(pro_id) + '.json'))['product']['images']
    for child in convert['children']:
        child_id = self.get_map_field_by_src(self.TYPE_CHILD, child['id'], child['code'])
        if child_id and child['thumb_image']['url'] and child['thumb_image']['path']:
            data_thumb_image = child['thumb_image']
            # check image exists
            url_image = data_thumb_image['url'] + data_thumb_image['path']
            if url_image in dic_image.values():
                for k, v in dic_image.items():
                    if v == url_image:
                        image_id = k
                        break
            else:
                data_image_post = {
                    "image": {
                        "src": data_thumb_image['url'] + data_thumb_image['path']
                    }
                }
                image_post = self.api('products/' + to_str(pro_id) + '/images.json', data_image_post, 'POST')
                if image_post:
                    image_id = json_decode(image_post)['image']['id']
                    dic_image[image_id] = url_image
            data_image_update = {
                "image": {
                    "id": image_id,
                    "variant_ids": [child_id]
                }
            }
            # products/632910392/images/850703190.json
            self.api('products/' + to_str(pro_id) + '/images/' + to_str(image_id) + '.json', data_image_update, 'put')

# Xóa cate từ magento → woo
cate_id = self.get_map_field_by_src(self.TYPE_CATEGORY, convert['id'], convert['code'], lang=self._notice['target']['language_default'])
if cate_id:
    if len(category['path']) >= 6 and category['path'][:6] != '1/1285':
        where = {
            'migration_id': self._migration_id,
            'type': self.TYPE_CATEGORY,
            'id_desc': cate_id
        }
        # categories = self.select_obj(TABLE_MAP, where)
        # category_ids = list()
        # if categories['result'] == 'success':
        #  category_ids = duplicate_field_value_from_list(categories['data'], 'id_desc')
        # if not category_ids:
        #  return next_clear
        category_id_con = self.list_to_in_condition([cate_id])
        taxonomy_meta_table = 'termmeta'
        collections_query = {
            'type': 'select',
            'query': "SELECT * FROM `_DBPRF_term_taxonomy` WHERE (taxonomy = 'product_cat' OR taxonomy = 'post_cat') AND term_id = " + to_str(
                cate_id)
        }
        categories = self.get_connector_data(self.get_connector_url('query'),
                                             {'query': json.dumps(collections_query)})
        if categories['data']:
            all_queries = list()
            taxonomy_ids = duplicate_field_value_from_list(categories['data'], 'term_taxonomy_id')
            all_queries.append({
                'type': 'query',
                'query': "DELETE FROM `_DBPRF_" + taxonomy_meta_table + "` WHERE term_id IN " + category_id_con
            })
            all_queries.append({
                'type': 'query',
                'query': "DELETE FROM `_DBPRF_terms` WHERE term_id IN " + category_id_con
            })
            all_queries.append({
                'type': 'query',
                'query': "DELETE FROM `_DBPRF_term_taxonomy` WHERE term_taxonomy_id IN " + self.list_to_in_condition(
                    taxonomy_ids)
            })
            if self._notice['target']['support']['wpml']:
                clear_table = self.get_connector_data(self.get_connector_url('query'), {
                    'query': json.dumps({
                        'type': 'query',
                        'query': "DELETE FROM `_DBPRF_icl_translations` "
                                 "WHERE element_type = 'tax_product_cat' AND element_id IN " + category_id_con
                    })
                })
            if self._notice['config']['seo'] or self._notice['config']['seo_301']:
                clear_table = self.get_connector_data(self.get_connector_url('query'), {
                    'query': json.dumps({
                        'type': 'query',
                        'query': "DELETE FROM `_DBPRF_lecm_rewrite` where type = 'category' and type_id IN " + category_id_con
                    })
                })
            if all_queries:
                self.import_multiple_data_connector(all_queries, 'cleardemo')
            self.delete_obj(TABLE_MAP, where)
            self.log(to_str(convert['id']) + ' | ' + to_str(cate_id), 'del_default_categories')

# update attribute - value(text) woocommerce:
product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'],
                                       lang=self._notice['target']['language_default'])
if product_id:
    where = {
        'post_id': product_id,
        'meta_key': '_product_attributes',
    }
    check_pro_attr = self.select_data_connector(self.create_select_query_connector('postmeta', where, 'meta_value'))
    if check_pro_attr:
        pro_attr_data = php_unserialize(check_pro_attr['data'][0]['meta_value'])
        if pro_attr_data:
            # pro_lst = list(pro_attr_data.keys())
            if pro_attr_data.get('no-stock-message') and pro_attr_data.get('no-stock-message').get(
                    'value') == '[mgz_pagebuilder]{"elements":[]}[/mgz_pagebuilder]':
                pro_attr_data['no-stock-message']['value'] = ''
            if pro_attr_data.get('technical-description'):
                value_tech_desc = pro_attr_data.pop('technical-description')
                pro_attr_data['technical-description'] = value_tech_desc
            else:
                return True
            position = 0
            for i in list(pro_attr_data.keys()):
                key = val = None
                pro_attr_data[i]['position'] = list(pro_attr_data.keys()).index(i)
                position = pro_attr_data[i]['position']
                if pro_attr_data.get('technical-description') and pro_attr_data.get('technical-description').get(
                        'value') == '[mgz_pagebuilder]{"elements":[]}[/mgz_pagebuilder]':
                    pro_attr_data['technical-description']['value'] = ''
                    break
                if i == 'technical-description' and pro_attr_data[i]['value'][0:4] not in ['<img', '<tab']:
                    pro_atrr_value = pro_attr_data[i]['value']
                    pro_attr_data[i]['value'] = 'Technical Description'
                    if '||' not in pro_atrr_value:
                        data = pro_atrr_value.split('&&')
                        key, val = data[0], data[1]
                        pro_attr_data['_'.join(data[0].split()).lower()] = {
                            'name': key.strip(':'),
                            'value': val,
                            'position': position + 1,
                            'is_visible': 1,
                            'is_variation': 0,
                            'is_taxonomy': 0,
                        }
                    else:
                        list_attr = pro_atrr_value.split('||')
                        for attr in list_attr:
                            if '||' not in attr:
                                data = attr.split('&&')
                                key, val = data[0], data[1]
                                pro_attr_data['_'.join(data[0].split()).lower()] = {
                                    'name': key.strip(':'),
                                    'value': val,
                                    'position': position + 1 + list_attr.index(attr),
                                    'is_visible': 1,
                                    'is_variation': 0,
                                    'is_taxonomy': 0,
                                }
            if pro_attr_data.get('technical-description'):
                pro_attr_data.pop('technical-description')
        pro_attr_unser = php_serialize(pro_attr_data)
        data_update = {
            'meta_value': pro_attr_unser,
        }
        self.select_data_connector(self.create_update_query_connector('postmeta', data_update, where))
return True


# recent migration for godaddy:

# kiểm tra entity cuối cùng và số page, cập nhật trên migration_recent và update


def display_import_source(self):
    parent = super().display_import_source()
    if parent['result'] != 'success':
        return parent
    recent = self.get_recent(self._migration_id)
    # if recent:
    #  types = ['categories', 'products']
    #  for _type in types:
    #     self._notice['process'][_type]['id_src'] = recent['process'][_type]['id_src']
    #     self._notice['process'][_type]['total'] = 0
    #     self._notice['process'][_type]['imported'] = 0
    #     self._notice['process'][_type]['error'] = 0
    self._notice['process']['products']['total'] = self.()
    self._notice['process']['products']['imported'] = recent['process']['products']['imported']
    self._notice['process']['products']['total_view'] = self._notice['process']['products']['total'] - \
                                                        self._notice['process']['products']['imported']
    # if self._notice['src']['config']['login_type']:
    self._notice['process']['orders']['total'] = self.get_totalCount_Orders()
    self._notice['process']['categories']['total'] = self.get_totalCount_categories()
    self._notice['process']['categories']['imported'] = recent['process']['categories']['imported']
    self._notice['process']['categories']['total_view'] = self._notice['process']['categories']['total'] - \
                                                          self._notice['process']['categories']['imported']
    return response_success()


# delete disable items
# pro_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
# if pro_id:
# 	for pro_child in convert['children']:
# 		if not pro_child['status']:
# 			pro_child_id = self.get_map_field_by_src(self.TYPE_CHILD, pro_child['id'], pro_child['code'])
# 			if pro_child_id:
# 				self.api('products/' + to_str(pro_id) + '/variants/' + to_str(pro_child_id) + '.json', None, 'DELETE')
# 				self.log(to_str(pro_id) + ' | ' + to_str(pro_child_id), 'pro_variant_del')
# 				where = {
# 					'migration_id': self._migration_id,
# 					'type': self.TYPE_CHILD,
# 					'id_desc': pro_child_id
# 				}
# 				self.delete_obj(TABLE_MAP, where)
# # if pro_id and convert['status_pro'] == 2:
# # 	self.api('products/' + to_str(pro_id) + '.json', None, 'DELETE')
# # 	where = {
# # 		'migration_id': self._migration_id,
# # 		'type': self.TYPE_PRODUCT,
# # 		'id_desc': pro_id
# # 	}
# # 	self.log(to_str(convert['id']) + ' | ' + to_str(pro_id), 'pro_del')
# # 	self.delete_obj(TABLE_MAP, where)

# return True
# # return self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])

# update image for product variants
# pro_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
# if pro_id and convert['children']:
# 	dic_image = dict()
# 	pro_variant = []
# 	image_id = None
# 	# data_images = json_decode(self.api('products/' + str(pro_id) + '.json'))['product']['images']
# 	pro_variant_data = self.api('products/' + to_str(pro_id) + '/variants.json?limit=250')
# 	if pro_variant_data:
# 		pro_variant = json_decode(pro_variant_data)['variants']
# 	else:
# 		return True
# 	for child in convert['children']:
# 		image_id = None
# 		# child_id = self.get_map_field_by_src(self.TYPE_CHILD, child['id'], child['code'])
# 		child_id = get_row_value_from_list_by_field(pro_variant, 'sku', child['sku'], 'id')

# 		if child_id and child['thumb_image']['url'] and child['thumb_image']['path']:
# 			data_thumb_image = child['thumb_image']
# 			# check image exists
# 			url_image = data_thumb_image['url'] + data_thumb_image['path']
# 			if url_image in dic_image.values():
# 				for k, v in dic_image.items():
# 					if v == url_image:
# 						image_id = k
# 						break
# 			else:
# 				data_image_post = {
# 					"image": {
# 						"src": data_thumb_image['url'] + data_thumb_image['path']
# 					}
# 				}
# 				image_post = self.api('products/' + to_str(pro_id) + '/images.json', data_image_post, 'POST')
# 				if image_post:
# 					image_id = json_decode(image_post)['image']['id']

# 					dic_image[image_id] = url_image
# 			data_image_update = {
# 				"image": {
# 					"id": image_id,
# 					"variant_ids": [child_id]
# 				}
# 			}
# 				# products/632910392/images/850703190.json
# 			self.api('products/' + to_str(pro_id) + '/images/' + to_str(image_id) + '.json', data_image_update, 'put')
# 	self.log(to_str(convert['id']) + ' | ' + to_str(pro_id), 'update_variant_iamges')

# return True

# sort product variant
# product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
# if product_id:
#     product_api = self.api('products/' + to_str(product_id) + '.json')
#     product_data = json_decode(product_api)
#     product_data = product_data.get('product')
#     variants = []
#     if product_data:
#         variants = product_data['variants']
#
#     # check_sort = 1
#
#     new_variants = []
#     if len(variants) > 1:
#         sorted_child = sorted(convert['children'], key=lambda i: i['position'])
#         for child in sorted_child:
#             for variant in variants:
#                 if child['sku'] == variant['sku']:
#                     new_variants.append(variant)
#     else:
#         return True
#     # self.log(new_variants, 'new')
#     # self.log(convert['id'], 'new')
#
#     product_data['variants'] = new_variants if new_variants else variants
#     update_data = {"product": product_data}
#     self.log(product_data, 'update_data')
#     update_response = self.api('products/' + to_str(product_id) + '.json', update_data, 'PUT')
#
#     self.log(to_str(convert['id']) + ' | ' + to_str(product_id), 'sort_product_variant')
# self.log(update_response, 'res')

# add product tag
# product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
# self.log(convert, 'convert')
# if product_id:
# 	product_api = self.api('products/' + to_str(product_id) +'.json')
# 	product_data = json_decode(product_api)
# 	product_data = product_data.get('product')
# 	tags = ""
# 	if product_data:
# 		tags = product_data['tags']

# 	# if convert['guest_hide_price']:
# 	# 	tags += ', guest_hide_price'
# 	# else:
# 	# 	return True

# 	if convert['enable_qty_increments']:
# 		tags += ', qty_increments'
# 	else:
# 		return True

# 	# new_variants = []
# 	# if len(variants) > 1:
# 	# 	sorted_child = sorted(convert['children'], key=lambda i: i['position'])
# 	# 	for child in short_description_child:
# 	# 		for variant in variants:
# 	# 			if child['sku'] == variant['sku']:
# 	# 				new_variants.append(variant)
# 	# else:
# 	# 	return True
# 	# self.log(new_variants, 'new')
# 	# self.log(convert['id'], 'new')

# # 	product_data['variants'] = new_variants if new_variants else variants
# 	update_data = {
# 		"product": {
# 			"tags": tags,
# 		}

# 	}
# 	update_response = self.api('products/' + to_str(product_id) +'.json', update_data, 'PUT')

# 	self.log(to_str(convert['id']) + ' | ' + to_str(product_id) + ' | ' + to_str(product_data['tags']) + ' | ' + to_str(tags), 'add_pro_tags')
# # 	# self.log(update_response, 'res')
# product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
# if product_id:
#     product_api = self.api('products/' + to_str(product_id) + '.json')
#     product_data = json_decode(product_api)
#     product_data = product_data.get('product')
#     list_old_variants = []
#     list_old_options = []
#
#     if product_data:
#         list_old_variants = product_data['variants']
#         list_old_options = product_data['options']
#     sale_price = None
#     compare_price = None
#     if convert.get('special_price', dict()).get('price') and self.to_timestamp(
#             convert['special_price']['start_date']) < time.time() and (
#             self.to_timestamp(convert['special_price']['end_date']) > time.time() or (
#             convert['special_price']['end_date'] == '0000-00-00' or convert['special_price'][
#         'end_date'] == '0000-00-00 00:00:00') or convert['special_price']['end_date'] == '' or
#             convert['special_price']['end_date'] == None):
#         sale_price = convert['special_price']['price']
#         compare_price = convert['price'] if convert['price'] and round(to_decimal(convert['price']), 2) > round(
#             to_decimal(sale_price), 2) else None
#     else:
#         sale_price = convert['price']
#
#     img_children = dict()
#     ivt_children = dict()
#     # if
#     if convert['children']:
#         _map = dict()
#         variants = list()
#         options = list()
#         index = 1
#         options_src = dict()
#         count = 0
#         option_value_dict = dict()
#         for child in convert['children']:
#             max_count = len(child['attributes']) if child['attributes'] else 0
#             if max_count > count:
#                 count = max_count
#                 options_src = child['attributes']
#             for option in options_src:
#                 if option['option_name'] not in option_value_dict:
#                     option_value_dict[option['option_name']] = dict()
#                     option_value_dict[option['option_name']][option['option_value_id']] = option[
#                         'option_value_name']
#                 elif option['option_value_id'] not in option_value_dict[option['option_name']]:
#                     option_value_dict[option['option_name']][option['option_value_id']] = option[
#                         'option_value_name']
#         # self.log(option_value_dict, 'options')
#         if not count:
#             # self.log('Product id ' + to_str(convert['id']) + 'import failed. Please fill out children attributes!', 'product_errors')
#             return response_error(
#                 'Product id ' + to_str(convert['id']) + 'import failed. Please fill out children attributes!',
#                 'product_errors')
#         all_option_name = list()
#         for option in options_src:
#             if index == 4:
#                 break
#             if option['option_name'] in all_option_name:
#                 continue
#             all_option_name.append(option['option_name'])
#             _map[get_value_by_key_in_dict(option, 'option_id', option['option_code'])] = index
#             option_values = option_value_dict[to_str(option['option_name'])]
#             option_target = {
#                 'product_id': product_id,
#                 'position': index,
#                 'name': to_str(option['option_name']).replace('/', '-')
#             }
#             if option_values:
#                 option_target['values'] = list()
#                 for key in sorted(option_values.keys()):
#                     option_target['values'].append(option_values[key])
#
#             options.append(option_target)
#             index += 1
#         pos = 1
#         number_variant_imported = 0
#         # for
#         list_variants = list()
#         for child in convert['children']:
#             if number_variant_imported >= 100:
#                 break
#             if child.get('special_price', dict()).get('price') and self.to_timestamp(
#                     convert['special_price']['start_date']) < time.time() and (
#                     self.to_timestamp(child['special_price']['end_date']) > time.time() or (
#                     child['special_price']['end_date'] == '0000-00-00' or child['special_price'][
#                 'end_date'] == '0000-00-00 00:00:00') or child['special_price']['end_date'] == '' or
#                     child['special_price']['end_date'] == None):
#                 child_sale_price = child.get('special_price', dict()).get('price')
#                 child_compare_price = child['price'] if child['price'] and round(to_decimal(child['price']),
#                                                                                  2) > round(
#                     to_decimal(child_sale_price), 2) else None
#             else:
#                 child_sale_price = child['price']
#                 child_compare_price = compare_price if compare_price and round(to_decimal(compare_price),
#                                                                                2) > round(
#                     to_decimal(child_sale_price), 2) else None
#             if 'thumb_image' in child and child['thumb_image']['url']:
#                 if self._notice['src']['config'].get('auth'):
#                     child['thumb_image']['url'] = self.join_url_auth(child['thumb_image']['url'])
#                 img_children[str(pos)] = child['thumb_image']
#             ivt_children[str(pos)] = child['qty']
#
#             variant = {
#                 'product_id': product_id,
#                 'position': pos,
#                 'title': to_str(child['name']).replace('/', '-'),
#                 'sku': child['sku'] if child['sku'] else convert['sku'],
#                 'price': round(to_decimal(child_sale_price), 2) if to_decimal(child_sale_price) > 0 else 0,
#                 'compare_at_price': round(to_decimal(child_compare_price), 2) if child_compare_price and round(
#                     to_decimal(child_compare_price), 2) != round(to_decimal(child_sale_price), 2) else None,
#                 'weight': to_decimal(child['weight']) if to_decimal(child['weight']) > 0 else 0,
#                 'cost': get_value_by_key_in_dict(child, 'cost', None),
#                 'inventory_policy': 'deny' if child['manage_stock'] else 'continue',
#                 'inventory_management': 'shopify' if child['manage_stock'] else None,
#                 'taxable': False
#             }
#             if child.get('barcode'):
#                 variant['barcode'] = get_value_by_key_in_dict(child, 'barcode',
#                                                               get_value_by_key_in_dict(child, 'upc',
#                                                                                        get_value_by_key_in_dict(
#                                                                                            child, 'ean', '')))
#             else:
#                 variant['barcode'] = get_value_by_key_in_dict(convert, 'barcode',
#                                                               get_value_by_key_in_dict(convert, 'upc',
#                                                                                        get_value_by_key_in_dict(
#                                                                                            convert, 'ean', '')))
#             pos += 1
#             map_current = dict()
#             for row in child['attributes']:
#                 map_current[get_value_by_key_in_dict(row, 'option_id', row['option_code'])] = True
#
#             # diff two dict
#             map_empty = _map.copy()
#             for option_id, value in map_current.items():
#                 if option_id in map_empty:
#                     del map_empty[option_id]
#                 else:
#                     map_empty[option_id] = value
#             count_attr = 0
#             variant_option = dict()
#             for row in child['attributes']:
#                 if get_value_by_key_in_dict(row, 'option_id', row['option_code']) in _map:
#                     if count_attr >= 3:
#                         break
#                     variant[
#                         'option' + to_str(_map[get_value_by_key_in_dict(row, 'option_id', row['option_code'])])] = \
#                         row['option_value_name']
#                     variant_option[
#                         'option' + to_str(_map[get_value_by_key_in_dict(row, 'option_id', row['option_code'])])] = \
#                         row['option_value_name']
#                     count_attr += 1
#             if map_empty and len(map_empty):
#                 for remain_id, value in map_empty.items():
#                     variant['option' + to_str(value)] = 'No Value'
#             if not self.check_variant_exist(variant_option, list_variants):
#                 variants.append(variant)
#                 list_variants.append(variant_option)
#
#             number_variant_imported += 1
#         # endfor
#         # var_post_data['product']['variants'] = variants
#         # var_post_data['product']['options'] = options
#     #     var_response = self.api('products/' + to_str(product_id) + '.json', var_post_data, 'Put')
#
#     if not variants:
#         return True
#     new_variants = []
#     for old_var in list_old_variants:
#         for var in variants:
#             if var['sku'] == old_var['sku']:
#                 old_var['title'] = var['title']
#                 old_var['option1'] = var['option1']
#                 old_var['option2'] = var['option2']
#                 old_var['option3'] = var['option3']
#                 old_var['barcode'] = var['barcode']
#
#                 new_variants.append(old_var)
#     sort_variants = []
#     if len(variants) > 1:
#         # sorted_child = sorted(convert['children'], key=lambda i: i['position'])
#         for child in convert['children']:
#             for variant in new_variants:
#                 if child['sku'] == variant['sku']:
#                     sort_variants.append(variant)
#
#     new_options = []
#     for index in range(len(list_old_options)):
#         # list_old_options[index]
#         list_old_options[index]['name'] = options[index]['name']
#         list_old_options[index]['position'] = options[index]['position']
#         list_old_options[index]['values'] = options[index]['values']
#         new_options.append(list_old_options[index])
#     update_data = {
#         "product": {
#             "variants": sort_variants,
#             "options": new_options,
#         }
#     }
#     self.log(update_data, 'update_data')
# update_response = self.api('products/' + to_str(product_id) + '.json', update_data, 'PUT')


# update product image shopify
# # id_desc = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
# # self.log(id_desc, 'id_desc')
# # images = list()
# # main_image = None
# # list_image_children = []
# # if id_desc:
# # 	if convert['thumb_image']['url']:
# # 		main_image = self.process_image_before_import(convert['thumb_image']['url'],
# # 													  convert['thumb_image']['path'])
# # 		if main_image['url'] not in list_image_children:
# # 			if self._notice['src']['config'].get('auth'):
# # 				main_image['url'] = self.join_url_auth(main_image['url'])
# # 			if to_str(self._notice['src']['cart_type']) == 'bigcommerce':
# # 				main_image['url'] = self.URL_PROXY + to_str(main_image['url'])
# # 			image_data = self.resize_image(main_image['url'])
# # 			if image_data:
# # 				image_data['alt'] = convert['thumb_image']['label']
# # 				images.append(image_data)
# # 			else:
# # 				images.append({'src': main_image['url'], 'alt': convert['thumb_image']['label']})
# # 	for img_src in convert['images']:
# # 		if 'status' in img_src and not img_src['status']:
# # 			continue
# # 		image_process = self.process_image_before_import(img_src['url'], img_src['path'])
# # 		if image_process['url'] in list_image_children:
# # 			continue
# # 		if self._notice['src']['config'].get('auth'):
# # 			image_process['url'] = self.join_url_auth(image_process['url'])
# # 		if to_str(self._notice['src']['cart_type']) == 'bigcommerce':
# # 			image_process['url'] = self.URL_PROXY + to_str(image_process['url'])
# # 		image_data = self.resize_image(image_process['url'])
# # 		if image_data:
# # 			image_data['alt'] = img_src['label']
# # 			images.append(image_data)
# # 		else:
# # 			images.append({'src': image_process['url'], 'alt': img_src['label']})
# #
# # 	product_api = self.api('products/' + to_str(id_desc) + '.json')
# # 	product_api = json_decode(product_api)
# # 	product_desc = product_api.get('product')
# # 	if product_desc:
# # 		put_data = {
# # 			"product": {
# # 				"images": images
# # 			}
# # 		}
# # 		update_data = self.api('products/' + to_str(id_desc) + '.json', put_data, 'put')
# # 	else:
# # 		self.log(to_str(id_desc) + ":NOT UPDATE IMAGES", "update_status")
# return self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])


# update ORDER product bigcommerce (get map sai option_value)
if ord_items:
    for item in ord_items:
        item_data = dict()
        item_data['quantity'] = to_decimal(item['qty']) if to_decimal(item['qty']) > 0 else 0
        if to_decimal(item['price']) < 0 or to_decimal(item_data['quantity']) <= 0:
            continue
        product = self.select_map(self._migration_id, self.TYPE_PRODUCT, item['product']['id'], None,
                                  item['product']['code'])

        if not product:
            product_id = 0
        else:
            product_id = product['id_desc']
            pro_info_api = self.api('/products/' + to_str(product_id) + '.json')
            # self.log(product, 'pro_order')

            if pro_info_api:
                pro_info = json_decode(pro_info_api)
                self.log(pro_info, 'pro_info')
                if not pro_info:
                    product_id = 0
                elif pro_info.get('inventory_tracking') == 'simple' and to_decimal(
                        pro_info.get('inventory_level')) < to_decimal(item_data.get('quantity')):
                    if product:
                        value_product = json_decode(product['value'])
                        if value_product and product_id:
                            product_update = {
                                'inventory_level': item['qty'] + to_int(value_product.get('qty')) if to_decimal(
                                    value_product.get('qty')) >= 0 else 0,

                            }
                            async_request.append(
                                self.create_async_request_data('/products/' + to_str(product_id), product_update,
                                                               'PUT'))
                            self.log(async_request, "async_request_if")
                elif pro_info.get('inventory_tracking') == 'sku':
                    src_sku = item['product']['sku']
                    variants_info = self.api('/products/' + to_str(product_id) + '/skus.json')
                    self.log(variants_info, "variants_info")
                    if variants_info:
                        variants = json_decode(variants_info)
                        for var in variants:
                            if to_str(var['sku']).strip() == src_sku.strip() and to_decimal(
                                    var.get('inventory_level')) < to_decimal(item_data.get('quantity')):
                                product_update = {
                                    'inventory_level': to_int(item_data.get('quantity')) + to_int(
                                        var['inventory_level']),
                                }
                                if var['is_purchasing_disabled']:
                                    product_update['is_purchasing_disabled'] = False
                                # update_purchase[product_id] = var['id']
                                async_request.append(self.create_async_request_data(
                                    '/products/' + to_str(product_id) + '/skus/' + to_str(var['id']), product_update,
                                    'PUT'))
        if product_id:
            item_data['product_id'] = product_id
        item_data['name'] = item['product']['name']
        item_sku = item['product']['sku']
        if not item_sku or item_sku == '':
            if product:
                item_sku = product['code_desc'] if product['code_desc'] else product['id_desc']
            else:
                item_sku = self.convert_attribute_code(item['product']['name']) if item['product']['name'] and \
                                                                                   item['product'][
                                                                                       'name'] != '' else self.convert_attribute_code(
                    item['product']['code'])
        item_data['sku'] = item_sku
        # item_data['base_price'] = item['price']
        item_data['price_ex_tax'] = item['original_price'] if item['original_price'] else 0
        item_data['price_inc_tax'] = item['price']
        # item_data['base_total'] = item['total']
        # item_data['total_ex_tax'] = item_data['base_total']
        # item_data['total_inc_tax'] = item_data['base_total']
        item_data['product_options'] = list()
        if item['options'] and int(product_id) > 0:
            all_pro_opts_api = self.api('/products/' + to_str(product_id) + '/options.json')
            if all_pro_opts_api or to_str(all_pro_opts_api) != '':
                all_pro_opts = json.loads(all_pro_opts_api)
                # self.log(all_pro_opts, 'all_pro_opts')
                for item_option in item['options']:
                    option = dict()
                    option['id'] = get_row_value_from_list_by_field(all_pro_opts, 'display_name',
                                                                    item_option['option_name'], 'id')
                    option_id = get_row_value_from_list_by_field(all_pro_opts, 'display_name',
                                                                 item_option['option_name'], 'option_id')
                    self.log(item_option['option_value_name'] + '-pro-' + to_str(item['product']['id']), 'attr_value')
                    where = {
                        'migration_id': self._migration_id,
                        'type': self.TYPE_ATTR_VALUE,
                        'code_src': item_option['option_value_name'].lower() + '-pro-' + to_str(product_id)
                    }
                    list_attr_map = self.select_obj(TABLE_MAP, where)
                    list_attr_map_ids = list()
                    if list_attr_map['data']:
                        list_attr_map_ids = list(map(lambda x: x['id_desc'], list_attr_map['data']))
                    # self.log(list_attr_map_ids, 'list_attr_map')
                    option_values = json_decode(self.api('/options/' + to_str(option_id) + '/values.json'))
                    list_attr_ids = list(map(lambda x: x['id'], option_values)) if option_values else []
                    # self.log('/options/' + to_str(option_id) + '/values.json', 'option_values')
                    # self.log(option_values, 'option_values')
                    if len(list_attr_map_ids) > 1:
                        for attr_id in list_attr_map_ids:
                            if attr_id in list_attr_ids:
                                option['value'] = attr_id
                                # attr_value_ids = list(map(lambda x: x['id'], option_values))
                                # if attr_id in attr_value_ids:
                                # 	option['value'] = attr_id
                                break
                    else:
                        option['value'] = self.get_map_field_by_src(self.TYPE_ATTR_VALUE, None, item_option[
                            'option_value_name'].lower() + '-pro-' + to_str(product_id))
                    if not option['id'] or not option['value']:
                        continue
                    item_data['product_options'].append(option)
        all_pro_opts_api = self.api('/products/' + to_str(product_id) + '/options.json')

        all_pro_opts = json_decode(all_pro_opts_api)

        # self.log(item_data, 'item_data1')
        # self.log(all_pro_opts, 'all_pro_opts')
        if all_pro_opts:
            for item_option in all_pro_opts:
                if item_option['is_required'] and not get_row_from_list_by_field(item_data['product_options'], 'id',
                                                                                 item_option['id']):
                    option = dict()
                    option['id'] = item_option['id']
                    option_values = self.api('/options/' + str(item_option['option_id']) + '/values')
                    option_values = json_decode(option_values)
                    option['value'] = option_values[0]['id']
                    item_data['product_options'].append(option)
        items_data.append(item_data)
        self.log(items_data, 'item_data')

# check
^(2021/[0-1]{0,1}[0-1]{0,1}/[0-1]{0,1}[0-1]{0,1} [0-1]{0,1}[0-1]{0,1} ?:[0-1]{0,1}[0-9]{1,2}:[0-5][0-9] ?:) 

# update price and add related product, upsells, crosssell into metafields shopify
def check_product_import(self, convert, product, products_ext):
		# self.log(convert, 'pro_convert')
		product_id = self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
		if product_id:
			product_api = self.api('products/' + to_str(product_id) + '.json')
			product_data = json_decode(product_api)
			product_data = product_data.get('product')
			if not product_data:
				return True
			variant_data = product_data.get('variants')
			if variant_data and len(variant_data) == 1:
				variant_id = variant_data[0].get('id')
				if not variant_id:
					return True
				pro_price_update_data = {
					"variant": {
						'id': variant_id,
						'price': convert['price']
					}
				}
				self.api('/variants/' + to_str(variant_id) + '.json', pro_price_update_data, 'PUT')
				self.log(f"{convert['id']} | {convert['sku']} |{product_id} | {convert['price']}", 'pro_price_upate')

		# 	if convert['relate'].get('related_products'):
		# 		list_product_relate_id = list(map(lambda x: x['id'], convert['relate'].get('related_products')))
		# 		list_product_relate_id_target = list(filter(lambda x: x, [self.get_map_field_by_src(self.TYPE_PRODUCT, x, convert['code']) for x in list_product_relate_id]))
		# 		list_product_relate_id_target = [to_str(x) for x in list_product_relate_id_target]
		# 		# self.log(f"related: {convert['id']} | {list_product_relate_id_target}", 'list_related_pro')
		# 		if list_product_relate_id_target:
		# 			value = ', '.join(list_product_relate_id_target)
		# 			pro_related_metafield = {
		# 				"metafield": {
		# 					"key": "related_products",
		# 					"value": value,
		# 					"value_type": "string",
		# 					"namespace": "global"
		# 				}
		# 			}
		# 			self.api('products/' + to_str(product_id) + '/metafields.json', pro_related_metafield, 'Post')
		# 			self.log(f"{convert['id']} | {convert['sku']} |{product_id} | {pro_related_metafield}", 'pro_related')
		# 	if convert['relate'].get('up_sells'):
		# 		list_product_upsells_id = list(map(lambda x: x['id'], convert['relate'].get('up_sells')))
		# 		list_product_upsell_id_target = list(filter(lambda x: x, [self.get_map_field_by_src(self.TYPE_PRODUCT, x, convert['code']) for x in list_product_upsells_id]))
		# 		list_product_upsell_id_target = [to_str(x) for x in list_product_upsell_id_target]
		# 		# self.log(f"related: {convert['id']} | {list_product_upsell_id_target}", 'list_upsell_pro')
		# 		if list_product_upsell_id_target:
		# 			value = ', '.join(list_product_upsell_id_target)
		# 			pro_upsells_metafield = {
		# 				"metafield": {
		# 					"key": "up_sells",
		# 					"value": value,
		# 					"value_type": "string",
		# 					"namespace": "global"
		# 				}
		# 			}
		# 			self.api('products/' + to_str(product_id) + '/metafields.json', pro_upsells_metafield, 'Post')
		# 			self.log(f"{convert['id']} | {convert['sku']} |{product_id} | {pro_upsells_metafield}", 'pro_upsells')
		# 	if convert['relate'].get('cross_sells'):
		# 		list_product_cross_sells_id = list(map(lambda x: x['id'], convert['relate'].get('cross_sells')))
		# 		list_product_cross_sells_id_target = list(filter(lambda x: x, [self.get_map_field_by_src(self.TYPE_PRODUCT, x, convert['code']) for x in list_product_cross_sells_id]))
		# 		list_product_cross_sells_id_target = [to_str(x) for x in list_product_cross_sells_id_target]
		# 		# self.log(f"related: {convert['id']} | {list_product_cross_sells_id_target}", 'list_cross_pro')
		# 		if list_product_cross_sells_id_target:
		# 			value = ', '.join(list_product_cross_sells_id_target)
		# 			pro_cross_sells_metafield = {
		# 				"metafield": {
		# 					"key": "cross_sells",
		# 					"value": value,
		# 					"value_type": "string",
		# 					"namespace": "global"
		# 				}
		# 			}
		# 			self.api('products/' + to_str(product_id) + '/metafields.json', pro_cross_sells_metafield, 'Post')
		# 			self.log(f"{convert['id']} | {convert['sku']} |{product_id} | {pro_cross_sells_metafield}", 'pro_crosssells')
		return True #self.get_map_field_by_src(self.TYPE_PRODUCT, convert['id'], convert['code'])
    
# update image from srcset - shopify (anh hien thi theo kich thuoc man hinh)
    def process_description_before_import(self, convert, is_blog = False, is_page = False):
		theme_data = self.get_theme_data(is_blog=is_blog, is_page=is_page)
		description = convert['content']
		if not theme_data:
			theme_data = self.get_theme_data(True, is_blog, is_page)
		match = None
		if description:
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
				image_path = img_src[1]
				if self._notice['src']['cart_type'] == 'shopify':
					if ('http' or 'https') not in image_path:
						image_path = 'https://' + to_str(image_path).lstrip('//')
					if '?' in image_path:
						img_path = image_path.split('?')
						image_path = img_path[0]
					if image_path in links:
						continue
				links.append(image_path)
				if 'srcset' in img:
					image_from_srcset = re.findall(r"(srcset=[\"'](.*?)[\"'])", to_str(img))
					if image_from_srcset:
						list_image_from_srcset_data = image_from_srcset[0][1].split(',')
						if list_image_from_srcset_data:
							list_image_from_srcset = list(x.strip() for x in list_image_from_srcset_data)
							list_image_from_srcset = list(map(lambda x: x.split(' ')[0], list_image_from_srcset))
							for i in list_image_from_srcset:
								if i not in links:
									links.append(i)