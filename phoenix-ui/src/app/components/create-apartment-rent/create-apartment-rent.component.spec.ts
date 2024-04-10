import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateApartmentRentComponent } from './create-apartment-rent.component';

describe('CreateApartmentRentComponent', () => {
  let component: CreateApartmentRentComponent;
  let fixture: ComponentFixture<CreateApartmentRentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreateApartmentRentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateApartmentRentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
