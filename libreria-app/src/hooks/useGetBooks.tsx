import { useEffect } from "react";
import { useState } from "react";
import { getBooks } from "../api/getBooks";
import { Book, UseGetBooks } from "../entities/entities";

export const useGetBooks = (): UseGetBooks => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const handleBooks = async () => {
    const books = await getBooks();

    setBooks(books);
    setLoading(false);
  };

  useEffect(() => {
    handleBooks();
  }, []);

  return {
    books,
    loading,
    setBooks,
    handleBooks,
  };
};
