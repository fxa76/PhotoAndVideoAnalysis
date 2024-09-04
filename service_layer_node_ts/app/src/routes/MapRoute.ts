import { NextFunction, Request, Response, Router } from "express";
import { BaseRoute } from "./BaseRoute";
import {Image} from '../image';
import {PoolConfig, Pool} from "pg";
/**
 * / route
 *
 * @class User
 */
export class MapRoute extends BaseRoute {

  /**
   * Create the routes.
   *
   * @class IndexRoute
   * @method create
   * @static
   */
  public static create(router: Router, pg : Pool) {
    //log
    console.log("[IndexRoute::create] Creating Map route.");
    //add home page route
    var mapRoutes : MapRoute = new MapRoute(pg);
    router.post("/v2/map", (req: Request, res: Response, next: NextFunction) => {
       mapRoutes.index(req, res, next);
    });
    router.get("/v2/map-mock", (req: Request, res: Response, next: NextFunction) => {
       mapRoutes.mock(req, res, next);
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
   * The home page route return all the data points corresponding to the frompart filled by search parameters.
   *
   * @class IndexRoute
   * @method index
   * @param req {Request} The express Request object.
   * @param res {Response} The express Response object.
   * @next {NextFunction} Execute the next method.
   */
  public index(req: Request, res: Response, next: NextFunction) {
    //nullify offset and next so the map is not limited to what the image page can show.

    var fromPart = this.build_request(req.body);

    console.log(fromPart);

    this.pg.query('SELECT image_id, lat,lon,coord_from_exif,timestamp '+ fromPart, (err, result) => {
      if (err) {
        throw err
      }
      res.status(200).json(result.rows)
    })
  }

  /**
   * a mock for the map data returning only one image point
   *
   * @class IndexRoute
   * @method index
   * @param req {Request} The express Request object.
   * @param res {Response} The express Response object.
   * @next {NextFunction} Execute the next method.
   */
  public mock(req: Request, res: Response, next: NextFunction) {
      res.json([{image_id:1234,lat:10,lon:10,coord_from_exif:false}])
  }
}
