import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewApartmentRentComponent } from './view-apartment-rent.component';

describe('ViewApartmentRentComponent', () => {
  let component: ViewApartmentRentComponent;
  let fixture: ComponentFixture<ViewApartmentRentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewApartmentRentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ViewApartmentRentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
