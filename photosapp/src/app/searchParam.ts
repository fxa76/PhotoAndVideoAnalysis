import { Description } from './description';
import { Camera } from './camera';
import { FileFormat } from './fileformat';
import { Source } from './source';

export class SearchParam {
  use_coords: boolean;
  gpsIsNull:boolean;
  bottomLeft: number[];
  topRight: number[];
  fromdate: number;
  todate: number;
  dateIsNull:boolean;
  descriptions: Description[];
  cameramodels: Camera[];
  fileformats: FileFormat[];
  sources: Source[];
  offset: number;
  next: number;
  source: string = "";
  iteration: string;
  id: string;
}
