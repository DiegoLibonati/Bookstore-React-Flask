import React from "react";
import { useGetBooksByGenre } from "../hooks/useGetBooksByGenre";
import { FilterItemProps } from "../entities/entities";

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
