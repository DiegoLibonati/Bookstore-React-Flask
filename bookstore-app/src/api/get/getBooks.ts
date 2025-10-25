import { GetBooksResponse } from "@src/entities/responses";

import { booksApi } from "@src/api/books";

export const getBooks = async (): Promise<GetBooksResponse> => {
  try {
    const response = await fetch(`${booksApi}/`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error fetching books.");
    }

    const data: GetBooksResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error fetching books: ${e}.`);
  }
};
