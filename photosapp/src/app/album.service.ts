import { Injectable } from '@angular/core';

import { HttpClient, HttpHeaders }    from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { GenericService } from './generic.service';
import { MessageService } from './message.service';
import { ImageService } from './image.service';

import { Album } from './album';
import { Image } from './image';

@Injectable({
  providedIn: 'root'
})

export class AlbumService extends GenericService{

  constructor(protected http: HttpClient,protected messageService: MessageService,private imageService :ImageService) {
    super(http,messageService)
  }

  addAlbum(album:Album){
    this.log('fetching albums');
    const httpOptions = {
      headers: new HttpHeaders({
      'Content-Type':  'application/json'
    })};
    console.log(album);
    return this.http.put<Album>('./capi2/v2/albumadd',album, httpOptions).subscribe(res => {
      console.log(res);
    }, error => {
      console.log('error')
    });;

  }

  getAlbumById(id:number):Observable<Album>{
      this.log(`fetching album id=${id}`);
      return this.http.get<Album>('./capi2/v2/album/' + id)
  }

  updateAlbum(album){
      const httpOptions = {
        headers: new HttpHeaders({
          'Content-Type': 'application/json'
        })
      };
      console.log("updating album" + album)
      return this.http.put<Album>('./capi2/v2/albumupdate', album, httpOptions).pipe(
            tap(_ => this.log(`updated album id=${album.album_id}`))
            //catchError(this.handleError<any>('updateImage'))
      ).subscribe(res => {
      }, error => {
        console.log('error')
      });;
  }

  getAlbums(searchParam): Observable<Album[]> {
    this.log('fetching albums');
    const httpOptions = {
      headers: new HttpHeaders({
      'Content-Type':  'application/json'
    })};
    console.log(searchParam);
    return this.http.post<Album[]>('./capi2/v2/albums',searchParam, httpOptions)
       //return of(IMAGES);
  }

  getImagesForAlbum(album:Album): Observable<Image[]> {
    this.log('get images for album');
    const httpOptions = {
      headers: new HttpHeaders({
      'Content-Type':  'application/json'
    })};
    var rel = {
      album_id: album.album_id
    }
    return this.http.post<Image[]>('./capi2/v2/imagesforalbum',rel, httpOptions)
       //return of(IMAGES);
  }

  addImageAlbumRel( album_id:number,image_id:number): Observable<Image[]> {
    this.log('adding image to album');
    const httpOptions = {
      headers: new HttpHeaders({
      'Content-Type':  'application/json'
    })};
    var rel = {
      album_id: album_id,
      image_id:image_id
    }
    return this.http.put('./capi2/v2/addImageAlbumRel',rel, httpOptions).pipe(
      tap( _ => this.log(`updated album id=${album_id}`)),
      catchError(this.handleError<any>('updateImage'))
    );
  }
  deleteImageAlbumRel( album_id:number,image_id:number): Observable<Image[]> {
      this.log('remove image from album');
      const httpOptions = {
        headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })};
      var rel = {
        album_id: album_id,
        image_id:image_id
      }
      return this.http.put('./capi2/v2/deleteImageAlbumRel',rel, httpOptions).pipe(
        tap( _ => this.log(`removing image from album id=${album_id}`)),
        catchError(this.handleError<any>('updateImage'))
      );
  }
}
