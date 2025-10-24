import { Book } from "@src/entities/app";

import { booksApi } from "@src/api/books";

export const getBooksByGenre = async (genre: string): Promise<Book[]> => {
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

    const data = await response.json();
    const books = data.data as Book[];

    return books;
  } catch (e) {
    throw new Error(`Error fetching books by genre: ${e}.`);
  }
};
