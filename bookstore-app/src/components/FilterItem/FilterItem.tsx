import React from "react";

import { FilterItemProps } from "@src/entities/props";

import { getBooksByGenre } from "@src/api/get/getBooksByGenre";

import "@src/components/FilterItem/FilterItem.css";

export const FilterItem = ({
  genre,
  setBooks,
}: FilterItemProps): JSX.Element => {
  const handleFilter: React.MouseEventHandler<HTMLLIElement> = async () => {
    const responseBooksByGenre = await getBooksByGenre(genre);

    setBooks(responseBooksByGenre);
  };

  return (
    <li onClick={(e) => handleFilter(e)} className="filter-item">
      {genre}
    </li>
  );
};
