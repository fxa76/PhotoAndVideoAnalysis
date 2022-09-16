import { NextFunction, Request, Response, Router } from "express";
import { BaseRoute } from "./BaseRoute";
import {Image} from '../image';
import {PoolConfig, Pool} from "pg";

/**
 * / route
 *
 * @class User
 */
export class IndexRoute extends BaseRoute {

  /**
   * Create the routes.
   *
   * @class IndexRoute
   * @method create
   * @static
   */
  public static create(router: Router, pg : Pool) {
    //log
    console.log("[IndexRoute::create] Creating index route.");
    //add home page route
    var index = new IndexRoute(pg);
    router.get("/", (req: Request, res: Response, next: NextFunction) => {
      index.index(req, res, next);
    });
    router.get("/health", (req: Request, res: Response, next: NextFunction) => {
      index.health(req, res, next);
    });
  }

  /**
   * Constructor
   *
   * @class IndexRoute
   * @constructor
   */
  constructor( pg : Pool) {
    super( pg);
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
      res.send("API to get access to image data please refer to documentation or check project's github page.<a href=''>here</a>");
  }


  public health(req: Request, res: Response, next: NextFunction) {
      res.send("");
  }
}
