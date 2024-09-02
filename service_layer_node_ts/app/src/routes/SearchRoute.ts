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
    router.post("/v2/searchSources", (req: Request, res: Response, next: NextFunction) => {
      searchRoutes.searchSources(req, res, next);
   });
   router.post("/v2/searchCountTotal", (req: Request, res: Response, next: NextFunction) => {
    searchRoutes.searchCountTotal(req, res, next);
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

    var sql = 'SELECT description,count(image_id) as amount from objects obj where obj.image_id in (( select image_id ' + fromPart + ' )) group by description order by description asc'
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

    var sql = 'SELECT model as name,count(image_id) as count from images where image_id in (( select image_id ' + fromPart + ' )) group by name order by name asc'
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

    var sql = 'SELECT fileextensions as name,count(image_id) as count from images where image_id in (( select image_id ' + fromPart + ' )) group by name order by name asc'
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
  public searchSources(req: Request, res: Response, next: NextFunction) {
    //nullify offset and next so the search is not limited to what the image page can show.
    req.body.offset=null; 
    req.body.next=null;
    req.body.use_coords=false;
    var fromPart = this.build_request(req.body);

    var sql = 'SELECT "source" as name,count(image_id) as count from images where image_id in (( select image_id ' + fromPart + ' )) group by name order by name asc'
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
  public searchCountTotal(req: Request, res: Response, next: NextFunction) {
    //nullify offset and next so the search is not limited to what the image page can show.
    req.body.offset=null; 
    req.body.next=null;
    req.body.use_coords=false;
    var fromPart = this.build_request(req.body);

    var sql = 'SELECT count(image_id) as count from images where image_id in (( select image_id ' + fromPart + ' ))'
    console.log("" + sql);

    this.pg.query( sql, (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows[0].count)
    })
  }
}
