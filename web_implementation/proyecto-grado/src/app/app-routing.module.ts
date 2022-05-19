import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TarrosComponent } from './tarros/tarros.component';

const routes: Routes = [
  { path: '**', redirectTo: '/tarros', pathMatch: 'full' },
  { path: 'tarros', pathMatch: 'full', component: TarrosComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
