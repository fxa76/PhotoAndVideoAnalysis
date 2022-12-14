import { NextFunction, Request, Response, Router } from "express";
import { BaseRoute } from "./BaseRoute";
import {Image} from '../image';
import {PoolConfig, Pool} from "pg";
/**
 * / route
 *
 * @class User
 */
export class SearchRoute extends BaseRoute {

  /**
   * Create the routes.
   *
   * @class IndexRoute
   * @method create
   * @static
   */
  public static create(router: Router, pg : Pool) {
    //log
    console.log("[IndexRoute::create] Creating Search route.");
    //add home page route
    var searchRoutes : SearchRoute = new SearchRoute(pg);
    router.post("/v2/searchObjects", (req: Request, res: Response, next: NextFunction) => {
       searchRoutes.searchObjects(req, res, next);
    });
    router.post("/v2/searchModels", (req: Request, res: Response, next: NextFunction) => {
       searchRoutes.searchModels(req, res, next);
    });
    router.post("/v2/searchFileFormats", (req: Request, res: Response, next: NextFunction) => {
       searchRoutes.searchFileFormats(req, res, next);
    });

  }

  /**
   * Constructor
   *
   * @class IndexRoute
   * @constructor
   */
  constructor(pg: Pool) {
    super(pg);
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
  public searchObjects(req: Request, res: Response, next: NextFunction) {

    var fromPart = this.build_request(req.body);

    var sql = 'SELECT description,count(image_id) as amount from objects obj where obj.image_id in (( select image_id ' + fromPart + ' )) group by description'
    console.log("" + sql);

    this.pg.query( sql, (err, result) => {
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
  public searchModels(req: Request, res: Response, next: NextFunction) {
    //nullify offset and next so the search is not limited to what the image page can show.
    req.body.offset=null;
    req.body.next=null;
    var fromPart = this.build_request(req.body);

    var sql = 'SELECT model as name,count(image_id) as count from images where image_id in (( select image_id ' + fromPart + ' )) group by model'
    console.log("" + sql);

    this.pg.query( sql, (err, result) => {
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
  public searchFileFormats(req: Request, res: Response, next: NextFunction) {
    //nullify offset and next so the search is not limited to what the image page can show.
    req.body.offset=null;
    req.body.next=null;
    req.body.use_coords=false;
    var fromPart = this.build_request(req.body);

    var sql = 'SELECT fileextensions as name,count(image_id) as count from images where image_id in (( select image_id ' + fromPart + ' )) group by fileextensions'
    console.log("" + sql);

    this.pg.query( sql, (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })
  }
}
