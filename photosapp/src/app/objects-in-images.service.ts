import { Injectable } from '@angular/core';

import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';


import { MessageService } from './message.service';

import { Object_in_image } from './object_in_image';
import { Description } from './description';

@Injectable({
  providedIn: 'root'
})

export class ObjectsInImagesService {

  constructor(private http: HttpClient, private messageService: MessageService) { }

  getObjects(image_id): Observable<Object_in_image[]> {

    this.messageService.add('ObjectInImageService: fetching objects for image id : ' + image_id);
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.get<Object_in_image[]>('https://localhost/capi2/v2/list_objects_for_image_id/'+image_id);
  }

  getFaces(searchParam): Observable<Object_in_image[]> {

    this.messageService.add('ObjectInImageService: fetching faces from offset ' + searchParam.offset + ' to next' + searchParam.next);
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    return this.http.post<Object_in_image[]>('https://localhost/capi2/v2/list_faces', searchParam, httpOptions);
  }

  getFacesForIterationFaceId(searchParam): Observable<Object_in_image[]> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
  };
    this.messageService.add(`ObjectInImageService: fetching faces for iteration and face_id`);
    //todo add search params
    return this.http.post<Object_in_image[]>('https://localhost/capi2/v2/list_distinct_face_iteration', searchParam, httpOptions);

  }

  getDistinctFaces(searchParam): Observable<Object_in_image[]> {
    this.messageService.add(`ObjectInImageService: fetching distinct faces`);
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };

    return this.http.post<Object_in_image[]>('https://localhost/capi2/v2/list_distinct_faces', searchParam, httpOptions);
  }

  get_similar_face(id) : Observable<Object_in_image[]> {
    this.messageService.add(`ObjectInImageService: fetching similar faces`);
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };

    return this.http.get<Object_in_image[]>('https://localhost/python/get_similiar_faces_to/'+id)
  }

  /** GET: update the hero on the server */
  hiddeFace(iteration, id): Observable<any> {
    return this.http.get('https://localhost/capi2/v2/hideFaceIdForIterationId/' + iteration + '/' + id).pipe(
      tap(_ => this.log(`hidding face`)),
      catchError(this.handleError<any>('updateImage'))
    );
  }

  /* Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }
  /** Log a HeroService message with the MessageService */
  private log(message: string) {
    this.messageService.add(`Objects service : ${message}`);
  }
}
