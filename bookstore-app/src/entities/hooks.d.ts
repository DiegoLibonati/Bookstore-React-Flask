export type UseForm<T> = {
  formState: T;
  onInputChange: React.ChangeEventHandler<
    HTMLInputElement | HTMLTextAreaElement
  >;
  onResetForm: () => void;
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
  genres: Book["genre"][];
  setGenres: React.Dispatch<React.SetStateAction<string[]>>;
};

export type UseHide = {
  hide: boolean;
  handleHide: () => void;
};
