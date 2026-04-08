import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import type { BookProps } from "@/types/props";

import Book from "@/components/Book/Book";

interface RenderComponent {
  container: HTMLElement;
  props: BookProps;
}

const renderComponent = (overrides?: Partial<BookProps>): RenderComponent => {
  const props: BookProps = {
    image: "https://example.com/book.jpg",
    title: "Test Book",
    author: "Test Author",
    description: "Test Description",
    ...overrides,
  };
  const { container } = render(<Book {...props} />);
  return { container, props };
};

describe("Book", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("should render the article element", () => {
    const { container } = renderComponent();
    expect(container.querySelector<HTMLElement>("article.book")).toBeInTheDocument();
  });

  it("should render the book image with correct src and alt", () => {
    const { props } = renderComponent();
    const img = screen.getByAltText(props.title);
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute("src", props.image);
  });

  it("should not show book information initially", () => {
    renderComponent();
    expect(screen.queryByRole("heading", { level: 2 })).not.toBeInTheDocument();
  });

  it("should show title, author and description when image is clicked", async () => {
    const user = userEvent.setup();
    const { props } = renderComponent();
    await user.click(screen.getByAltText(props.title));
    expect(screen.getByText(props.title)).toBeInTheDocument();
    expect(screen.getByText(props.author)).toBeInTheDocument();
    expect(screen.getByText(props.description)).toBeInTheDocument();
  });

  it("should hide book information when image is clicked again", async () => {
    const user = userEvent.setup();
    const { props } = renderComponent();
    const img = screen.getByAltText(props.title);
    await user.click(img);
    await user.click(img);
    expect(screen.queryByText(props.author)).not.toBeInTheDocument();
  });
});
