import { render, screen } from "@testing-library/react";

import Header from "@/components/Header/Header";

interface RenderComponent {
  container: HTMLElement;
}

const renderComponent = (): RenderComponent => {
  const { container } = render(<Header />);
  return { container };
};

describe("Header", () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it("should render the header element", () => {
    renderComponent();
    expect(screen.getByRole("banner")).toBeInTheDocument();
  });

  it("should render the logo image with the correct alt text", () => {
    renderComponent();
    expect(screen.getByAltText("logo")).toBeInTheDocument();
  });

  it("should render the logo image with the mocked src", () => {
    renderComponent();
    expect(screen.getByAltText("logo")).toHaveAttribute("src", "/images/libraryLogo.png");
  });
});
