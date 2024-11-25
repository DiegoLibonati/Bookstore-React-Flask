import { screen, render } from "@testing-library/react";

import { Header } from "./Header";

const renderComponent = (): { container: HTMLElement } => {
  const { container } = render(<Header />);

  return {
    container: container,
  };
};

test("The library logo must be rendered.", () => {
  renderComponent();

  const altImageLogo = "logo";

  const imgElement = screen.getByAltText(altImageLogo);

  expect(imgElement).toBeInTheDocument();
  expect(imgElement).toHaveAttribute("src", "image-mock");
  expect(imgElement).toHaveAttribute("alt", altImageLogo);
});
