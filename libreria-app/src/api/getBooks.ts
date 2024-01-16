import { Book } from "../entities/entities";

export const getBooks = async (): Promise<Book[]> => {
  const request = await fetch("http://127.0.0.1:5000/libreria");
  const response: Book[] = await request.json();

  return response;
};
