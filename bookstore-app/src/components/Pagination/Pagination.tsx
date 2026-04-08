import type { JSX } from "react";
import type { PaginationProps } from "@/types/props";

import "@/components/Pagination/Pagination.css";

const Pagination = ({ totalBooks, booksPerPage, setCurrentPage }: PaginationProps): JSX.Element => {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalBooks / booksPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <ul className="pagination-list">
      {pageNumbers.map((number) => (
        <li
          onClick={() => {
            setCurrentPage(number);
          }}
          key={number * 13}
          className="pagination-list__item"
        >
          {number}
        </li>
      ))}
    </ul>
  );
};

export default Pagination;
