import { useEffect, useState } from "react";

import { Book } from "../entities/entities";

import { getBooks } from "../api/getBooks";

type UseGetBooks = {
  books: Book[];
  loading: boolean;
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
  handleBooks: () => Promise<void>;
};

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
