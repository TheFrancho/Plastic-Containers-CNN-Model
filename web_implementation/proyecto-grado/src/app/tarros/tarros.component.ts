import { Component, OnInit } from '@angular/core';
import { CheckImagesService } from '../services/check-images.service';

@Component({
  selector: 'app-tarros',
  templateUrl: './tarros.component.html',
  styleUrls: ['./tarros.component.scss']
})
export class TarrosComponent implements OnInit {

  firstSelectedFile: any;
  secondSelectedFile: any;
  thirdSelectedFile: any;
  public prediction: string;
  result: any = false;

  constructor(private checkImageService: CheckImagesService) { 
    this.prediction = '';
  }

  displayedColumns: string[] = ['key', 'value'];

  ngOnInit(): void {
  }

  onFileOneSelected(event: any): void {
    this.firstSelectedFile = event.target.files[0] ?? null;
  }

  onFileTwoSelected(event: any): void {
    this.secondSelectedFile = event.target.files[0] ?? null;
  }

  onFileThreeSelected(event: any): void {
    this.thirdSelectedFile = event.target.files[0] ?? null;
  }

  onCheckImages(): void {
    let fd = new FormData();
    fd.append('file_1', this.firstSelectedFile);
    fd.append('file_2', this.secondSelectedFile);
    fd.append('file_3', this.thirdSelectedFile);
    this.checkImageService.post(fd).subscribe(
      data => {
        let check_result = data.data

        let prediction;
        if (check_result['result'] == true) {
          prediction = 'Positivo';
          this.prediction  = prediction;
        } else {
          prediction = 'Negativo';
          this.prediction  = prediction;
        }
        this.result = [
          {'key': 'Predicción', 'value': prediction},
          {'key': 'Tarro frontal', 'value': `${check_result['front']}%`},
          {'key': 'Tarro tracero', 'value': `${check_result['back']}%`},
          {'key': 'Tarro arriba', 'value': `${check_result['up']}%`}
        ];
      },
      error => {
        this.prediction = 'Negativo';
        this.result = [
          {
            'key': 'Error',
            'value': 'Ha ocurrido un error al intentar comprobar las imágenes'
          }
        ];
      }
    );
  }

}
