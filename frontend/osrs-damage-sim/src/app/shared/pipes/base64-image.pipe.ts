import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Pipe({
  name: 'base64Image',
})
export class Base64ImagePipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}
  transform(encodedImage: string): SafeResourceUrl {
    const blob = this.dataURItoBlob(encodedImage);
    const url = URL.createObjectURL(blob);
    return this.sanitizer.bypassSecurityTrustUrl(url);
  }

  dataURItoBlob(dataURI: string) {
    const byteString = window.atob(dataURI);

    const ab = new ArrayBuffer(byteString.length);
    const ia = new Uint8Array(ab);
    for (let i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
    }

    const blob = new Blob([ab], { type: 'image/png' });
    return blob;
  }
}
