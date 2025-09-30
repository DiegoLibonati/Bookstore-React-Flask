import { useEffect, useState } from "react";

import { Book } from "@src/entities/entities";
import { UseGetBooksByGenre } from "@src/entities/hooks";

import { getBooksByGenre } from "@src/api/getBooksByGenre";

export const useGetBooksByGenre = (genre: string): UseGetBooksByGenre => {
  const [books, setBooks] = useState<Book[]>([]);

  const handleBooksByGenre = async (): Promise<void> => {
    const books = await getBooksByGenre(genre);

    setBooks(books);
    return;
  };

  useEffect(() => {
    handleBooksByGenre();
    // eslint-disable-next-line
  }, []);

  return {
    books,
  };
};
