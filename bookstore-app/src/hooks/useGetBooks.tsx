import { useEffect, useState } from "react";

import { Book, UseGetBooks } from "../entities/entities";

import { getBooks } from "../api/getBooks";

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
