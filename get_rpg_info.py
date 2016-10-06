import csv
import time
import requests
from bs4 import BeautifulSoup


def get_val(tag, term):
	try:
		val = tag.find(term)['value'].encode('ascii', 'ignore')
	except:
        	val = 'NaN'
    	return val


# below commented is the nonworking base I tried, need to try the commented one below it:
# base = 'http://www.rpggeek.com/xmlapi2/thing?id={}&type=rpg&stats=1'
# base = 'http://www.rpggeek.com/xmlapi2/thing?id={}&stats=1'
base = 'http://www.rpggeek.com/xmlapi2/family?type=rpg&id={}&stats=1'

with open('ids.txt') as f:
    ids = [line.strip() for line in f.readlines()]
split = 30
f = open('rpgs.csv', 'w')
writer = csv.writer(f)
writer.writerow(('id', 'type', 'name', 'rank', 'users_rated', 'average_rating', 
                 'bayes_average_rating', 'total_owners', 'total_traders', 'total_wanters',
                 'total_wishers', 'total_comments', 'total_weights', 'average_weight',
                 'rpgfamily', 'rpgsystem', 'rpgmechanic', 'rpghonor', 'geekitem_name'))
for i in range(0, len(ids), split):
    url = base.format(','.join(ids[i:i+split]))
    print('Requesting {}'.format(url))
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'xml')
    items = soup.find_all('item')
    for item in items:
        gid = item['id']
        gtype = item['type']
        gname = get_val(item, 'name')
        grpgfamily = get_val(item, 'rpgfamily')
        grpgsystem = get_val(item, 'rpgsystem')
        grpgmechanic = get_val(item, 'rpgmechanic')
        grpghonor = get_val(item, 'rpghonor')
        ggeekitem_name = get_val(item, 'geekitem_name')
        grank = get_val(item, 'rank')
        usersrated = get_val(item.statistics.ratings, 'usersrated')
        avg = get_val(item.statistics.ratings, 'average')
        bayesavg = get_val(item.statistics.ratings, 'bayesaverage')
        owners = get_val(item.statistics.ratings, 'owned')
        traders = get_val(item.statistics.ratings, 'trading')
        wanters = get_val(item.statistics.ratings, 'wanting')
        wishers = get_val(item.statistics.ratings, 'wishing')
        numcomments = get_val(item.statistics.ratings, 'numcomments')
        numweights = get_val(item.statistics.ratings, 'numweights')
        avgweight = get_val(item.statistics.ratings, 'averageweight')
        # desc = item.description.text.encode('ascii', 'ignore')
        writer.writerow((gid, gtype, gname, grank, , grpgfamily, grpgsystem, grpgmechanic, grpghonor, ggeekitem_name,
                         usersrated, avg, bayesavg, owners, traders, wanters, wishers, numcomments,
                         numweights, avgweight))
    time.sleep(2)
f.close()

