import { NextFunction, Request, Response, Router } from "express";
import { BaseRoute } from "./BaseRoute";
import {Image} from '../image';
import {PoolConfig, Pool} from "pg";
/**
 * / route
 *
 * @class User
 */
export class AlbumRoute extends BaseRoute {

  /**
   * Create the routes.
   *
   * @class IndexRoute
   * @method create
   * @static
   */
  public static create(router: Router, pg : Pool) {
    //log
    console.log("[AlbumRoute::create] Creating Album route.");
    //add home page route
    var albumRoutes : AlbumRoute = new AlbumRoute(pg);
    router.post("/v2/albums", (req: Request, res: Response, next: NextFunction) => {
       albumRoutes.index(req, res, next);
    });
    router.post("/v2/imagesforalbum", (req: Request, res: Response, next: NextFunction) => {
       albumRoutes.getImagesForAlbum(req, res, next);
    });
    router.put("/v2/addImageAlbumRel", (req: Request, res: Response, next: NextFunction) => {
      albumRoutes.AddImageAlbumRel(req, res, next);
    });
    router.put("/v2/deleteImageAlbumRel", (req: Request, res: Response, next: NextFunction) => {
      albumRoutes.DeleteImageAlbumRel(req, res, next);
    });
    router.get("/v2/album/:id", (req: Request, res: Response, next: NextFunction) => {
      albumRoutes.getAlbum(req, res, next);
    });
    router.put("/v2/albumupdate", (req: Request, res: Response, next: NextFunction) => {
      albumRoutes.updateAlbum(req, res, next);
    });
    router.put("/v2/albumadd", (req: Request, res: Response, next: NextFunction) => {
      albumRoutes.addAlbum(req, res, next);
    });
  }

  /**
   * Constructor
   *
   * @class AlbumRoute
   * @constructor
   */
  constructor(pg: Pool) {
    super(pg);
  }

  public index(req: Request, res: Response, next: NextFunction) {
    this.pg.query('SELECT album_id, title,comments FROM albums ORDER BY title ASC', (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })
  }


  public getImagesForAlbum(req: Request, res: Response, next: NextFunction) {
    var rel = req.body;
    console.log("received : "+rel.album_id)
    var query = 'SELECT image_id, thumbnail, creationdate from images where image_id in (select image_id from album_images_rel where album_id = $1 ) order by creationdate desc '
    this.pg.query(query, [rel.album_id], (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })
  }

  public addAlbum(req: Request, res: Response, next: NextFunction) {
    var rel = req.body;
    var title = rel.title;
    var comments = rel.comments;
    var query = 'INSERT INTO public.albums (title, comments)	VALUES ($1,$2)';
    this.pg.query(query, [title,comments], (err, result) => {
      if (err) {
        throw err
      }
      console.log(result.rows);
      res.status(200).json(result.rows);
    })
  }

  public getAlbum(req: Request, res: Response, next: NextFunction) {
    let album_id = req.params.id;
    console.log("received : "+ album_id)
    var query = 'SELECT album_id, title, comments from albums where album_id = $1'
    this.pg.query(query,[album_id], (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows[0])
    })
  }

  public updateAlbum(req: Request, res: Response, next: NextFunction) {
    var rel = req.body;
    console.log("received : "+ rel)

    var album_id = rel.album_id;
    var title = rel.title;
    var comments = rel.comments;


    var query = 'update albums set title = $1, comments=$2 where album_id =$3';
    console.log(query);
    this.pg.query(query,[title,comments,album_id], (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows[0])
    })
  }

  public AddImageAlbumRel(req: Request, res: Response, next: NextFunction) {
    var rel = req.body;
    var album_id = rel.album_id;
    var image_id = rel.image_id;
    var query = 'INSERT INTO public.album_images_rel (album_id, image_id)	VALUES ($1,$2)';
    this.pg.query(query, [album_id,image_id], (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })
  }



  public DeleteImageAlbumRel(req: Request, res: Response, next: NextFunction) {
    var rel = req.body;
    var album_id = rel.album_id;
    var image_id = rel.image_id;
    var query = 'DELETE from public.album_images_rel WHERE	album_id = $1 and image_id = $2';
    this.pg.query(query, [album_id,image_id] , (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })
  }

}
