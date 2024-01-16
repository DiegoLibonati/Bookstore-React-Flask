import { Book } from "../entities/entities";

export const getBooksByGenre = async (genre: string): Promise<Book[]> => {
  const request = await fetch(`http://127.0.0.1:5000/libreria/${genre}`);
  const response: Book[] = await request.json();

  return response;
};
