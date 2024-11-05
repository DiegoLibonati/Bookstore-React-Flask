import { Book } from "../entities/entities";

import { api_route_genres } from "./route";

export const getGenres = async (): Promise<Book["genre"][]> => {
  const request = await fetch(`${api_route_genres}`, {
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  const response: { message: string; data: Book["genre"][] } =
    await request.json();

  return response.data;
};
