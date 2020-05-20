import { Component,OnInit } from '@angular/core';
import { HttpService } from './http.service'
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-second',
  templateUrl: './second.component.html',
  styleUrls: ['./second.component.css']
})
export class SecondComponent implements OnInit {

	clickcounter: number = 0;
	title: string;
	food:Object;
	list_of_problems = [];
	constructor(private http: HttpService) {}
	ngOnInit(){
		this.title = 'Game is On!!';
		this.http.getdata().subscribe(data =>
		{
		console.log(data['list'])
		this.list_of_problems = data['list'];
		},
		 error => {
        console.log('Log the error here: ', error);
    });
		

	}
	onClickMe()
	{
	this.clickcounter += 1;
	
	}
}
