import { NextFunction, Request, Response, Router } from "express";
import { BaseRoute } from "./BaseRoute";
import { PoolConfig, Pool } from "pg";

/**
 * / route
 *
 * @class User
 */
export class FileRoute extends BaseRoute {



  /**
   * Create the routes.
   *
   * @class IndexRoute
   * @method create
   * @static
   */
  public static create(router: Router, pg: Pool) {
    //log
    console.log("[UploadRoute::create] Creating Upload route.");
    //add home page route
    var fileRoutes: FileRoute = new FileRoute(pg);
    router.post("/v1/upload", (req: Request, res: Response, next: NextFunction) => {
      fileRoutes.upload(req, res, next);
    });
    router.get("/v1/get_file/:id", (req: Request, res: Response, next: NextFunction) => {
      fileRoutes.getFile(req, res, next);
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
  public getFile(req: Request, res: Response, next: NextFunction) {
    //DEBUT
    let fileId = req.params.id;
    var sql = "SELECT filefullname,fileextensions FROM public.images where image_id = $1";
    let values: (string | number)[]  = [fileId]

    this.pg.query(sql, values ,(err, result) => {
      if (err) {
        throw err
      }
      if (result.rows.length == 0) {
        res.send('no file with id : ' + fileId);
      }
      else {
        var fileSystem = require('fs');
        let image = result.rows[0];
        console.log(image)
        let filePath = image.filefullname
        console.log("src :" + filePath);
        var stat = fileSystem.statSync(filePath);
        console.log(stat);

        var contenttype = 'Document';
        switch (image.fileextensions) {
          case '.jpeg':
          case '.jpg':
            contenttype = 'image/jpeg';
            break;
          case '.tiff':
          case '.tif':
            contenttype = 'image/tiff';
            break;
          case '.png':
            contenttype = 'image/png';
            break;
          case '.mov':
          case '.MOV':
            contenttype = 'video/quicktime';
            break;
          case '.mp4':
            contenttype = 'video/mpeg';
            break;
          case '.orf':
            contenttype = ' image/x-olympus-orf';
            break;
          default:
            break;
        }

        res.writeHead(200, {
          'Content-Type': contenttype, // 'application/x-troff-msvideo',
          'Content-Length': stat.size
          //,'Content-Disposition': 'attachment; filename="file'+image.fileextensions+'"'
        });

        var readStream = fileSystem.createReadStream(filePath);
        // We replaced all the event handlers with a simple call to readStream.pipe()
        readStream.pipe(res);
      }
    });
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
  public upload(req: Request, res: Response, next: NextFunction) {
    //DEBUT
    var formidable = require('formidable');

    var form = new formidable.IncomingForm();
    form.encoding = 'utf-8';
    form.keepExtensions = true;

    form.on('file', function(name: string, file: File) {
      var DIR: string = '/pictures_inbox/uploads/';
      //console.log("file received !!!!" + file.name);
      var fs = require('fs');
      fs.readFile((file as any).path, 'utf8', function(err: any, data: string) {
        console.log(data);
        const base64data = data.replace(/^data:.*,/, '');
        var fs2 = require('fs');
        fs2.writeFile(DIR + file.name, base64data, 'base64', (err2: any) => {
          if (err2) {
            console.log(err2);
            console.log("No file received");
            return res.send({
              success: false
            });
          }
          else {
            console.log('file received : ' + DIR);
            return res.send({
              success: true
            })
          }
        });
      });

    });

    form.on('field', function(name: string, value: string) {

      console.log("field received !!!!" + name);


    });

    form.parse(req, function(err: any, fields: any, files: any) {
    });

    //FIN
  }

}
