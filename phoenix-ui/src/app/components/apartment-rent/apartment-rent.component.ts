import {Component, OnInit, ViewChild} from '@angular/core';
import {PhoenixService} from "../../services/phoenix.service";
import {Router, RouterLink} from "@angular/router";
import {NgForOf, NgIf} from "@angular/common";
import {animate, keyframes, style, transition, trigger} from "@angular/animations";
import {CarouselComponent, CarouselModule} from 'ngx-bootstrap/carousel';

@Component({
  selector: 'app-apartment-rent',
  standalone: true,
    imports: [
        RouterLink,
        NgIf,
        CarouselModule,
        NgForOf,

    ],
  templateUrl: './apartment-rent.component.html',
  styleUrl: './apartment-rent.component.css',
  animations: [
    trigger('cardAnimation', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(-50px)' }),
        animate('1s', style({ opacity: 1, transform: 'translateY(0)' }))
      ])
    ])
  ]
})
export class ApartmentRentComponent implements OnInit{
  @ViewChild('carousel') carousel!: CarouselComponent;
  idApartment!: string
  dossier: any | undefined
  ngOnInit(): void {
  }
  constructor(private service: PhoenixService,
              private router: Router,) {
    this.idApartment = router.url.split('rent/')[1]
    this.getApartment()
  }
  getApartment(){
    this.service.viewApartment(this.idApartment).subscribe({
      next: (result: any) => {
        this.dossier = (result.body as unknown as any)
        console.log(this.dossier.image)
    },
      complete: () => {
    },
      error: (err: any) => {
      console.log(err)
    }
  })
  }

  delete(id: string){
    this.service.deleteApartment(id).subscribe()
    alert('You have successfully deleted dossier');
    this.router.navigateByUrl('/all-apartment-rent')
  }

    protected readonly JSON = JSON;
}
