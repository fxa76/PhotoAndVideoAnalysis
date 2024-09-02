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
export class ImageRoute extends BaseRoute {

  /**
   * Create the routes.
   *
   * @class IndexRoute
   * @method create
   * @static
   */
  public static create(router: Router, pg : Pool) {
    //log
    console.log("[IndexRoute::create] Creating Image route.");
    //add home page route
    var imageRoutes : ImageRoute = new ImageRoute(pg);
    router.post("/v2/images", (req: Request, res: Response, next: NextFunction) => {
       imageRoutes.getImages(req, res, next);
    });
    router.post("/v2/imagestimeline", (req: Request, res: Response, next: NextFunction) => {
       imageRoutes.getImagesTimeline(req, res, next);
    });
    router.post("/v2/imagestimebar", (req: Request, res: Response, next: NextFunction) => {
       imageRoutes.getImagesTimeBar(req, res, next);
    });
    router.get("/v2/image/:id", (req: Request, res: Response, next: NextFunction) => {
       imageRoutes.getImage(req, res, next);
    });
    router.post("/v2/getImagesWithFaces", (req: Request, res: Response, next: NextFunction) => {
       imageRoutes.getImagesWithFaces(req, res, next);
    });
    router.get("/v2/duplicates", (req: Request, res: Response, next: NextFunction) => {
       imageRoutes.getDuplicates(req, res, next);
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
  public getImages(req: Request, res: Response, next: NextFunction) {
    console.log(req.query);

    var fromPart = this.build_request(req.body);

    let offset = req.body.offset
    let next_offset = req.body.next

    var sql = 'SELECT * '+ fromPart;

    if(offset != null && next_offset !=null){
      sql = sql + "  OFFSET "+offset+" ROWS FETCH NEXT "+next_offset+" ROWS ONLY"
    }

    console.log("running query")
    this.pg.query(sql, (err, result) => {
      if (err) {
        throw err
      }
      console.log("returning results")
      res.status(200).json(result.rows)
      console.log("returned values")
    })

  }

  public getImagesTimeline(req: Request, res: Response, next: NextFunction) {
    console.log(req.query);

    var sql = `SELECT date_trunc('months', timestamp) as date, count(*) as value from images
              where timestamp is not null
              group by date
              order by date asc`;

    this.pg.query(sql, (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })

  }

  public getImagesTimeBar(req: Request, res: Response, next: NextFunction) {
    console.log(req.query);

    var sql = `SELECT date_trunc('years', timestamp) as date from images`;

    this.pg.query(sql, (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })

  }

  public getDuplicates(req: Request, res: Response, next: NextFunction){
    var sql = `select duplicates from
        (
        	SELECT sha512, count(*) AS c,json_agg(json_build_object('image_id', image_id,'thumbnail',thumbnail))as duplicates
        	FROM Images where SHA512 is not null
        		GROUP BY sha512
        		ORDER BY c DESC
        ) dupli_req
        where c >1 OFFSET 0 ROW FETCH NEXT 50 ROWS ONLY`

    this.pg.query(sql, (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json( result.rows)
    })
  }

  public getImagesWithFaces(req: Request, res: Response, next: NextFunction){
    console.log(req.query);

    var sql = `select * from images where image_id in (select image_id from (
        	SELECT img.image_id, img.filefullname, img.creationdate,
        	  count(*) FILTER (WHERE obj.description = 'face' and obj.face_id=0  and obj.face_id_iteration = 0) AS "persons1",
        	  count(*) FILTER (WHERE obj.description = 'face' and obj.face_id=11 and obj.face_id_iteration = 0) AS "persons2"
        	FROM images img
        	JOIN objects obj
        	ON img.image_id = obj.image_id
        	GROUP BY img.image_id, img.filefullname, img.creationdate
        	) as sub
        Where persons1 >0 and persons2 >0
        )
        order by creationdate desc`

    this.pg.query(sql, (err, result) => {
        if (err) {
          throw err
        }
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
  public getImage(req: Request, res: Response, next: NextFunction) {
    console.log(req.query);
    let id = req.params.id;
    var sql = "SELECT image_id, filefullname, filename, filepath, fileextensions, filesize, creationdate, lat, lon, to_be_deleted, favorite, coord_from_exif, thumbnail, source, model, duplicate_of_image_id, othernames, comments, timestamp FROM public.images where image_id = "+id;
    this.pg.query(sql, (err, result) => {
      if (err) {
        throw err
      }
      //var img =result.rows[0];
      //img.img_base64= "data:image/jpg;base64,"+fs.readFileSync(img.filefullname,'base64');
      res.status(200).json(result.rows[0])
    })

  }

}
