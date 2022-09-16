import { NextFunction, Request, Response, Router } from "express";
import { BaseRoute } from "./BaseRoute";
import {Image} from '../image';
import {PoolConfig, Pool} from "pg";
import fs from 'fs';

/**
 * / route
 *
 * @class User
 */
export class FaceRoute extends BaseRoute {

  /**
   * Create the routes.
   *
   * @class IndexRoute
   * @method create
   * @static
   */
  public static create(router: Router, pg : Pool) {
    //log
    console.log("[IndexRoute::create] Creating Face route.");
    //add home page route
    var faceRoutes : FaceRoute = new FaceRoute(pg);

    router.get("/v2/list_objects_for_image_id/:id", (req: Request, res: Response, next: NextFunction) => {
       faceRoutes.listObjectsForImageId(req, res, next);
    });

    router.post("/v2/list_distinct_faces", (req: Request, res: Response, next: NextFunction) => {
       faceRoutes.index(req, res, next);
    });
    router.post("/v2/list_distinct_face_iteration", (req: Request, res: Response, next: NextFunction) => {
       faceRoutes.getFaceIdForIterationId(req, res, next);
    });
    router.get("/v2/hideFaceIdForIterationId/:iteration/:id", (req: Request, res: Response, next: NextFunction) => {
       faceRoutes.hideFaceIdForIterationId(req, res, next);
    });
    router.post("/v2/list_faces", (req: Request, res: Response, next: NextFunction) => {
       faceRoutes.getFaces(req, res, next);
    });
  }


  /**
   * The home page route.
   *
   * @class IndexRoute
   * @method index
   * @param req {Request} The express Request object.
   * @param res {Response} The express Response object.
   * @next {NextFunction} Execute the next method.
   */
  public index(req: Request, res: Response, next: NextFunction) {
    //console.log(req.query);
    var fromPart = this.build_request(req.body);

    let offset = req.body.offset;
    let next_offset = req.body.next;

    /*var sql = `SELECT distinct on (obj.face_id,obj.face_id_iteration)
      objects_id, obj.image_id, object_image_filename, obj.face_id, img.creationdate,obj.face_id_iteration as iteration
      FROM public.objects as obj
      JOIN images as img
      ON img.image_id = obj.image_id
      JOIN public.face_id face
      ON obj.face_id = face.face_id AND obj.face_id_iteration = face.face_id_iteration
      WHERE obj.face_id is not null AND (hidden = false or hidden is null)
      AND obj.image_id in (( select image_id ` + fromPart + ` ))
      ORDER BY obj.face_id_iteration, obj.face_id, img.creationdate desc`
      */
      var sql = `SELECT distinct on (obj.face_id,obj.face_id_iteration)
        objects_id, obj.image_id, object_image_filename, obj.face_id, img.creationdate,obj.face_id_iteration as iteration
        FROM public.objects as obj
        JOIN images as img
        ON img.image_id = obj.image_id
        JOIN public.face_id face
        ON obj.face_id = face.face_id AND obj.face_id_iteration = face.face_id_iteration
        WHERE obj.face_id is not null AND (hidden = false or hidden is null)
        ORDER BY obj.face_id_iteration, obj.face_id, img.creationdate desc`

    if(offset != null && next_offset !=null){
      sql = sql + "  OFFSET "+offset+" ROWS FETCH NEXT "+next_offset+" ROWS ONLY"
    }

    console.log(sql);
    this.pg.query(sql, (err, result) => {
      if (err) {
        throw err
      }
      result.rows.forEach(function(row){
        var filepath =  "/pictures_work/faceschip/"+row.object_image_filename;
        try{
          row.image = "data:image/jpg;base64,"+fs.readFileSync(filepath,'base64');
        }
        catch(e) {
          console.log(row)
          console.log(e);
        }
      })
      res.status(200).json(result.rows)
    })

  }

