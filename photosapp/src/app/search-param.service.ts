import { Injectable } from '@angular/core';
import { SearchParam } from './searchParam';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

import { GenericService } from './generic.service';
import { MessageService } from './message.service';

import { Object_in_image } from './object_in_image';
import { Description } from './description';
import { Camera } from './camera';
import { FileFormat } from './fileformat';

@Injectable({
  providedIn: 'root'
})
export class SearchParamService extends GenericService {
  searchParam: SearchParam;
  possibleDescriptions: Description[];
  possibleCameras: Camera[];
  possibleFileformats: FileFormat[];

  constructor(protected http: HttpClient, protected messageService: MessageService) {
    super(http, messageService);
    this.searchParam = new SearchParam();
    this.searchParam.use_coords = true;
    this.searchParam.bottomLeft = [-180, -67];
    this.searchParam.topRight = [180, 84];
    this.searchParam.fromdate = 1451602860;
    this.searchParam.todate = 2097960740;
    this.searchParam.dateIsNull = false;
    this.searchParam.gpsIsNull = false;

    this.searchParam.descriptions = [];
    this.searchParam.cameramodels = [];
    this.searchParam.fileformats = [];

    this.searchParam.offset = 0;
    this.searchParam.next = 100;
    this.getObjectsDescriptions(this.searchParam)
      .subscribe(descriptions => {
        this.possibleDescriptions = descriptions
        console.log("Objects descriptions ready!!");
      }
      );
    this.getCameraModelsDescriptions(this.searchParam)
      .subscribe(descriptions => {
        this.possibleCameras = descriptions
        console.log("Camera descriptions ready!!");
      }
      );
    this.getFileFormatsDescriptions(this.searchParam)
      .subscribe(descriptions => {
        this.possibleFileformats = descriptions
        console.log("FielFormats descriptions ready!!");
      }
      );
  }

  getObjectsDescriptions(searchParam): Observable<Description[]> {
    if (this.searchParam.descriptions.length > 0) {
      console.log("some description criteria already selected");
    }
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
};
    this.log(`fetching objects descriptions`);
    return this.http.post<Description[]>('https://localhost/capi2/v2/searchObjects', searchParam, httpOptions);
    //return this.http.post<Description[]>('https://localhost/python/descriptions',searchParam,httpOptions);
  }

  getCameraModelsDescriptions(searchParam): Observable<Camera[]> {
    if (this.searchParam.descriptions.length > 0) {
      console.log("some description criteria already selected");
    }
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    this.log(`fetching camera models descriptions`);
    //return this.http.get<Camera[]>('https://localhost/python/list_camera_models');//,searchParam,httpOptions);
    return this.http.post<Camera[]>('https://localhost/capi2/v2/searchModels', searchParam, httpOptions);

  }
  getFileFormatsDescriptions(searchParam): Observable<FileFormat[]> {
    if (this.searchParam.descriptions.length > 0) {
      console.log("some description criteria already selected");
    }
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    this.log(`fetching file formats descriptions`);
    //return this.http.get<Camera[]>('https://localhost/python/list_camera_models');//,searchParam,httpOptions);
    return this.http.post<FileFormat[]>('https://localhost/capi2/v2/searchFileFormats', searchParam, httpOptions);

  }

  getPossibleDescriptions(): Description[] {
    return this.possibleDescriptions;
  }

}
