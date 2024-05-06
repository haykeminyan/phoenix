import {Component, OnInit} from '@angular/core';
import {PhoenixService} from "../../services/phoenix.service";
import {Router, RouterLink} from "@angular/router";
import {NgIf} from "@angular/common";
import {animate, keyframes, style, transition, trigger} from "@angular/animations";

@Component({
  selector: 'app-apartment-rent',
  standalone: true,
  imports: [
    RouterLink,
    NgIf
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
    },
      complete: () => {
    },
      error: (err: any) => {
      console.log(err)
    }
  })
  }

}
