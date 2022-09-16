import { Image } from './image';

export class Album {
  album_id: number;
  title: string = "Album title";
  comments: string;
  images : Image[] = [];
}
