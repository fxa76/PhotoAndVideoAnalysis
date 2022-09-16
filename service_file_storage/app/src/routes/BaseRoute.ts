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
}
