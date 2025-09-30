import { screen, render } from "@testing-library/react";

import { Header } from "@src/components/Header/Header";

type RenderComponent = { container: HTMLElement };

const renderComponent = (): RenderComponent => {
  const { container } = render(<Header />);

  return {
    container: container,
  };
};

describe("Header.tsx", () => {
  describe("General Tests.", () => {
    test("The library logo must be rendered.", () => {
      renderComponent();

      const altImageLogo = "logo";

      const imgElement = screen.getByAltText(altImageLogo);

      expect(imgElement).toBeInTheDocument();
      expect(imgElement).toHaveAttribute("src", "image-mock");
      expect(imgElement).toHaveAttribute("alt", altImageLogo);
    });
  });
});
