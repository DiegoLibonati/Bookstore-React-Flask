import { GetGenresResponse } from "@src/entities/responses";

import { booksApi } from "@src/api/books";

export const getGenres = async (): Promise<GetGenresResponse> => {
  try {
    const response = await fetch(`${booksApi}/genres`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching genres.");
    }

    const data: GetGenresResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching genres: ${e}.`);
  }
};
