import { Book } from "@src/entities/app";

import { booksApi } from "@src/api/books";

export const getGenres = async (): Promise<Book["genre"][]> => {
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

    const data = await response.json();
    const genres = data.data as Book["genre"][];

    return genres;
  } catch (e) {
    throw new Error(`Error fetching genres: ${e}.`);
  }
};
