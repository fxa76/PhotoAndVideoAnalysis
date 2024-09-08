import { Injectable } from '@angular/core';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { MessageService } from './message.service';

import { SearchParam } from './searchParam';
import { Poi } from './poi';

@Injectable({
  providedIn: 'root'
})

export class MapService {

  constructor(private http: HttpClient, private messageService: MessageService) { }

  getPoi(searchParam: SearchParam): Observable<Poi[]> {
    this.messageService.add('MapService : fetching Point of Interests');
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    };
    console.log(searchParam);
    searchParam.use_coords = true;
    console.log(searchParam);
    return this.http.post<Poi[]>('./capi2/v2/map', searchParam, httpOptions)
    //return of(IMAGES);
  }

}
