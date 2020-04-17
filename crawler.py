import semidbm, boto3, json, concurrent.futures

s3 = boto3.client('s3')

def s3folders(bucket, prefix):
    response = s3.list_objects(
        Bucket=bucket,
        Prefix=prefix,
        Delimiter='/')
    return [p['Prefix'] for p in response.get('CommonPrefixes', [])]

def s3ips(bucket, key):
    response = s3.select_object_content(
        Bucket=bucket,
        Key=key,
        ExpressionType='SQL',
        Expression='select ip, piwik_ip from s3object',
        InputSerialization={'Parquet': {}},
        OutputSerialization = {'JSON': {}})

    records = []
    for event in response['Payload']:
        if 'Records' in event:
            records.append(event['Records']['Payload'])

    entries = [json.loads(line) for line in b''.join(records).splitlines()]
    return entries

def s3files(bucket, prefix):
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        if 'Contents' not in page:
            # Data for the given prefix does not exist.
            continue
        for obj in page['Contents']:
            s3_filepath = obj['Key']
            yield s3_filepath

def main():
    db_ips = semidbm.open('ips.db', 'c')
    db_mrk = semidbm.open('mrk.db', 'c')
    bucket = 'tvsquared-userdata'
    siteIdPrefixes = s3folders(bucket, 'collector-tng-pre/visit/')

    executor = concurrent.futures.ThreadPoolExecutor()
    for prefix in siteIdPrefixes:
        print(prefix)
        if prefix.encode() in db_mrk:
            print(' skipping')
            continue
        parquetPrefixes = sorted(s3files(bucket, prefix), reverse=True)[:1000]
        print(' got %d files' % len(parquetPrefixes))
        parquetPrefixes = [p for p in parquetPrefixes if p.encode() not in db_ips]
        print(' processing %d files' % len(parquetPrefixes))
        c = 0
        for parquetPrefix, ips in executor.map(lambda p: [p, s3ips(bucket, p)], parquetPrefixes):
            c += 1
            db_ips[parquetPrefix] = ','.join([
                ':'.join([ip.get('ip') or '', ip.get('piwik_ip') or ''])
                for ip in ips
            ])
            print(' {}/{}'.format(c, len(parquetPrefixes)), end='\r')
        db_mrk[prefix] = '1'
        print(' done storing')

main()
