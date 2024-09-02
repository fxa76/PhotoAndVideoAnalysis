import { NextFunction, Request, Response } from "express";
import {PoolConfig, Pool} from "pg";

/**
 * Constructor
 *
 * @class BaseRoute
 */
export class BaseRoute {
  pg : Pool;
  /**
   * Constructor
   *
   * @class BaseRoute
   * @constructor
   */
  constructor( pg : Pool) {
      this.pg = pg;
  }


  replaceAll(target:any,search:string, replacement:string):string {
      return target.replace(new RegExp(search, 'g'), replacement)
  };

  build_request(param:any):string{
    console.log("received param " + param.sources);

    var offset = param.offset;
    var next = param.next;

    var bottomLeft = param.bottomLeft;
    var topRight = param.topRight;
    var use_coords = param.use_coords;
    var gps_is_null = param.gpsIsNull;

    var from_date = param.fromdate;
    var to_date = param.todate;
    var date_is_null = param.dateIsNull;

    var descriptions = param.descriptions;
    var cameramodels = param.cameramodels;
    var fileformats = param.fileformats;
    var sources = param.sources;

    var comments = param.comments;


    //only use the join with objects if looking for objects
    var sql = "";
    if( descriptions !=null && descriptions.length > 0 ){
      sql = " from ( SELECT img.image_id, img.source, img.filefullname, img.filename, img.filepath, img.fileextensions, img.filesize, img.creationdate,img.lat, img.lon,img.to_be_deleted, img.model,img.coord_from_exif, img.thumbnail "

      console.log("object descriptions")
      descriptions.forEach(function(desc:any){
        console.log("description received : "+ JSON.stringify(desc))
        var description_no_space = desc.description.replace(new RegExp(" ", 'g'), "_");
        sql = sql + ", count(*) FILTER (WHERE obj.description = '"+desc.description+"') AS \""+description_no_space+"s\" "
      })

      sql = sql + " FROM images img JOIN objects obj ON img.image_id = obj.image_id GROUP BY img.image_id, img.filefullname, img.creationdate) as sub "
    }
    else{
      sql =" from images "
    }
      //Define the WHERE clause
      sql = sql + " where to_be_deleted != true"

      if (comments != null && comments.length>0){
        sql = sql + " and comments ~ '"+comments+"'"
      }

      //define date interval
      console.log("date interval")
      if(from_date!= null && to_date != null && date_is_null == false){
        sql = sql + " AND creationdate between " + from_date + " AND " + to_date
      }
      else if( date_is_null == true){
        sql = sql + " AND creationdate is null "
      }

      //define coordinate usage
      console.log("use coords")
      if(use_coords && !gps_is_null){
        sql = sql + " AND ((lat between "+bottomLeft[1]+" AND "+topRight[1]+") and (lon between "+bottomLeft[0]+" AND  "+topRight[0]+"))"
      }
      else if (gps_is_null){
        sql = sql + " AND (lat is null AND lon is null) "
      }

      //define camera models
      console.log("camera models")
      if (cameramodels !=null && cameramodels.length > 0){
          sql = sql + " AND (";
          var cpt = 0;
          cameramodels.forEach(function(model:any){
            if (cpt > 0) {
                sql = sql + " or ";
            }
            sql = sql + " model = '"+model.name+"'"
            cpt=cpt+1;
          });
          sql = sql + ")"
      }

      if (fileformats !=null && fileformats.length > 0){
          sql = sql + " AND (";
          var cpt = 0;
          fileformats.forEach(function(fileformat:any){
            if (cpt > 0) {
                sql = sql + " or ";
            }
            sql = sql + " fileextensions = '"+fileformat.name+"'"
            cpt=cpt+1;
          });
          sql = sql + ")"
      }

      if (sources !=null && sources.length > 0){
        sql = sql + " AND (";
        var cpt = 0;
        sources.forEach(function(source:any){
          if (cpt > 0) {
              sql = sql + " or ";
          } 
          sql = sql + '"source" = '+"'"+source.name+"'"
          cpt=cpt+1;
        });
        sql = sql + ")"
    }

      //define number of objects
      console.log("object descriptions")
      if (descriptions!=null){
        descriptions.forEach(function(desc:any){
          console.log(desc)
          var description_no_space = desc.description.replace(new RegExp(" ", 'g'), "_");
          sql=sql+ " and "+description_no_space+"s "
          if(desc.criteria=="lessthan"){
              sql = sql + " < "+desc.qty
          }else if(desc.criteria=="atleast"){
              sql = sql + " > "+ (parseInt(desc.qty)-1)
          }else if(desc.criteria=="exactly"){
              sql = sql + " = "+desc.qty
          }else{
              sql = sql + " > 0"
            }
        });
      }

      //use timestamp instead of creation date as timestamp can be modified in interface to reorder pictures
      sql = sql + " order by timestamp desc"

      console.log("from part of sql : "+sql)
      return sql
  }
}
