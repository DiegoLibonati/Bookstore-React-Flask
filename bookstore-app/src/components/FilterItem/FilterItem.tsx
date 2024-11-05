import React from "react";

import { Book } from "../../entities/entities";

import { useGetBooksByGenre } from "../../hooks/useGetBooksByGenre";

interface FilterItemProps {
  genre: string;
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
}

export const FilterItem = ({
  genre,
  setBooks,
}: FilterItemProps): JSX.Element => {
  const { books } = useGetBooksByGenre(genre);

  const handleFilter: React.MouseEventHandler<HTMLLIElement> = () => {
    setBooks(books);
  };

  return <li onClick={(e) => handleFilter(e)}>{genre}</li>;
};
