import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { AlbumsComponent } from './albums/albums.component';
import { AlbumDetailComponent} from './album-detail/album-detail.component';
import { ImagesComponent } from './images/images.component';
import { ImageDetailComponent } from './image-detail/image-detail.component';
import { ImageOverlayComponent } from './image-overlay/image-overlay.component';
import { FacesComponent } from './faces/faces.component';
import { MapComponent } from './map/map.component';
import { SearchParamComponent } from './search-param/search-param.component';
import { UploadComponent } from './upload/upload.component';
import { DuplicatesComponent } from './duplicates/duplicates.component';

import { AuthGuard } from "./shared/auth.guard";
import {SignupComponent} from "./signup/signup.component"
import {SigninComponent} from "./signin/signin.component"
import {UserProfileComponent} from "./user-profile/user-profile.component"

import { OrderStatusComponent } from './order-status/order-status.component';
import { OrderDeliveryComponent } from './order-delivery/order-delivery.component';
import { TimelineComponent } from './timeline/timeline.component';
import { TimelinebarComponent } from './timelinebar/timelinebar.component';

const routes: Routes = [

  //working
  { path: 'signup', component: SignupComponent },
  { path: 'log-in', component: SigninComponent },
  //protected access
  { path: 'user-profile/:id', component: UserProfileComponent, canActivate: [AuthGuard] },
  { path: 'albums', component: AlbumsComponent, canActivate: [AuthGuard] },
  { path: 'album_create', component: AlbumDetailComponent, canActivate: [AuthGuard] },
  { path: 'album_detail/:id', component: AlbumDetailComponent, canActivate: [AuthGuard] },
  { path: 'images/:today', component: ImagesComponent, canActivate: [AuthGuard] },
  { path: 'detail/:id', component: ImageDetailComponent, canActivate: [AuthGuard] },
  { path: 'overlay/:id', component: ImageOverlayComponent, canActivate: [AuthGuard] },
  { path: 'facesdistinct', component: FacesComponent, canActivate: [AuthGuard] },
  { path: 'faces', component: FacesComponent, canActivate: [AuthGuard] },
  { path: 'faces/:id', component: FacesComponent, canActivate: [AuthGuard] },
  { path: 'face/:iteration/:id/:offset/:next', component: FacesComponent, canActivate: [AuthGuard] },
  { path: 'map', component: MapComponent, canActivate: [AuthGuard] },
  { path: 'searchParam', component: SearchParamComponent, canActivate: [AuthGuard] },
  { path: 'upload', component: UploadComponent, canActivate: [AuthGuard] },
  { path: 'duplicates', component: DuplicatesComponent, canActivate: [AuthGuard] },
  { path: 'status', component: OrderStatusComponent, canActivate: [AuthGuard]  },
  { path: 'delivery', component: OrderDeliveryComponent, canActivate: [AuthGuard]  },
  { path: 'timeline', component: TimelineComponent, canActivate: [AuthGuard]  },
  { path: 'timelinebar', component: TimelinebarComponent, canActivate: [AuthGuard]  }

];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
