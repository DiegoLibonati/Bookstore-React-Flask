import { Book } from "../src/entities/entities";

export const bookDracula = {
  _id: "asd123",
  author: "Bram Stoker",
  description:
    "Es una novela de fantasía gótica escrita por Bram Stoker, publicada en 1897.",
  genre: "Novela",
  image:
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Dracula-First-Edition-1897.jpg/220px-Dracula-First-Edition-1897.jpg",
  title: "Drácula",
};
export const books: Book[] = [bookDracula];
export const genres: string[] = [bookDracula.genre];
