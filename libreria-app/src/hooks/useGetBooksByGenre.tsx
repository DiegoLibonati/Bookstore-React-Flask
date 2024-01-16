import { useEffect } from "react";
import { useState } from "react";
import { getBooksByGenre } from "../api/getBooksByGenre";
import { Book, UseGetBooksByGenre } from "../entities/entities";

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
