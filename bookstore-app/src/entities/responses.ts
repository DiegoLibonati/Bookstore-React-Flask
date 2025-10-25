import { Book } from "@src/entities/app";

export type GetBooksResponse = {
  message: string;
  code: string;
  data: Book[];
};

export type GetBooksByGenreResponse = {
  message: string;
  code: string;
  data: Book[];
};

export type GetGenresResponse = {
  message: string;
  code: string;
  data: Book["genre"][];
};

export type PostBookResponse = {
  message: string;
  code: string;
  data: Book;
};
