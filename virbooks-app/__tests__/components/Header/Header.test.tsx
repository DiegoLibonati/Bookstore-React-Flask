import { render, screen } from "@testing-library/react";

import type { RenderResult } from "@testing-library/react";

import Header from "@/components/Header/Header";

const renderComponent = (): RenderResult => render(<Header />);

describe("Header", () => {
  describe("rendering", () => {
    it("should render the header element", () => {
      renderComponent();
      expect(screen.getByRole("banner")).toBeInTheDocument();
    });

    it("should render the logo image", () => {
      renderComponent();
      expect(screen.getByRole("img", { name: "logo" })).toBeInTheDocument();
    });
  });
});
