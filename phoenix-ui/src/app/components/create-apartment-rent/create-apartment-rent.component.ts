import {Component, OnInit} from '@angular/core';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  ReactiveFormsModule,
  ValidationErrors,
  Validators
} from "@angular/forms";
import {PhoenixService} from "../../services/phoenix.service";
import {Router} from "@angular/router";
import {CommonModule, NgIf} from "@angular/common";

@Component({
  selector: 'app-create-apartment-rent',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgIf,
    CommonModule
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
        living_area: new FormControl('', [Validators.required, this.numericValidator]),
        number_of_bedrooms: new FormControl(null, this.numericValidator),
        number_of_bathrooms: new FormControl(null, this.numericValidator),
        building_year: new FormControl(null, this.buildingYearValidator),
        address: new FormControl('', Validators.required),
        condition: new FormControl('good'),
        energy_label: new FormControl('a_plus_plus'),
        rent_price: new FormControl('', [Validators.required, this.numericValidator]),
        file: new FormControl('')
    })
  }

  numericValidator(control: AbstractControl): ValidationErrors | null {
    const value = control.value

    // Regular expression for validating numeric input
    const numericPattern = /^-?\d+$/;

    // Check if the value matches the numeric pattern
    if (!numericPattern.test(value) || Number(value) < 0) {
      return { numeric: true };
    }
    return null

  }

  buildingYearValidator(control: AbstractControl): ValidationErrors | null {
    const value = control.value

    // Regular expression for validating numeric input
    const numericPattern = /^-?\d+$/;
    // Check if the value matches the numeric pattern
    if (!numericPattern.test(value) || Number(value) < 1700) {
      return { year: true };
    }
    return null

  }


  onReset(): void {
    this.submitted = false;
    this.form.reset();

    // Get a reference to the specific field you want to preserve
    const confitionLabelControl = this.form.get('condition');
    // Set the preserved value back to the control
    if (confitionLabelControl) {
      confitionLabelControl.setValue('good');
    }
  }

  //TODO need to understand may be add null value for energy label?

  onSubmit() {
    this.submitted = true
    if (this.form.invalid) {
      return;
    }

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
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      this.form.patchValue({
        file: file
      });
    }
  }

}
