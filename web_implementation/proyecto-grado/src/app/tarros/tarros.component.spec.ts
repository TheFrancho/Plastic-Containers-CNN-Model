import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TarrosComponent } from './tarros.component';

describe('TarrosComponent', () => {
  let component: TarrosComponent;
  let fixture: ComponentFixture<TarrosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TarrosComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TarrosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
