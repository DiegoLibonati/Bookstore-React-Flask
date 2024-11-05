import { useEffect, useState } from "react";

import { Book } from "../entities/entities";

import { getBooksByGenre } from "../api/getBooksByGenre";

type UseGetBooksByGenre = {
  books: Book[];
};

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
