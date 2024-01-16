import { Book } from "../entities/entities";

export const getGenres = async (): Promise<Book["genero"][]> => {
  const request = await fetch("http://127.0.0.1:5000/libreria/generos");
  const response: Book["genero"][] = await request.json();

  return response;
};
