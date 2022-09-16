import express from 'express';
import bodyParser from "body-parser";
import Helmet from "helmet";

import {PoolConfig, Pool} from "pg";
import {IndexRoute} from './routes/IndexRoute';
import {MapRoute} from './routes/MapRoute';
import {AlbumRoute} from './routes/AlbumRoute';
import {ImageRoute} from './routes/ImageRoute';
import {SearchRoute} from './routes/SearchRoute';
import {FaceRoute} from './routes/FaceRoute';


export class Server{
    public app: express.Application ;

    constructor(){
      this.app = express();

      //security features
      this.app.use(Helmet());
      this.app.use(Helmet.xssFilter());
      this.app.use(Helmet.hidePoweredBy());
      this.app.use(Helmet.hsts());
      this.app.use(Helmet.frameguard());
      this.app.use(Helmet.contentSecurityPolicy({
              directives: {defaultSrc: ["'self'"],
                scriptSrc: ["'self'"],
                styleSrc: ["'self'"],
                imgSrc: ["'self'"],
                connectSrc: ["'self'"],
                fontSrc: ["'self'"],
                objectSrc: ["'none'"],
                mediaSrc: ["'self'"],
                frameSrc: ["'none'"]
            }}
        ));

      this.app.listen(2344, function () {
        console.log('Service layer node ts app listening on port 2344!');
      });

      this.app.use(bodyParser.json({limit: '50mb'}))
      this.app.use(
        bodyParser.urlencoded({
          limit: '50mb',
          extended: true,
        })
      )

      this.routes();
    }

    private routes() {
      var portStr = process.env["POSTGRES_PORT"];
      if (portStr==null){
        portStr = "5432";
      }


      const pool = new Pool({
        user: process.env["POSTGRES_USER"],
        host: process.env["POSTGRES_HOST"],
        database: process.env["POSTGRES_DB"],
        password: process.env["POSTGRES_PASSWORD"],
        port: parseInt(portStr)
      })

      let router: express.Router;
      router = express.Router();

      //IndexRoute
      IndexRoute.create(router,pool);
      MapRoute.create(router,pool);
      AlbumRoute.create(router,pool);
      ImageRoute.create(router,pool);
      SearchRoute.create(router,pool);
      FaceRoute.create(router,pool);
      //use router middleware
      this.app.use(router);
    }
}
