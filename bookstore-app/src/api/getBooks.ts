import { Book } from "../entities/entities";

import { api_route_books } from "./route";

export const getBooks = async (): Promise<Book[]> => {
  const request = await fetch(`${api_route_books}`, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });

  const response: { message: string; data: Book[] } = await request.json();

  return response.data;
};
