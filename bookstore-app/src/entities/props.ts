import { Book } from "@src/entities/app";

export interface AddBookProps {
  books: Book[];
  genres: Book["genre"][];
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
  setGenres: React.Dispatch<React.SetStateAction<string[]>>;
}

export interface BookProps {
  image: string;
  title: string;
  author: string;
  description: string;
}

export interface FilterItemProps {
  genre: string;
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
}

export interface FilterMenuProps {
  genres: string[];
  filterName: string;
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
}

export interface PaginationProps {
  totalBooks: number;
  booksPerPage: number;
  setCurrentPage: React.Dispatch<React.SetStateAction<number>>;
}
