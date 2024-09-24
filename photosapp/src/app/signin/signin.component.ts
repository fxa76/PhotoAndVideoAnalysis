import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { UntypedFormBuilder, UntypedFormGroup, FormControl,ReactiveFormsModule  } from "@angular/forms";
import {MatButtonModule} from '@angular/material/button';

import { AuthService } from './../shared/auth.service';


@Component({
  selector: 'app-signin',
  templateUrl: './signin.component.html',
  styleUrls: ['./signin.component.css']
})

export class SigninComponent implements OnInit {
  signinForm: UntypedFormGroup;

  constructor(
    public fb: UntypedFormBuilder,
    public authService: AuthService,
    public router: Router
  ) {
    this.signinForm = this.fb.group({
      email: [''],
      password: ['']
    })
  }

  ngOnInit() { }

  loginUser() {
    this.authService.signIn(this.signinForm.value)
  }
}
