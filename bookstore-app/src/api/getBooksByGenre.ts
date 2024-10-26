import { Book } from "../entities/entities";

import { api_route } from "./route";

export const getBooksByGenre = async (genre: string): Promise<Book[]> => {
  const request = await fetch(`${api_route}/${genre}`, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  const response: Book[] = await request.json();

  return response;
};
