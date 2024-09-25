import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { GenericService } from './generic.service';
import { MessageService } from './message.service';

import { Image } from './image';
import { SearchParam } from './searchParam';
import { IMAGES } from './mock-images';
import { Stock } from './stock';
import { Year } from './year';

@Injectable({
  providedIn: 'root'
})

export class ImageService extends GenericService {
  constructor(protected http: HttpClient, protected messageService: MessageService) {
    super(http, messageService);
  }

  getImages(searchParam): Observable<Image[]> {
    this.log('fetching images');
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    console.log(searchParam);
    //return this.http.post<Image[]>('https://localhost/python/process_search_form',searchParam, httpOptions)
    return this.http.post<Image[]>('./capi2/v2/images', searchParam, httpOptions)    
    //return of(IMAGES);
  }

  getTodaysImages(searchParam): Observable<Image[]> {
    this.log('fetching images');
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    console.log(searchParam);
    return this.http.post<Image[]>('./capi2/v2/gettodaysimages', searchParam, httpOptions)
    //return of(IMAGES);
  }

  //new Date(2100,11,12,0,0,0,0)
  getMonthDayImages(searchParam): Observable<Image[]> {
    this.log('fetching images');
    searchParam.targetDate=new Date(searchParam.targetDate); //new Date("2024-08-27");
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    console.log(searchParam);
    return this.http.post<Image[]>('./capi2/v2/getmonthdayimages', searchParam, httpOptions)
    //return of(IMAGES);
  }

  getImagesYears(): Observable<Year[]>{
    this.log('fetching images timeline');
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    //return this.http.post<Image[]>('https://localhost/python/process_search_form',searchParam, httpOptions)
    return this.http.post<Year[]>('./capi2/v2/imagesyears',httpOptions)
    //return of(IMAGES);
  }

  getImagesTimeline(): Observable<Stock[]>{
    this.log('fetching images timeline');
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    //return this.http.post<Image[]>('https://localhost/python/process_search_form',searchParam, httpOptions)
    return this.http.post<Stock[]>('./capi2/v2/imagestimeline',httpOptions)
    //return of(IMAGES);
  }

  getImagesTimebar(): Observable<Stock[]>{
    this.log('fetching images timeline');
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    //return this.http.post<Image[]>('https://localhost/python/process_search_form',searchParam, httpOptions)
    return this.http.post<Stock[]>('./capi2/v2/imagestimebar',httpOptions)
  }

  getImagesWithFaces(searchParam): Observable<Image[]> {
    this.log('fetching images');
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    console.log(searchParam);
    //return this.http.post<Image[]>('https://localhost/python/process_search_form',searchParam, httpOptions)
    return this.http.post<Image[]>('./capi2/v2/getImagesWithFaces', searchParam, httpOptions)
  }

  getImage(id: number): Observable<Image> {
    this.log(`fetching image data id=${id}`);
    //return this.http.get<Image>('https://localhost/python/get_image/'+id);
    return this.http.get<Image>('./capi2/v2/image/' + id)
  }

  /*File image is taken via the python open cv as it as a very good management of orientation.*/
  getImageFile(id: number): Observable<Image> {
    this.log(`fetching image file id=${id}`);
    return this.http.get<Image>('./python/get_image/' + id);
  }

  getImageOverlay(id: number): Observable<Image> {
    this.log(`ImageService: fetched image id=${id}`);
    return this.http.get<Image>('./python/get_image_with_overlay/' + id);
    //return this.http.get<Image>('./python/get_image/' + id);
  }

  updateImage(image: Image): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.put('./python/update_image', image, httpOptions).pipe(
      tap(_ => this.log(`updated image id=${image.image_id}`)),
      catchError(this.handleError<any>('updateImage'))
    );
  }

}
