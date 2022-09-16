#!/usr/bin/env python
from __future__ import print_function
import sys

#local imports
from fximage import FXImage
from fximageobject import FXImageObject
import fxconnection
import fximageutils
import images_access
import time

def search_form(postgreSQL_pool,fromdate,todate):
    if fromdate is None:
        fromdate = "0"#"1546383600"
    if todate is None:
        todate = "2529874799"

    sqlquery = """SELECT description, count (*) FROM public.objects obj
        JOIN images img ON img.filefullname = obj.filefullname
        WHERE img.creationdate between {} and {}
        group by description order by description;""".format(fromdate,todate)

    conn = postgreSQL_pool.getconn()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(sqlquery)
    rows = cur.fetchall()
    descriptions=[]
    for row in rows :
        description = {}
        description['name'] = row[0]
        description['amount'] = row[1]
        descriptions.append(description)
    cur.close()
    postgreSQL_pool.putconn(conn)

    fromdate = time.strftime("%Y-%m-%d", time.gmtime(int(fromdate)))
    todate = time.strftime("%Y-%m-%d", time.gmtime(int(todate)))
    return fromdate,todate,descriptions;

def process_search_form(postgreSQL_pool,json_received):
    print("process_search_form entered",file=sys.stderr)
    use_coords = None
    bottomLeft = None
    topRight = None
    from_date = None
    to_date = None
    descriptions = None
    cameramodels = None
    offset = None
    next = None
    try:
        use_coords = json_received['use_coords']
        use_gps_coordinates = use_coords
        from_date = json_received['fromdate']
        to_date = json_received['todate']
        descriptions = json_received['descriptions']
        cameramodels = json_received['cameramodels']
        offset = json_received['offset']
        next = json_received['next']
    except(Exception) as error:
        print("Error while retrieving expected paramaetr in Json data {}".format(error),file=sys.stderr)

    print("Checking variables initialisation",file=sys.stderr)
    if bottomLeft is None:
        bottomLeft = [-180,90]
    if topRight is None:
        topRight = [180,90]
    if from_date is None:
        from_date = 0
    if to_date is None :
        to_date = 20000000
    if descriptions is None :
        descriptions = []
    if cameramodels is None :
        cameramodels = []
    if use_coords is None:
        use_coords = False
    if offset is None:
        offset = 0
        json_received['offset']=0
    if next is None:
        next = 50
        json_received['next']=50

    print("Done :  variables initialisation",file=sys.stderr)
    print("looking for images between {} and {} containing : ".format(from_date,to_date),file=sys.stderr)
    for desc in descriptions:
        print("{}".format(desc['name']))

    #Build the request
    sql = "select image_id, filefullname, filename, filepath, fileextensions, filesize, creationdate, lat, lon, thumbnail, to_be_deleted, model,comments, timestamp "

    for desc in descriptions:
        sql=sql+ ", {}s".format(desc['name'].replace(" ","_"))

    sql = sql + " from ( SELECT img.image_id, img.filefullname, img.filename, img.filepath, img.fileextensions, img.filesize, img.creationdate,img.lat, img.lon, thumbnail, to_be_deleted, model,comments,timestamp"

    for desc in descriptions:
        description_no_space = desc['name'].replace(" ","_")
        sql = sql + ", count(*) FILTER (WHERE obj.description = '{}') AS \"{}s\" ".format(desc['name'],description_no_space)

    sql = sql + " FROM images img JOIN objects obj ON img.image_id = obj.image_id GROUP BY img.image_id, img.filefullname, img.creationdate) as sub "

    sql = sql + " where"
    sql = sql + " to_be_deleted is not true"

    #define camera models
    if len(cameramodels) > 0:
        sql = sql + " AND ("
        cpt = 0
        for model in cameramodels:
          if cpt > 0 :
              sql = sql + " or "
          sql = sql + " model = '{}'".format(model['name'])
          cpt=cpt+1
        sql = sql + ")"

    #define date interval
    sql = sql + " AND creationdate between  {} AND {}".format(from_date,to_date)
    if(use_gps_coordinates):
        bottomLeft = json_received['bottomLeft']
        topRight = json_received['topRight']
        sql = sql + " AND ((lat between {} AND {}) and (lon between {} AND  {}))".format(bottomLeft[1],topRight[1],bottomLeft[0],topRight[0])

    #define number of elements
    for desc in descriptions:
        print(desc)
        description_no_space = desc['name'].replace(" ","_")
        sql=sql+ " and {}s ".format(description_no_space)
        if(desc['criteria']=="lessthan"):
            sql = sql + " < {}".format(desc['qty'])
        elif(desc['criteria']=="atleast"):
            sql = sql + " > {}".format(int(desc['qty'])-1)
        elif(desc['criteria']=="exactly"):
            sql = sql + " = {}".format(desc['qty'])
        else:
            sql = sql + " > 0"


    sql = sql + " order by creationdate desc"
    sql = sql + "  OFFSET {} ROWS FETCH NEXT {} ROWS ONLY".format(offset,next)

    print("SQL REQUEST created : ",file=sys.stderr)
    print(sql,file=sys.stderr)

    images = images_access.get_generic(postgreSQL_pool,sql)
    #print(sql)
    return images, offset, next, json_received;
