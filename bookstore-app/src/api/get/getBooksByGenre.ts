import { GetBooksByGenreResponse } from "@src/entities/responses";

import { booksApi } from "@src/api/books";

export const getBooksByGenre = async (
  genre: string
): Promise<GetBooksByGenreResponse> => {
  try {
    const response = await fetch(`${booksApi}/${genre}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching books by genre.");
    }

    const data: GetBooksByGenreResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching books by genre: ${e}.`);
  }
};
