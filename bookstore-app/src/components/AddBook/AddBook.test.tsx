import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { AddBookProps } from "@src/entities/props";

import { AddBook } from "@src/components/AddBook/AddBook";

import { booksApi } from "@src/api/books";

import { createServer } from "@tests/msw/server";
import { bookDracula } from "@tests/jest.constants";

type RenderComponent = {
  container: HTMLElement;
  props: {
    setBooks: jest.Mock;
    setGenres: jest.Mock;
  } & AddBookProps;
};

const renderComponent = (): RenderComponent => {
  const props = {
    books: [bookDracula],
    genres: ["123"],
    setBooks: jest.fn(),
    setGenres: jest.fn(),
  };

  const { container } = render(
    <AddBook
      books={props.books}
      genres={props.genres}
      setBooks={props.setBooks}
      setGenres={props.setGenres}
    />
  );

  return {
    container: container,
    props: {
      books: props.books,
      genres: props.genres,
      setBooks: props.setBooks,
      setGenres: props.setGenres,
    },
  };
};

describe("AddBook.tsx", () => {
  describe("General Tests.", () => {
    createServer([
      {
        path: `${booksApi}/`,
        method: "post",
        res: () => {
          return {
            ok: true,
            data: bookDracula,
          };
        },
      },
    ]);

    test("The add new book button must be rendered when the component is rendered.", () => {
      renderComponent();

      const addButton = screen.getByRole("button", {
        name: /add book/i,
      });

      expect(addButton).toBeInTheDocument();
    });

    test("The form and its elements should be rendered when the add book button is clicked.", async () => {
      renderComponent();

      const addButton = screen.getByRole("button", {
        name: /add book/i,
      });

      expect(addButton).toBeInTheDocument();

      await user.click(addButton);

      const formElement = screen.getByRole("form", {
        name: /form add book/i,
      });

      expect(formElement).toBeInTheDocument();

      const inputs = ["Title", "Author", "Genre", "Description", "Image"];

      for (let input of inputs) {
        const inputElement = screen.getByRole("textbox", {
          name: new RegExp(input),
        });

        expect(inputElement).toBeInTheDocument();
      }

      const submitButton = screen.getByRole("button", {
        name: /submit/i,
      });

      expect(submitButton).toBeInTheDocument();
    });

    test("A new book must be added when the form is submitted.", async () => {
      const { props } = renderComponent();

      const addButton = screen.getByRole("button", {
        name: /add book/i,
      });

      expect(addButton).toBeInTheDocument();

      await user.click(addButton);

      const formElement = screen.getByRole("form", {
        name: /form add book/i,
      });

      expect(formElement).toBeInTheDocument();

      const inputs = ["Title", "Author", "Genre", "Description", "Image"];
      const valueText = "text in input";

      for (let input of inputs) {
        const inputElement = screen.getByRole("textbox", {
          name: new RegExp(input),
        });

        expect(inputElement).toBeInTheDocument();

        await user.click(inputElement);
        await user.keyboard(valueText);

        expect(inputElement).toHaveValue();
      }

      const submitButton = screen.getByRole("button", {
        name: /submit/i,
      });

      expect(submitButton).toBeInTheDocument();

      await user.click(submitButton);

      expect(props.setBooks).toHaveBeenCalled();
      expect(props.setBooks).toHaveBeenCalledWith([
        ...props.books,
        {
          _id: bookDracula._id,
          author: bookDracula.author,
          description: bookDracula.description,
          genre: bookDracula.genre,
          image: bookDracula.image,
          title: bookDracula.title,
        },
      ]);
      expect(props.setGenres).toHaveBeenCalled();
      expect(props.setGenres).toHaveBeenCalledWith([
        ...props.genres,
        bookDracula.genre,
      ]);
    });
  });
});
