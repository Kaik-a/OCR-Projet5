"""This file is used to store constants of the program"""

from os import getcwd

# SQL
DATABASE = 'test'  # name of user's databae
FIRST_USE_SCRIPT = getcwd() + '/model/MCD.sql'  # script to format database

# HTTP
OPENFOODFACT_URL = 'https://fr.openfoodfacts.org/'
CATEGORIES_JSON = OPENFOODFACT_URL + 'categories.json'  # url of categories
STORES_JSON = OPENFOODFACT_URL + 'stores.json'  # url of stores
SEARCH_URL = OPENFOODFACT_URL + 'cgi/search.pl'
BASE_SEARCH_PARAMS = {'action': 'process',
                      'tagtype_0': 'categories',
                      'tagcontains_0': 'contains',
                      'tag_0': 'test',
                      'page_size': 1000,
                      'sort_by': 'unique_scans_n',
                      'json': 1}
# Presets
GIVEN_CATEGORIES = ['Boissons',  # Categories preset
                    'Fromages',
                    'Plats préparés',
                    'Snacks',
                    'Viandes']
ITEM_DISPLAYED = 10  # Number of items displayed while looking for bad product
SEPARATION = "################################################################"
