import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BrowserModule } from '@angular/platform-browser';

import { faImages, faBook, faSmile, faGlobe, faSearch, faVectorSquare } from '@fortawesome/free-solid-svg-icons';
import { faSquare, faCheckSquare, faUpload,faUser, faSignOutAlt,faSignInAlt, faUserPlus, faChartBar, faCalendar } from '@fortawesome/free-solid-svg-icons';

import { AuthService } from './shared/auth.service';
import { User } from './shared/user';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'FXA Photos App';
  faImages = faImages;
  faBook = faBook;
  faSmile = faSmile;
  faGlobe = faGlobe;
  faSearch = faSearch;
  faVectorSquare = faVectorSquare;
  faSquare = faSquare;
  faCheckSquare = faCheckSquare;
  faUpload = faUpload;
  faUser = faUser;
  faSignOutAlt = faSignOutAlt;
  faSignInAlt = faSignInAlt;
  faUserPlus =  faUserPlus;
  faChartBar = faChartBar;
  faCalendar = faCalendar;

  currentUser: User;
  isLoading : boolean = true;

  constructor(public authService: AuthService) {
    this.isLoggedIn();

  }

  isLoggedIn ():boolean{
    if(this.authService!=null && this.authService.isLoggedIn  ){
        this.currentUser = this.authService.currentUser;
        this.isLoading = false;
        return true;
      }
    else{
        this.isLoading = false;
      return false;
    }
  }

  logout() {
   this.authService.doLogout()
 }
}
