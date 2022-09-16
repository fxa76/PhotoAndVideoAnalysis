import { Component, OnInit,AfterViewInit, ElementRef, ViewChild, Input } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { faUnlink,faEdit } from '@fortawesome/free-solid-svg-icons';

import {CdkDragDrop, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';

import { SearchParamService } from '../search-param.service';

import { AlbumService } from '../album.service';
import { Album } from '../album';
import { Image } from '../image';

@Component({
  selector: 'app-albums',
  templateUrl: './albums.component.html',
  styleUrls: ['./albums.component.css']
})
export class AlbumsComponent implements OnInit {
  faUnlink = faUnlink;
  faEdit = faEdit;

  albums : Album[] = [];
  curr_album : Album;
  isLoading : boolean = true;

  constructor(private albumService: AlbumService,  private searchParamService: SearchParamService) {
  }

  ngOnInit() {
        this.getAlbums();
  }

  getAlbums(): void {
    this.albumService.getAlbums(this.searchParamService.searchParam)
      .subscribe(albums=> {
        this.albums = albums;
        this.albums.forEach(function(album){
          album.images=[];
        })
      });
  }

  drop(event: CdkDragDrop<Image[]>) {
    if (event.container.id === event.previousContainer.id) {
      console.log();
    }
    else{
      console.log("moving between lists");
    }
    if (event.previousContainer === event.container) {
       moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
     } else {
       //transferArrayItem(event.previousContainer.data,
        //                 event.container.data,
          //               event.previousIndex,
            //             event.currentIndex);
            var img = event.previousContainer.data[event.previousIndex];
            event.container.data.push(img);
            this.albumService.addImageAlbumRel(this.curr_album.album_id, img.image_id)
              .subscribe(() => this);
     }
   }
   delete(image_id:number){
     this.albumService.deleteImageAlbumRel(this.curr_album.album_id,image_id)
       .subscribe(() => this);
   }
   openGroup(album:Album){
      this.isLoading = true;
      console.log("getting images for album");
      this.curr_album = album;
       this.albumService.getImagesForAlbum(album)
         .subscribe(images=> {
              album.images=images;
              this.isLoading = false;
         }
        );
   }

}
