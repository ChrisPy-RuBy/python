import semidbm, re, collections

siteid_results = collections.defaultdict(lambda: {'total': 0, 'sameip': 0})
db_ips = semidbm.open('ips.db', 'r')
for prefix in db_ips:
    siteid = re.search('site_id=(.+?)/', prefix.decode()).groups(1)[0]
    ips = [s.split(':') for s in db_ips[prefix].decode().split(',')]

    siteid_results[siteid]['total'] += len(ips)
    siteid_results[siteid]['sameip'] += len([i for i in ips if i[0] == i[1]])

print('siteid', 'total', 'sameip', 'ratio', sep='\t')
for siteid, result in siteid_results.items():
    total, sameip = result['total'], result['sameip']
    print(siteid, total, sameip, sameip / total * 100, sep='\t')
