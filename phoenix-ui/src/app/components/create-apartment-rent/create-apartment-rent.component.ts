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
import {v4 as uuidv4} from "uuid";

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
  formFiles: FormGroup;
  isAdd: boolean = true;
  isEdit: boolean = false;
  id: string | undefined;
  files!: File ;
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
    })

    this.formFiles = new FormGroup({
      files: new FormControl(''),
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
    this.files = this.formFiles.value.files; // Get the file

    if (this.isAdd) {
    this.service.createApartmentRent(this.form.value, this.files).subscribe({
        next: (result: any) => {
          alert('Congratulations! You have created dossier!')
          this.router?.navigateByUrl('/all-apartment-rent')
        },
        complete: () => {
        },
        error: (err: any) => {
          console.log(err)
        }
      }

  )}
    else{
      const extension = String(this.files).substring(String(this.files).lastIndexOf('.') + 1); // Extract file extension
      const newFileName = `${uuidv4()}.${extension}`; // Generate new file name with UUID
      this.files = new File([this.files], newFileName); // Create a new File object with the updated file name

      this.service.editApartment(this.form.value, this.files, this.id).subscribe({
        next: (result: any) => {
          alert('Congratulations! You have edited dossier!')
          this.router?.navigateByUrl('/all-apartment-rent')
        },
        complete: () => {
        },
        error: (err: any) => {
          console.log(err)
        }
      })

    }
  }

  ngOnInit(): void {
    this.isEdit =  /\d+/.test(this.router.url)

    if (this.isEdit){
      this.id = this.router.url.split('rent/')[1]
      this.isAdd = false
      this.editApartment(this.id)
    }
  }

  editApartment(id: string){
    this.service.viewApartment(id).subscribe(
      response=>{
        const response_api = (response.body as unknown as any)
        console.log(response_api)

        this.form.patchValue({
          'living_area': response_api.living_area,
          'number_of_bedrooms': response_api.number_of_bedrooms,
          'number_of_bathrooms': response_api.number_of_bathrooms,
          'rent_price': response_api.rent_price,
          'building_year': response_api.building_year,
          'address': response_api.address,
        })
        this.formFiles.patchValue({
          'files': response_api.image
        })
        console.log(this.formFiles.value)
        console.log(response.body)
        console.log(response_api)
        return response.body;
      }
    )
  }

  onFileChange(event: any) {
    if (event.target.files && event.target.files.length > 0) {
      const file = event.target.files[0];
      console.log(file)
      this.formFiles.patchValue({
        files: file.name
      });
      console.log('!!!!!!')
      console.log(this.formFiles.value)
      console.log('!!!!!!')
    }
  }


}
