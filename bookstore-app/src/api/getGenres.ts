import { Book } from "../entities/entities";

import { api_route } from "./route";

export const getGenres = async (): Promise<Book["genre"][]> => {
  const request = await fetch(`${api_route}/genres`, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  const response: Book["genre"][] = await request.json();

  return response;
};
