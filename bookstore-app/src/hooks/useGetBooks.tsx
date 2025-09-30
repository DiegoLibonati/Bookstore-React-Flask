import { useEffect, useState } from "react";

import { Book } from "@src/entities/entities";
import { UseGetBooks } from "@src/entities/hooks";

import { getBooks } from "@src/api/getBooks";

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
