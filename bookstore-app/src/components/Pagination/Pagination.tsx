import "./Pagination.css";

interface PaginationProps {
  totalBooks: number;
  booksPerPage: number;
  setCurrentPage: React.Dispatch<React.SetStateAction<number>>;
}

export const Pagination = ({
  totalBooks,
  booksPerPage,
  setCurrentPage,
}: PaginationProps): JSX.Element => {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalBooks / booksPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <ul className="pagination-list">
      {pageNumbers.map((number) => (
        <li
          onClick={() => setCurrentPage(number)}
          key={number * 13}
          className="pagination-list__item"
        >
          {number}
        </li>
      ))}
    </ul>
  );
};
