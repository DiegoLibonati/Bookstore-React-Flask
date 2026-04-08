import { BsPlusCircle } from "react-icons/bs";

import type { JSX } from "react";

import type { FormBook } from "@/types/forms";
import type { AddBookProps } from "@/types/props";

import { useForm } from "@/hooks/useForm";
import { useHide } from "@/hooks/useHide";

import bookService from "@/services/bookService";

import "@/components/AddBook/AddBook.css";

const AddBook = ({ books, genres, setBooks, setGenres }: AddBookProps): JSX.Element => {
  const { hide, handleHide } = useHide();

  const { formState, onInputChange } = useForm<FormBook>({
    title: "",
    author: "",
    genre: "",
    description: "",
    image: "",
  });

  const handleAdd = async (): Promise<void> => {
    const response = await bookService.add(formState);
    const newBook = response.data;

    setBooks([...books, { ...newBook }]);

    if (!genres.includes(newBook.genre)) {
      setGenres([...genres, newBook.genre]);
    }
  };

  const handleSubmit: React.SubmitEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();
    void handleAdd();
  };

  return (
    <article className="add-book">
      <button
        type="button"
        aria-label="Open add book form"
        className="add-book__btn"
        onClick={() => {
          handleHide();
        }}
      >
        <BsPlusCircle id="AddBookIconPlus" className="add-book__btn-icon"></BsPlusCircle>
      </button>

      {hide ? (
        <form
          aria-label="Add new book form"
          className="add-book__form"
          onSubmit={(e) => {
            handleSubmit(e);
          }}
        >
          <label htmlFor="title" className="add-book__form-label add-book__form-label--hide">
            Title
          </label>
          <input
            id="title"
            type="text"
            name="title"
            placeholder="Set title"
            className="add-book__form-input"
            value={formState.title}
            onChange={(e) => {
              onInputChange(e);
            }}
          ></input>
          <label htmlFor="author" className="add-book__form-label add-book__form-label--hide">
            Author
          </label>
          <input
            id="author"
            type="text"
            name="author"
            placeholder="Set author"
            className="add-book__form-input"
            value={formState.author}
            onChange={(e) => {
              onInputChange(e);
            }}
          ></input>
          <label htmlFor="genre" className="add-book__form-label add-book__form-label--hide">
            Genre
          </label>
          <input
            id="genre"
            type="text"
            name="genre"
            placeholder="Set genre"
            className="add-book__form-input"
            value={formState.genre}
            onChange={(e) => {
              onInputChange(e);
            }}
          ></input>
          <label htmlFor="description" className="add-book__form-label add-book__form-label--hide">
            Description
          </label>
          <textarea
            id="description"
            placeholder="Set description"
            name="description"
            className="add-book__form-textarea"
            value={formState.description}
            onChange={(e) => {
              onInputChange(e);
            }}
          ></textarea>
          <label htmlFor="image" className="add-book__form-label add-book__form-label--hide">
            Image
          </label>
          <input
            id="image"
            type="text"
            name="image"
            placeholder="Set image link"
            className="add-book__form-input"
            value={formState.image}
            onChange={(e) => {
              onInputChange(e);
            }}
          ></input>
          <button type="submit" aria-label="Submit new book" className="add-book__form-submit">
            Submit
          </button>
        </form>
      ) : null}
    </article>
  );
};

export default AddBook;
