import type { JSX } from "react";
import type { FilterItemProps } from "@/types/props";

import bookService from "@/services/bookService";

import "@/components/FilterItem/FilterItem.css";

const FilterItem = ({ genre, setBooks }: FilterItemProps): JSX.Element => {
  const handleFilter = async (): Promise<void> => {
    const response = await bookService.getAllByGenre(genre);
    const books = response.data;

    setBooks(books);
  };

  return (
    <li
      onClick={() => {
        void handleFilter();
      }}
      className="filter-item"
    >
      {genre}
    </li>
  );
};

export default FilterItem;
