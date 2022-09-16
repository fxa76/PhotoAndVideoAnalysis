import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject, Observable } from 'rxjs';
import { finalize } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Duplicate } from './duplicate';
import { Image } from './image';

@Injectable({
  providedIn: 'root'
})
export class DuplicatesService {

  constructor(private http: HttpClient) { }


  public getDuplicates(): Observable<Duplicate[]> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    //return this.http.post<Image[]>('https://localhost/python/process_search_form',searchParam, httpOptions)
    return this.http.get<Duplicate[]>('https://localhost/capi2/v2/duplicates', httpOptions)
    //return of(IMAGES);
  }


}
