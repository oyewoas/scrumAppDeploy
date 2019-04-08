import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataService } from './../data.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { DragulaService } from 'ng2-dragula';
import {Subscription} from 'rxjs';



@Component({
  selector: 'app-scrumboard',
  templateUrl: './scrumboard.component.html',
  styleUrls: ['./scrumboard.component.css']
})
export class ScrumboardComponent implements OnInit {
  public arrCount = [ 1, 2, 3, 4];

  subs = new Subscription();
  
  constructor(private router: Router, private dataservice: DataService, private dragula: DragulaService, private http: HttpClient) {
    this.dataservice.username = sessionStorage.getItem('username');
    this.dataservice.roles = sessionStorage.getItem('role');
    this.dataservice.message = sessionStorage.getItem('message');

    this.dataservice.authOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json', 'Authorization': 'JWT ' + sessionStorage.getItem('token')})
  };


    this.http.get('http://' + this.dataservice.domainname + '/ayooluwaoyewoscrumy/api/v1/scrumuser/', 
    this.dataservice.httpOptions).subscribe(
        data => {
            console.log(data);
            // tslint:disable-next-line:no-string-literal
            for (let i = 0; i < data['length']; i++) {
              data[i]['scrumygoals_set'] = data[i]['scrumygoals_set'].filter(item => item['visible']);
            }

            this.dataservice.users = data;
        },
        err => {
           this.dataservice.message = 'Unexpected Error';
           console.log(err);
        }
    );


    this.dragula.createGroup('mainTable', {
      revertOnSpill: true,
      direction: 'horizontal',
      invalid : (el) => {
        return el.id === 'user' || el.id === 'remove' || el.id === 'blank';
      }
    });

    this.subs.add(
      this.dragula.drop('mainTable').subscribe(
        value => {
          console.log(value);
          const el = value['el'];
          const target = value['target'];
          const source = value.source;

          if (target.id === source.id) {
            let offset = 0;

            for (let i = 0; i < target.children.length; i++) {
              if ( i === 0 && target.children[i].id === 'user') {
                offset = 1;
                continue;
              }
              if (target.children[i].id === el.id) {
                console.log(i - offset);
                this.dataservice.moveGoal(source.id, i - offset);
                break;
              }
            }
          } else {
              this.dataservice.changeOwner(source.id, target.id);
          }
        }
      )
    );
  }

  editGoal(event) {
    console.log(event);
    const items = event.target.innerText.split(/\)\s(.+)/);
    const goal_name = window.prompt('Editing task ID No ' + items[0] + ':', items[1]);
    // tslint:disable-next-line:curly
    if (goal_name == null || goal_name === '') {
      this.dataservice.message = 'Editing Canceled';
    } else {
      this.http.put('http://' + this.dataservice.domainname + '/ayooluwaoyewoscrumy/api/v1/scrumgoal/',
        JSON.stringify({mode: 1, goal_id: items[0], new_name: goal_name }), this.dataservice.authOptions).subscribe(
            data => {
                this.dataservice.users = data['data'];
                this.dataservice.message = data['message'] ;

            },

            err => {

              console.error(err);
              if (err.status === 401) {
                this.dataservice.message = 'Session Invalid or Expired, Please Login';
                this.dataservice.logout();
              } else {
                this.dataservice.message = 'Unexpected Error!';
              }


            },
          );
    }

  }

  doNoitemething() {

  }

  ngOnInit() {
  }
  addGoal() {


    this.dataservice.addGoal();
  }



  logout() {
   this.dataservice.logout();
   this.dataservice.message = 'Thank you for using Scrum!';
}

 ngOnDestroy() {
  this.subs.unsubscribe();
  this.dragula.destroy('mainTable');
}

}


