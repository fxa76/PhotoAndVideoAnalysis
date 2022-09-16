import express from 'express';
import bodyParser from "body-parser";
import Helmet from "helmet";
import {PoolConfig, Pool} from "pg";
import {IndexRoute} from './routes/IndexRoute';
import {FileRoute} from './routes/FileRoute';

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
              directives: {
                defaultSrc: ["'self'"],
                scriptSrc: ["'self'"],
                styleSrc: ["'self'","'unsafe-inline'"],
                imgSrc: ["'self'"],
                connectSrc: ["'self'"],
                fontSrc: ["'self'"],
                objectSrc: ["'none'"],
                mediaSrc: ["'self'"],
                frameSrc: ["'none'"]
            }}
        ));

        this.app.listen(2345,'0.0.0.0', function () {
            console.log('Example app listening on port 2345!');
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
      FileRoute.create(router,pool);
      //use router middleware
      this.app.use(router);
    }
}
