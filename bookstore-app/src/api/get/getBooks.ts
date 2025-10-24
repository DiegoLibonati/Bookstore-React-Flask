import { Book } from "@src/entities/app";

import { booksApi } from "@src/api/books";

export const getBooks = async (): Promise<Book[]> => {
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

    const data = await response.json();
    const books = data.data as Book[];

    return books;
  } catch (e) {
    throw new Error(`Error fetching books: ${e}.`);
  }
};
