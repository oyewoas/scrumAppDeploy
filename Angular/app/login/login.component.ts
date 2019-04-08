import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from '../data.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  constructor(private router: Router, public dataservice: DataService) { }

  signUp() {
    this.router.navigate(['signup']);
  }
  logIn() {
    this.router.navigate(['login']);
  }

  toLogin(){
    this.dataservice.toLogin();

  }

  logout() {
    this.dataservice.logout();
  }
  ngOnInit() {
  }


}
