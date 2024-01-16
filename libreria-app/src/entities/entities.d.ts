export type Book = {
  _id: {
    $oid: string;
  };
  title: string;
  author: string;
  description: string;
  image: string;
  genero: string;
};

export type UseGetBooks = {
  books: Book[];
  loading: boolean;
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
  handleBooks: () => Promise<void>;
};

export type UseGetBooksByGenre = {
  books: Book[];
};

export type UseGetGenres = {
  genres: Book["genero"][];
  setGenres: React.Dispatch<React.SetStateAction<string[]>>;
};

export type UseHide = {
  hide: boolean;
  handleHide: () => void;
};

export type FormBook = {
  title: string;
  author: string;
  genre: string;
  description: string;
  image: string;
};

export interface FilterMenuProps {
  genres: string[];
  filterName: string;
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
}

export interface FilterItemProps {
  genre: string;
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
}

export interface AddBookProps {
  books: Book[];
  genres: Book["genero"][];
  setBooks: React.Dispatch<React.SetStateAction<Book[]>>;
  setGenres: React.Dispatch<React.SetStateAction<string[]>>;
}

export interface PaginationProps {
  totalBooks: number;
  booksPerPage: number;
  setCurrentPage: React.Dispatch<React.SetStateAction<number>>;
}

export interface BookProps {
  image: string;
  title: string;
  author: string;
  description: string;
}
