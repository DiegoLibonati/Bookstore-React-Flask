import { screen, render } from "@testing-library/react";
import user from "@testing-library/user-event";

import { BookProps } from "@src/entities/props";

import { Book } from "@src/components/Book/Book";

type RenderComponent = {
  container: HTMLElement;
  props: BookProps;
};

const renderComponent = (): RenderComponent => {
  const props = {
    author: "Bram Stoker",
    description:
      "Es una novela de fantasía gótica escrita por Bram Stoker, publicada en 1897.",
    image:
      "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Dracula-First-Edition-1897.jpg/220px-Dracula-First-Edition-1897.jpg",
    title: "Drácula",
  };

  const { container } = render(
    <Book
      title={props.title}
      author={props.author}
      description={props.description}
      image={props.image}
    />
  );

  return {
    container: container,
    props: props,
  };
};

describe("Book.tsx", () => {
  describe("General Tests.", () => {
    test("The book cover must be rendered when the component is rendered.", () => {
      const { props } = renderComponent();

      const imgElement = screen.getByAltText(new RegExp(props.title));

      expect(imgElement).toBeInTheDocument();
    });

    test("The title, description and author should be rendered when you click on the book cover.", async () => {
      const { props } = renderComponent();

      const imgElement = screen.getByAltText(new RegExp(props.title));

      await user.click(imgElement);

      const title = screen.getByRole("heading", {
        name: props.title,
      });
      const author = screen.getByRole("heading", {
        name: props.author,
      });
      const description = screen.getByText(props.description);

      expect(title).toBeInTheDocument();
      expect(author).toBeInTheDocument();
      expect(description).toBeInTheDocument();
    });
  });
});
