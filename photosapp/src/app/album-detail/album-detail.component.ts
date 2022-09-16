import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { AlbumService } from '../album.service';
import { Album } from '../album';


@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.css']
})
export class AlbumDetailComponent implements OnInit {

  @Input() album : Album;
  accessPath : any;
  isLoading : boolean = true;
  isCreation : boolean = false;
  constructor(private albumService: AlbumService,private route: ActivatedRoute) {


  }

  ngOnInit() {
    this.getAlbum();
  }

  getAlbum():void{
    this.isLoading = true;
    this.accessPath =  this.route.snapshot.routeConfig.path;
    console.log(this.accessPath)

    switch(this.accessPath){
      case 'album_create':
        this.album = new Album();
        this.isLoading = false;
        this.isCreation = true;
        break;
      case 'album_detail/:id':
        const id = +this.route.snapshot.paramMap.get('id');
        this.albumService.getAlbumById(id)
            .subscribe(album => {
              this.album = album;
              this.isLoading = false;
            });
        break;

    }
  }

  save(){
    if (this.isCreation){
      this.albumService.addAlbum(this.album);
    }
    else{
      this.albumService.updateAlbum(this.album);
    }
  }

}
