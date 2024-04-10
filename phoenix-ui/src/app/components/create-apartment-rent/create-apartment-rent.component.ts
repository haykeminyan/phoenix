import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {PhoenixService} from "../../services/phoenix.service";
import {error} from "@angular/compiler-cli/src/transformers/util";
import {Router} from "@angular/router";

@Component({
  selector: 'app-create-apartment-rent',
  standalone: true,
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './create-apartment-rent.component.html',
  styleUrl: './create-apartment-rent.component.css'
})
export class CreateApartmentRentComponent implements OnInit{
  submitted = false
  form: FormGroup;
  file: File | undefined ;
  constructor(private service: PhoenixService,
              protected router: Router,) {

      this.form = new FormGroup({
        living_area: new FormControl(''),
        number_of_bedrooms: new FormControl(''),
        number_of_bathrooms: new FormControl(''),
        address: new FormControl(''),
        condition: new FormControl(''),
        energy_label: new FormControl(''),
        rent_price: new FormControl(''),
        file: new FormControl('')
    })
  }

  onReset(): void {
    this.submitted = false;
    this.form.reset();
  }
  onSubmit() {
    this.submitted = true
    if (this.form.invalid) {
      return;
    }
    console.log(this.file)
    this.service.createApartmentRent(this.form.value, this.file).subscribe({
        next: (result: any) => {
          alert('Congratulations! You have created dossier!')
          this.router?.navigateByUrl('/apartment-rent')
        },
        complete: () => {
        },
        error: (err: any) => {
          console.log(err)
        }
      }
  )
  }

  ngOnInit(): void {
  }
  onFileChange(event: any) {
    console.log("File change event triggered");
    const files = event.target.files;
    console.log("Selected files:", files);
    if (files && files.length > 0) {
      this.file = files[0];
      console.log("Assigned file:", this.file);
      this.form.get('file')?.setValue(this.file);
    }
  }
}
