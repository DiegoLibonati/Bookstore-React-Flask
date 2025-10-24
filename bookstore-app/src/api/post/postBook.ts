import { Book } from "@src/entities/app";
import { FormBook } from "@src/entities/forms";

import { booksApi } from "@src/api/books";

export const postBook = async (body: FormBook): Promise<Book> => {
  try {
    const response = await fetch(`${booksApi}/`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error("Error adding book.");
    }

    const data = await response.json();
    const book = data.data as Book;

    return book;
  } catch (e) {
    throw new Error(`Error adding book: ${e}.`);
  }
};
