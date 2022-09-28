from util import *

for asset in get_all_assets('assets'):
    registry_file = os.path.join(asset, 'updated.txt')
    if os.path.isfile(registry_file):
        os.remove(registry_file)