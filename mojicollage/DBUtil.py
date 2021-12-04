import psycopg2

#DATABASE_URL = 'postgres://mmhnrmajpuswzn:9a6a033064974661839f58fe8354452b2bb96619f0b138263f191e8266018947@ec2-44-193-111-218.compute-1.amazonaws.com:5432/d5pnku1euimvt3'
DATABASE_URL = 'host=ec2-44-193-111-218.compute-1.amazonaws.com\
    port=5432\
    dbname=d5pnku1euimvt3\
    user=mmhnrmajpuswzn\
    password=9a6a033064974661839f58fe8354452b2bb96619f0b138263f191e8266018947\
    sslmode=require'

def connect():
    return psycopg2.connect(DATABASE_URL)

def getData(con, sql):
    with con.cursor() as curs:
        curs.execute(sql)
        rows = curs.fetchall()
    return rows

