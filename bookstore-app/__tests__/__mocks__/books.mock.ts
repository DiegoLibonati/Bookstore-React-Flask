import type { Book } from "@/types/app";

export const mockBook: Book = {
  _id: "asd123",
  author: "Bram Stoker",
  description: "Es una novela de fantasía gótica escrita por Bram Stoker, publicada en 1897.",
  genre: "Novela",
  image:
    "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Dracula-First-Edition-1897.jpg/220px-Dracula-First-Edition-1897.jpg",
  title: "Drácula",
};

export const mockBooks: Book[] = [mockBook];
