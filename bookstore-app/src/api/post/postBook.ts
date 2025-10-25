import { PostBookResponse } from "@src/entities/responses";
import { FormBook } from "@src/entities/forms";

import { booksApi } from "@src/api/books";

export const postBook = async (body: FormBook): Promise<PostBookResponse> => {
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

    const data: PostBookResponse = await response.json();

    return data;
  } catch (e) {
    throw new Error(`Error adding book: ${e}.`);
  }
};