  /**
   * The home page route.
   *
   * @class IndexRoute
   * @method index
   * @param req {Request} The express Request object.
   * @param res {Response} The express Response object.
   * @next {NextFunction} Execute the next method.
   */
  public getFaceIdForIterationId(req: Request, res: Response, next: NextFunction) {
    //n/:iteration/:id/:offset/:next
    console.log("getFaceIdForIterationId##############");


    var fromPart = this.build_request(req.body);

    let id = req.body.id;
    let iteration = req.body.iteration;
    let offset = req.body.offset;
    let next_offset = req.body.next;

    var sql = `SELECT obj.objects_id, obj.filefullname, obj.description, obj.image_id,obj.analyzer_version, obj.derived_from_object, obj.object_image_filename, img.creationdate
      FROM public.objects obj
      Join public.images img
      on img.filefullname = obj.filefullname
      where obj.description = 'face' and face_id = `+id+` and face_id_iteration=`+iteration+` AND obj.image_id in (( select image_id ` + fromPart + ` ))
      order by img.creationdate desc`

    if(offset != null && next_offset !=null){
      sql = sql + "  OFFSET "+offset+" ROWS FETCH NEXT "+next_offset+" ROWS ONLY"
    }
    console.log(sql);

    this.pg.query(sql, (err, result) => {
      if (err) {
        throw err
      }
      result.rows.forEach(function(row){
        var filepath =  "/pictures_work/faceschip/"+row.object_image_filename;
        try{
          row.image = "data:image/jpg;base64,"+fs.readFileSync(filepath,'base64');
        }
        catch(e) {
          console.log(row)
          console.log(e);
        }
      })
      res.status(200).json(result.rows)
    })

  }

  public getFaces(req: Request, res: Response, next: NextFunction) {
    console.log("getFaces#######################");
    var fromPart = this.build_request(req.body);

    let offset = req.body.offset;
    let next_offset = req.body.next;

    var sql= `SELECT objects_id, obj.image_id, object_image_filename, obj.face_id, img.creationdate,obj.face_id_iteration as iteration
      FROM public.objects as obj
      JOIN images as img
      ON img.image_id = obj.image_id
      WHERE obj.description = 'face' AND obj.image_id in (( select image_id ` + fromPart + ` ))
      ORDER BY img.creationdate desc `

    if(offset != null && next_offset !=null){
      sql = sql + "  OFFSET "+offset+" ROWS FETCH NEXT "+next_offset+" ROWS ONLY"
    }
    console.log(sql);

    this.pg.query(sql, (err, result) => {
      if (err) {
        throw err
      }
      result.rows.forEach(function(row){
        var filepath =  "/pictures_work/faceschip/"+row.object_image_filename;
        try{
          row.image = "data:image/jpg;base64,"+fs.readFileSync(filepath,'base64');
        }
        catch(e) {
          console.log(row)
          console.log(e);
        }
      })
      res.status(200).json(result.rows)
    })

  }

  /**
   * The home page route.
   *
   * @class IndexRoute
   * @method index
   * @param req {Request} The express Request object.
   * @param res {Response} The express Response object.
   * @next {NextFunction} Execute the next method.
   */
  public hideFaceIdForIterationId(req: Request, res: Response, next: NextFunction) {
    console.log(req.query);
    let id = req.params.id;
    let iteration = req.params.iteration;

    var sql = `UPDATE public.face_id
	   SET hidden=true
     where face_id = $1 and face_id_iteration= $2`

     console.log(sql);

    this.pg.query(sql,[id,iteration], (err, result) => {
      if (err) {
        throw err
      }
      result.rows.forEach(function(row){
        var filepath =  "/pictures_work/faceschip/"+row.object_image_filename;
        row.image = "data:image/jpg;base64,"+fs.readFileSync(filepath,'base64');
      })
      res.status(200).json(result.rows)
    })

  }

   /**
   * The home page route.
   *
   * @class IndexRoute
   * @method index
   * @param req {Request} The express Request object.
   * @param res {Response} The express Response object.
   * @next {NextFunction} Execute the next method.
   */
  public listObjectsForImageId(req: Request, res: Response, next: NextFunction) {
    console.log(req.query);
    let id = req.params.id;

    console.log("List objects ")

    var sql = `select * from Objects
     where image_id = $1`

     console.log(sql);

    this.pg.query(sql,[id], (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })

  }

}
