import React from "react";

import { FilterItemProps } from "@src/entities/props";

import { useGetBooksByGenre } from "@src/hooks/useGetBooksByGenre";

import "@src/components/FilterItem/FilterItem.css";

export const FilterItem = ({
  genre,
  setBooks,
}: FilterItemProps): JSX.Element => {
  const { books } = useGetBooksByGenre(genre);

  const handleFilter: React.MouseEventHandler<HTMLLIElement> = () => {
    setBooks(books);
  };

  return (
    <li onClick={(e) => handleFilter(e)} className="filter-item">
      {genre}
    </li>
  );
};
