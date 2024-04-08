import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApartmentSaleComponent } from './apartment-sale.component';

describe('ApartmentSaleComponent', () => {
  let component: ApartmentSaleComponent;
  let fixture: ComponentFixture<ApartmentSaleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ApartmentSaleComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ApartmentSaleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
