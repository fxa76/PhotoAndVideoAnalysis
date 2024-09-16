import { CommonModule, DatePipe } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { HttpClientModule, HTTP_INTERCEPTORS  } from '@angular/common/http';
import { AuthInterceptor } from './shared/authconfig.interceptor';

//my components
import { AppComponent } from './app.component';
import { ImagesComponent } from './images/images.component';
import { ImageDetailComponent } from './image-detail/image-detail.component';
import { MessagesComponent } from './messages/messages.component';
import { AppRoutingModule } from './app-routing.module';
import { ImageOverlayComponent } from './image-overlay/image-overlay.component';
import { MapComponent } from './map/map.component';
import { SearchParamComponent } from './search-param/search-param.component';
import { FacesComponent } from './faces/faces.component';
import { AlbumDetailComponent } from './album-detail/album-detail.component';
import { AlbumsComponent } from './albums/albums.component';
import { UploadComponent } from './upload/upload.component';
import { DuplicatesComponent } from './duplicates/duplicates.component';

//my directives
import { DragDropDirective } from './drag-drop.directive';

//my services
import { MapService } from './map.service';
import { MessageService } from './message.service';
import { ObjectsInImagesService } from './objects-in-images.service';
import { ImageService } from './image.service';
import { SearchParamService } from './search-param.service';
import { AlbumService } from './album.service';
import { DuplicatesService } from './duplicates.service';
import { SignupComponent } from './signup/signup.component';
import { SigninComponent } from './signin/signin.component';
import { UserProfileComponent } from './user-profile/user-profile.component';

//forms
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
//external modules
import { DragDropModule } from '@angular/cdk/drag-drop';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core';
import { MatInputModule } from '@angular/material';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import {MatIconModule} from '@angular/material/icon';
import {MatTableModule} from '@angular/material/table';
import {MatSlideToggleModule} from '@angular/material/slide-toggle';

//D3 Sample
import { OrderStatusComponent } from './order-status/order-status.component';
import { DonutChartComponent } from './donut-chart/donut-chart.component';
import { TimelineComponent } from './timeline/timeline.component';
import { TimelinebarComponent } from './timelinebar/timelinebar.component';
import { OrderDeliveryComponent } from './order-delivery/order-delivery.component';
import { AreaChartComponent } from './area-chart/area-chart.component';
import { BrushZoomComponent } from './brush-zoom/brush-zoom.component';
import { BrushZoomHistoComponent } from './brush-zoom-histo/brush-zoom-histo.component';
import { D3ImageViewerComponent } from './d3-image-viewer/d3-image-viewer.component';
import { D3ImageAndObjectsViewerComponent } from './d3-image-and-objects-viewer/d3-image-and-objects-viewer.component';

@NgModule({
  declarations: [
    DragDropDirective,
    AppComponent,
    ImagesComponent,
    ImageDetailComponent,
    MessagesComponent,
    ImageOverlayComponent,
    MapComponent,
    SearchParamComponent,
    FacesComponent,
    AlbumDetailComponent,
    AlbumsComponent,
    UploadComponent,
    DuplicatesComponent,
    SignupComponent,
    SigninComponent,
    UserProfileComponent,
    
    OrderStatusComponent,
    DonutChartComponent,
    OrderDeliveryComponent,
    AreaChartComponent,
    BrushZoomComponent,
    BrushZoomHistoComponent,
    TimelineComponent,
    TimelinebarComponent,
    D3ImageViewerComponent,
    D3ImageAndObjectsViewerComponent
  ],
  imports: [
    CommonModule,
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserModule,
    DragDropModule,
    BrowserAnimationsModule,
    //material
    MatIconModule,
    MatExpansionModule,
    MatProgressSpinnerModule,
    MatCardModule,
    MatProgressBarModule,
    MatButtonModule,
    MatTooltipModule,
    MatFormFieldModule,
    MatCheckboxModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatInputModule,
    MatToolbarModule,
    MatSidenavModule,
    MatTableModule,
    MatSlideToggleModule,
    MatListModule,
    //forms
    FormsModule,
    ReactiveFormsModule,
    //font
    FontAwesomeModule
  ],
  providers: [SearchParamService,
    MessageService,
    ObjectsInImagesService,
    ImageService,
    MapService,
    AlbumService,
    DuplicatesService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
    DatePipe
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
