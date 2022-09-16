from __future__ import print_function # In python 2.7
import sys
from fximage import FXImage
from fximageobject import FXImageObject
import fxconnection
import fximageutils
import time
import logging
import psycopg2

def get_image_lot(postgreSQL_pool,list):
	sqlquery = """select image_id, filefullname, filename, filepath, fileextensions, filesize, creationdate, to_be_deleted, thumbnail,comments,othernames,timestamp  from images
		where image_id in %s"""

	conn = postgreSQL_pool.getconn()
	cur = conn.cursor()
	cur.execute(sqlquery,(list,))
	rows = cur.fetchall()
	images = []
	for row in rows :
		image = FXImage(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[9])
		image.to_be_deleted = row[7]
		image.thumbnail = row[8]
		image.othernames = row[10]
		image.timestamp = row[11]
		print("Other name contains : {}".format(image.othernames),file = sys.stderr)
		images.append(image )
	cur.close()
	postgreSQL_pool.putconn(conn)
	return images

def get_image_with_objects_by(postgreSQL_pool,id):
	img = get_image_by_id(postgreSQL_pool,id)

	#fetch ALL objects for the image from the database
	sqlquery = """SELECT objects_id, filefullname, bbox, description, confidence, analyzer, analyzer_version, x, y, w, h, image_id, derived_from_object,object_image_filename,face_id,text_found
	FROM  public.objects WHERE filefullname=%s;"""
	try:
		conn = postgreSQL_pool.getconn()
		conn.autocommit = True
		cur = conn.cursor()

		cur.execute(sqlquery,(img.filefullname,))
		rows = cur.fetchall()
		image_objects_descriptions = []
		for row in rows :
			
			img_obj = FXImageObject(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15])
			print("{} {} {} {}".format(img_obj.x,img_obj.y,img_obj.w,img_obj.h))
			image_objects_descriptions.append( img_obj )
		img.objs = image_objects_descriptions
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if cur is not None:
			cur.close()
		if conn is not None:
			postgreSQL_pool.putconn(conn)

	return img

def get_image_by_id(postgreSQL_pool,id):
	print("getting image by id", file=sys.stderr )
	sqlquery = "SELECT image_id, filefullname, filename, filepath, fileextensions, filesize, creationdate, to_be_deleted, thumbnail,comments,othernames,lat,lon FROM public.images WHERE image_id = %s;"
	conn = postgreSQL_pool.getconn()
	conn.autocommit = True
	cur = conn.cursor()
	cur.execute(sqlquery,(id,))
	rows = cur.fetchall()
	images = []
	for row in rows :
		#app.logger.info(row[1])
		img = FXImage(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[9])
		img.to_be_deleted = row[7]
		img.thumbnail = row[8]
		img.othernames = row[10]
		img.lat = row[11]
		img.lon = row[12]
		print("Other name contains : {}".format(img.othernames),file = sys.stderr)
		images.append( img )
	cur.close()
	postgreSQL_pool.putconn(conn)
	return images[0]

def list_images(postgreSQL_pool,offset,next):
	sqlquery = "SELECT image_id, filefullname, filename, filepath, fileextensions, filesize, creationdate,to_be_deleted,thumbnail FROM public.images WHERE (fileextensions='.jpg' or fileextensions='.png' or fileextensions='.jpeg'  or fileextensions='.tiff') order by creationdate OFFSET %s ROWS FETCH NEXT %s ROWS ONLY;"
	conn = postgreSQL_pool.getconn()
	conn.autocommit = True
	cur = conn.cursor()
	cur.execute(sqlquery,(offset,next))
	rows = cur.fetchall()
	images = []
	for row in rows :
		img = FXImage(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
		img.to_be_deleted = row[7]
		img.thumbnail = row[8]
		images.append(img )
	cur.close()
	postgreSQL_pool.putconn(conn)
	return images

def get_generic(postgreSQL_pool,sqlquery):
	print("get_generic entered",file=sys.stderr)
	try:
		conn = postgreSQL_pool.getconn()
		cur = conn.cursor()
		cur.execute(sqlquery,)
		rows = cur.fetchall()
		images = []
		for row in rows :
			image = FXImage(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[12])
			image.lat = row[7]
			image.lon = row[8]
			image.thumbnail= row[9]
			image.to_be_deleted= row[10]
			image.model = row[11]
			image.timestamp = "{}".format(row[13])
			images.append(image)
	except(Exception)as error:
		print("error while executing sql : {}".format(error),file = sys.stderr)
	finally:
		cur.close()
		postgreSQL_pool.putconn(conn)
	return images
