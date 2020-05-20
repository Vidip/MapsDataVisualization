import { Component,AfterViewInit,OnInit,ViewChild,ElementRef } from '@angular/core';
import { Router,ActivatedRoute } from '@angular/router';
import * as  d3 from 'd3';
import {select, Selection} from 'd3-selection';
import { Chart } from 'chart.js'

@Component({
  selector: 'app-third',
  templateUrl: './third.component.html',
  styleUrls: ['./third.component.css']
})
export class ThirdComponent {
    @ViewChild('canvas') canvas: any;
  title = 'my-app33';
  chart = [];
  newval:string;
  sub;
  id:string;
  survey:string;
  ss: boolean;

    public barChartOptions = {
    scaleShowVerticalLines: false,
    responsive: true
  };
  public barChartLabels = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
  public barChartType = 'bar';
  public barChartLegend = true;
  public barChartData = [
    {data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A'},
    {data: [28, 48, 40, 19, 86, 27, 90], label: 'Series B'}
  ];

  constructor(private _Activatedroute:ActivatedRoute, private elementRef: ElementRef){
  	
  }

  ngOnInit()
  {

  this.survey = 'Halifax Transit Tracker';
   this.sub=this._Activatedroute.paramMap.subscribe(params => { 
         console.log(params);
          this.id = params.get('id'); 
          console.log(this.id);  
      });

      
      
  }

  ngAfterViewInit() {
    
     let ctx = this.canvas.nativeElement.querySelector('#canvas');
     console.log(this.canvas);
     let temp_max:number = [12,3,4];
      let temp_min:number = [11,22,22];
      const d: Date = new Date("2015-3-15");
      let weatherDates = [new Date("2019-3-15"),new Date("2019-3-18"),new Date("2019-3-19")];
      console.log(d);

       this.chart = new Chart(this.canvas.nativeElement, {
          type: 'line',
          data: {
            labels: ['Sep-Dec','Jan-Mar','Mar-May'],
            datasets: [
              { 
                data: temp_max,
                borderColor: "#3cba9f",
                fill: false
              },
              { 
                data: temp_min,
                borderColor: "#ffcc00",
                fill: false
              },
            ]
          },
          options: {
            legend: {
              display: false
            },
            scales: {
              xAxes: [{
                display: true
              }],
              yAxes: [{
                display: true
              }],
            }
          }
        });
}



}
